#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>

// ─────────────────────────────────────────────
//  Producto punto en GF(2)
// ─────────────────────────────────────────────
int dot_product(uint8_t a, uint8_t b) {
    uint8_t v = a & b;
    int parity = 0;
    while (v) { parity ^= (v & 1); v >>= 1; }
    return parity;
}

// ─────────────────────────────────────────────
//  Fast Walsh Hadamard Transform
// ─────────────────────────────────────────────
void fwht(int *W, int n) {
    for (int step = 1; step < n; step *= 2) {
        for (int i = 0; i < n; i += 2 * step) {
            for (int j = i; j < i + step; j++) {
                int u = W[j], v = W[j + step];
                W[j] = u + v;
                W[j + step] = u - v;
            }
        }
    }
}

// ─────────────────────────────────────────────
//  1. No linealidad
// ─────────────────────────────────────────────
int calcular_nl(uint8_t *sbox) {
    int max_lat = 0;

    #pragma omp parallel
    {
        int local_max = 0;
        int W[256];

        #pragma omp for
        for (int b = 1; b < 256; b++) {
            for (int x = 0; x < 256; x++) {
                W[x] = dot_product(b, sbox[x]) ? -1 : 1;
            }
            fwht(W, 256);
            for (int a = 1; a < 256; a++) {
                int val = abs(W[a]);
                if (val > local_max) local_max = val;
            }
        }

        #pragma omp critical
        { if (local_max > max_lat) max_lat = local_max; }
    }

    return 128 - (max_lat / 2);
}

// ─────────────────────────────────────────────
//  2. DSAC — Distance from Strict Avalanche Criterion
//  Ecuación 3: suma de |128 - SAC[Xi][Yj]|
//  Ideal = 0
// ─────────────────────────────────────────────
int calcular_dsac(uint8_t *sbox) {
    int dsac = 0;
    for (int i = 0; i < 8; i++) {
        uint8_t xi = (uint8_t)(1 << i);
        for (int j = 0; j < 8; j++) {
            int count = 0;
            for (int x = 0; x < 256; x++) {
                uint8_t diff = sbox[x] ^ sbox[x ^ xi];
                if ((diff >> j) & 1) count++;
            }
            dsac += abs(128 - count);
        }
    }
    return dsac;
}

// ─────────────────────────────────────────────
//  3. Uniformidad diferencial
//  δ(F) = max |{x : S(x) XOR S(x XOR α) = β}|
//  AES = 4
// ─────────────────────────────────────────────
int calcular_du(uint8_t *sbox) {
    int max_val = 0;
    for (int alpha = 1; alpha < 256; alpha++) {
        int tabla[256] = {0};
        for (int x = 0; x < 256; x++) {
            tabla[sbox[x] ^ sbox[x ^ alpha]]++;
        }
        for (int beta = 0; beta < 256; beta++) {
            if (tabla[beta] > max_val) max_val = tabla[beta];
        }
    }
    return max_val;
}

// ─────────────────────────────────────────────
//  4. Branch number diferencial
//  βd = min{ wt(x XOR x') + wt(S(x) XOR S(x')) }
//  AES = 2
// ─────────────────────────────────────────────
int popcount8(uint8_t v) {
    int c = 0;
    while (v) { c += (v & 1); v >>= 1; }
    return c;
}

int calcular_bn(uint8_t *sbox) {
    int min_bn = 999;
    for (int x = 0; x < 256; x++) {
        for (int xp = x + 1; xp < 256; xp++) {
            // Cast explícito a uint8_t antes de operar
            uint8_t dx  = (uint8_t)(x ^ xp);
            uint8_t dsx = (uint8_t)(sbox[x] ^ sbox[xp]);
            int bn = popcount8(dx) + popcount8(dsx);
            if (bn < min_bn) min_bn = bn;
        }
    }
    return min_bn;
}
// ─────────────────────────────────────────────
//  5. Puntos fijos (filtro interno, no se imprime)
//  fijo:     S(x) XOR x == 0x00
//  inv fijo: S(x) XOR x == 0xFF
// ─────────────────────────────────────────────
void calcular_puntos_fijos(uint8_t *sbox, int *fijos, int *fijos_inv) {
    *fijos = 0; *fijos_inv = 0;
    for (int x = 0; x < 256; x++) {
        uint8_t xv = x ^ sbox[x];
        if (xv == 0x00) (*fijos)++;
        if (xv == 0xFF) (*fijos_inv)++;
    }
}

