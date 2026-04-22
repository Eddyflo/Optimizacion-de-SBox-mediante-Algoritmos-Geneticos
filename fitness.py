import subprocess
import os

EJECUTABLE_C = "./evaluador"

# ─────────────────────────────────────────────
#  Umbrales de filtro
# ─────────────────────────────────────────────
UMBRAL_NL        = 80    # no linealidad mínima
UMBRAL_DU        = 10    # uniformidad diferencial máxima
UMBRAL_BN        = 2     # branch number mínimo
MAX_PUNTOS_FIJOS = 2     # puntos fijos máximos (filtro interno)
MAX_PUNTOS_INV   = 2     # puntos fijos inversos máximos (filtro interno)
TARGET_DSAC      = 800   # meta de DSAC para el fitness


def _ejecutar_evaluador(sbox_hex):
    """
    Llama al evaluador C.
    Salida esperada: nl dsac du bn fijos fijos_inv num_ciclos min_ciclo lin_struct lp
    Devuelve tupla con todos los valores o None si falla.
    """
    ejecutable = EJECUTABLE_C
    if not os.path.exists(ejecutable):
        if os.path.exists(ejecutable + ".exe"):
            ejecutable = ejecutable + ".exe"
        else:
            raise FileNotFoundError(f"No se encontró {ejecutable}.")

    try:
        resultado = subprocess.run(
            [ejecutable] + list(sbox_hex),
            capture_output=True,
            text=True,
            check=True
        )
        datos = resultado.stdout.strip().split()
        if len(datos) < 10:
            return None

        nl         = int(datos[0])
        dsac       = int(datos[1])
        du         = int(datos[2])
        bn         = int(datos[3])
        fijos      = int(datos[4])
        fijos_inv  = int(datos[5])
        num_ciclos = int(datos[6])
        min_ciclo  = int(datos[7])
        lin_struct = int(datos[8])
        lp         = float(datos[9])

        return nl, dsac, du, bn, fijos, fijos_inv, num_ciclos, min_ciclo, lin_struct, lp

    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
        print(f"Error en evaluación: {e}")
        return None


def consultar_fitness(sbox_hex):
    """
    Evalúa una S-box siguiendo la estructura del paper (Mishra et al., 2023).

    Filtros internos (no se reportan en pantalla):
        1. Biyectividad — garantizada por permutación
        2. Puntos fijos < MAX_PUNTOS_FIJOS
        3. Puntos fijos inversos < MAX_PUNTOS_INV
        4. Uniformidad diferencial <= UMBRAL_DU
        5. No linealidad >= UMBRAL_NL
        6. Branch number >= UMBRAL_BN

    Métrica de optimización: DSAC (minimizar)
        fitness = TARGET_DSAC - dsac  (mayor = mejor)

    Métricas de reporte (no afectan fitness):
        num_ciclos, min_ciclo, lin_struct, lp

    Devuelve:
        (fitness, nl, dsac, du, bn, num_ciclos, min_ciclo, lin_struct, lp, paso_filtros)
    """
    metricas = _ejecutar_evaluador(sbox_hex)
    if metricas is None:
        return -9999, 0, 9999, 99, 0, 0, 0, 1, 1.0, False

    nl, dsac, du, bn, fijos, fijos_inv, num_ciclos, min_ciclo, lin_struct, lp = metricas

    # ── Filtros en orden ──
    if fijos >= MAX_PUNTOS_FIJOS:
        return -1000 - fijos, nl, dsac, du, bn, num_ciclos, min_ciclo, lin_struct, lp, False

    if fijos_inv >= MAX_PUNTOS_INV:
        return -1000 - fijos_inv, nl, dsac, du, bn, num_ciclos, min_ciclo, lin_struct, lp, False

    if du > UMBRAL_DU:
        return -500 - du, nl, dsac, du, bn, num_ciclos, min_ciclo, lin_struct, lp, False

    if nl < UMBRAL_NL:
        return nl - UMBRAL_NL, nl, dsac, du, bn, num_ciclos, min_ciclo, lin_struct, lp, False

    if bn < UMBRAL_BN:
        return -200, nl, dsac, du, bn, num_ciclos, min_ciclo, lin_struct, lp, False

    # ── Pasó todos los filtros: optimizar DSAC ──
    fitness = TARGET_DSAC - dsac
    return fitness, nl, dsac, du, bn, num_ciclos, min_ciclo, lin_struct, lp, True


if __name__ == "__main__":
    test_hex = [f"{v:02x}" for v in range(256)]
    print("Probando con S-box identidad...")
    r = consultar_fitness(test_hex)
    fitness, nl, dsac, du, bn, nc, mc, ls, lp, paso = r
    print(f"NL={nl}  DSAC={dsac}  DU={du}  BN={bn}")
    print(f"Ciclos={nc}  MinCiclo={mc}  LinStruct={ls}  LP={lp:.6f}")
    print(f"Pasó filtros: {paso}  |  Fitness: {fitness}")