// ─────────────────────────────────────────────
//  6. Número de ciclos y longitud mínima de ciclo
//  Se recorre la S-box como función x → S(x)
//  Un ciclo es una cadena que regresa al inicio
// ─────────────────────────────────────────────
void calcular_ciclos(uint8_t *sbox, int *num_ciclos, int *min_ciclo) {
    int visitado[256] = {0};
    *num_ciclos = 0;
    *min_ciclo  = 256;

    for (int start = 0; start < 256; start++) {
        if (visitado[start]) continue;

        // Recorrer desde start hasta cerrar el ciclo
        int longitud = 0;
        int x = start;
        while (!visitado[x]) {
            visitado[x] = 1;
            x = sbox[x];
            longitud++;
        }

        (*num_ciclos)++;
        if (longitud < *min_ciclo) *min_ciclo = longitud;
    }
}

// ─────────────────────────────────────────────
//  7. Estructura lineal no nula
//  Si existe α ≠ 0 tal que S(x) XOR S(x XOR α)
//  es constante para todo x, α es estructura lineal.
//  Devuelve 1 si existe alguna (mala), 0 si no hay (buena)
// ─────────────────────────────────────────────
int tiene_estructura_lineal(uint8_t *sbox) {
    for (int alpha = 1; alpha < 256; alpha++) {
        uint8_t valor = sbox[0] ^ sbox[0 ^ alpha];
        int es_constante = 1;
        for (int x = 1; x < 256; x++) {
            if ((sbox[x] ^ sbox[x ^ alpha]) != valor) {
                es_constante = 0;
                break;
            }
        }
        if (es_constante) return 1;
    }
    return 0;
}

// ─────────────────────────────────────────────
//  8. Propagación lineal
//  LPmax = max( 2*Pr[X·a = S(X)·b] - 1 )²
//  para a,b ≠ 0
//  AES = 0.015625 (2⁻⁶)
// ─────────────────────────────────────────────
double calcular_lp(uint8_t *sbox) {
    double max_lp = 0.0;

    for (int a = 1; a < 256; a++) {
        for (int b = 1; b < 256; b++) {
            int count = 0;
            for (int x = 0; x < 256; x++) {
                if (dot_product(a, x) == dot_product(b, sbox[x]))
                    count++;
            }
            // Pr = count / 256
            double pr   = (double)count / 256.0;
            double lp   = (2.0 * pr - 1.0) * (2.0 * pr - 1.0);
            if (lp > max_lp) max_lp = lp;
        }
    }

    return max_lp;
}

// ─────────────────────────────────────────────
//  Main
// ─────────────────────────────────────────────
int main(int argc, char *argv[]) {

    if (argc != 257) {
        fprintf(stderr, "Uso: %s <256 valores en hex>\n", argv[0]);
        return 1;
    }

    uint8_t sbox[256];
    for (int i = 0; i < 256; i++) {
        unsigned int val;
        if (sscanf(argv[i + 1], "%x", &val) != 1 || val > 255) {
            fprintf(stderr, "Valor hex invalido: %s\n", argv[i + 1]);
            return 1;
        }
        sbox[i] = (uint8_t)val;
    }

    // ── Calcular todas las métricas ──
    int nl  = calcular_nl(sbox);
    int dsac = calcular_dsac(sbox);
    int du  = calcular_du(sbox);
    int bn  = calcular_bn(sbox);

    int fijos, fijos_inv;
    calcular_puntos_fijos(sbox, &fijos, &fijos_inv);

    int num_ciclos, min_ciclo;
    calcular_ciclos(sbox, &num_ciclos, &min_ciclo);

    int lin_struct = tiene_estructura_lineal(sbox);

    double lp = calcular_lp(sbox);

    // ── Salida: nl dsac du bn fijos fijos_inv num_ciclos min_ciclo lin_struct lp ──
    printf("%d %d %d %d %d %d %d %d %d %.6f\n",
           nl, dsac, du, bn,
           fijos, fijos_inv,
           num_ciclos, min_ciclo,
           lin_struct, lp);

    return 0;
}
