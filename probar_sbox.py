import fitness as fo

def evaluar_e_imprimir(nombre, sbox_hex, referencias=None):
    print(f"\n{'='*55}")
    print(f"  Evaluando: {nombre}")
    print(f"{'='*55}")

    r = fo.consultar_fitness(sbox_hex)
    fitness, nl, dsac, du, bn, nc, mc, ls, lp, paso = r

    ref = referencias or {}

    def cmp(val, key):
        if key in ref:
            return f"(paper: {ref[key]})"
        return ""

    print(f"  No linealidad (NL)          = {nl:<6} {cmp(nl, 'nl')}")
    print(f"  DSAC                        = {dsac:<6} {cmp(dsac, 'dsac')}")
    print(f"  Uniformidad diferencial (DU)= {du:<6} {cmp(du, 'du')}")
    print(f"  Branch number (BN)          = {bn:<6} {cmp(bn, 'bn')}")
    print(f"  Número de ciclos            = {nc:<6} {cmp(nc, 'ciclos')}")
    print(f"  Longitud mínima de ciclo    = {mc:<6} {cmp(mc, 'min_ciclo')}")
    print(f"  Estructura lineal no nula   = {'SI' if ls else 'NO':<6} {cmp(ls, 'ls')}")
    print(f"  Propagación lineal (LP)     = {lp:<.6f} {cmp(lp, 'lp')}")
    print(f"  Pasó filtros                = {'SI' if paso else 'NO'}")
    print(f"  Fitness                     = {fitness}")


# ── S-box I1 del paper ──
I1 = [
    "9c","32","36","fd","fe","f7","57","bc","67","89","3c","69","35","ba","62","55",
    "18","ed","77","51","95","76","bb","f2","ce","d5","6a","c2","20","c6","f5","7f",
    "a3","5a","84","c1","cb","c3","3d","b4","c7","a5","3b","91","9a","1e","04","23",
    "4a","b0","02","10","8b","47","29","8c","25","ec","e1","f4","fc","a2","60","3a",
    "e2","8e","a6","87","e4","34","19","66","72","63","d9","03","65","97","c9","41",
    "11","16","ea","50","6d","39","0f","7a","94","7b","ab","6f","13","bf","15","db",
    "75","5c","01","f6","1b","dc","08","22","b7","fa","e6","5d","7e","ac","4f","0d",
    "1d","09","74","45","e7","43","0c","31","a7","c0","12","0e","e0","56","9d","79",
    "d7","21","8f","33","da","24","d4","2f","df","a9","3e","cf","53","d6","e8","96",
    "f3","82","d0","be","61","0a","eb","8a","d8","3f","07","40","b2","b9","ee","71",
    "f8","6b","00","8d","7c","46","cd","b5","73","1a","ad","ff","88","28","58","f1",
    "37","14","a8","5b","49","b6","b3","6e","38","d2","52","9f","30","9e","a1","81",
    "0b","92","ae","aa","2b","ca","cc","d3","93","dd","59","44","70","c4","e5","86",
    "f9","a0","af","5f","1f","85","5e","2d","90","a4","b1","64","4d","1c","48","2c",
    "9b","99","80","83","fb","7d","26","4b","ef","27","2e","f0","b8","bd","06","d1",
    "2a","05","e9","42","c8","54","78","98","17","e3","c5","4e","6c","de","68","4c"
]

evaluar_e_imprimir("I1 del paper", I1, {
    "nl": 112, "dsac": 352, "du": 4, "bn": 2,
    "ciclos": 7, "lp": 0.015625
})



# ── S-box I2 del paper ──
I2 = [
    "63","be","b0","77","40","3e","a4","f8","1f","66","f9","58","87","ea","3a","b8",
    "6c","57","3f","b6","1d","14","c1","1b","fb","b9","6f","a0","82","ae","22","6a",
    "b4","d4","16","97","de","8b","d2","ad","85","a6","c0","13","71","7e","17","b5",
    "f4","a3","05","39","7a","84","fc","43","a7","7c","0c","09","5c","9f","26","eb",
    "3b","5f","91","21","29","ac","47","34","1a","11","e2","2e","03","01","c2","96",
    "12","2b","6e","9d","56","dc","75","4f","36","64","e1","4a","0e","cf","1c","fe",
    "23","c6","32","15","5b","c7","4c","9e","9a","4e","35","ed","41","d8","d1","69",
    "49","67","08","98","1e","8a","42","89","ba","bc","25","5e","27","8f","48","78",
    "a5","a9","74","95","d5","8c","92","ee","f0","fd","e5","d0","aa","8e","72","2a",
    "30","04","9c","e4","0d","50","45","51","c9","ce","20","bd","bf","dd","60","2d",
    "52","44","19","68","5d","af","cc","86","31","70","f3","6b","4d","d7","c8","2c",
    "9b","37","d6","ff","c3","b1","94","61","f7","80","81","54","a2","7f","a8","33",
    "7b","24","c4","ca","e0","f5","e7","ab","0f","ec","e3","b3","06","b2","02","0a",
    "79","83","ef","f1","55","3d","da","f2","38","8d","88","28","cd","62","e8","d9",
    "5a","46","18","2f","65","76","90","df","4b","bb","c5","07","f6","d3","0b","b7",
    "cb","3c","59","a1","e9","93","53","6d","00","10","99","fa","7d","db","73","e6"
]

evaluar_e_imprimir("I2 del paper", I2, {
    "nl": 112, "dsac": 364, "du": 4, "bn": 2,
    "ciclos": 3, "lp": 0.015625
})

def verificar_permutacion(nombre, sbox_hex):
    valores = [int(v, 16) for v in sbox_hex]
    if sorted(valores) != list(range(256)):
        faltantes = set(range(256)) - set(valores)
        repetidos = [v for v in valores if valores.count(v) > 1]
        print(f"  ERROR en {nombre}: no es permutación válida")
        print(f"  Faltantes: {[hex(x) for x in list(faltantes)[:5]]}")
        print(f"  Repetidos: {[hex(x) for x in list(set(repetidos))[:5]]}")
    else:
        print(f"  {nombre}: permutación válida ✓")

verificar_permutacion("I2", I2)
def contar_puntos_fijos(nombre, sbox_hex):
    valores = [int(v, 16) for v in sbox_hex]
    fijos     = sum(1 for x, s in enumerate(valores) if (x ^ s) == 0x00)
    fijos_inv = sum(1 for x, s in enumerate(valores) if (x ^ s) == 0xFF)
    print(f"  {nombre}: puntos fijos={fijos}, puntos fijos inversos={fijos_inv}")

contar_puntos_fijos("I2", I2)

I3 = [
    "63","b3","ca","36","00","d3","9f","33","c2","02","2f","5e","fc","69","ae","bc",
    "06","3b","cf","c5","b0","da","7c","bf","5d","a0","68","e2","9d","9b","f0","09",
    "b7","35","a8","d4","31","f7","3a","f5","8e","ed","60","c9","39","5c","b4","ab",
    "38","8c","ee","c0","21","92","4e","6e","f1","2e","84","e5","23","a2","8d","75",
    "b2","4d","db","9e","e8","e9","13","d7","a3","bb","1f","fb","e1","93","12","c8",
    "d5","9a","74","d0","27","43","44","65","a5","70","71","04","f6","05","ac","3c",
    "ec","6f","d8","c6","30","73","0b","be","c3","79","cb","7a","1c","3e","54","67",
    "6a","1e","f9","b1","de","eb","72","85","ce","c1","e3","51","91","8a","76","53",
    "83","88","58","a6","29","e4","b5","14","45","52","0c","48","e6","96","57","86",
    "aa","f2","cc","10","98","28","61","34","0a","19","82","dd","af","5f","0d","95",
    "5a","7d","cd","7b","3f","87","6b","e0","b6","25","2b","15","17","5b","16","89",
    "df","b9","47","20","0e","d6","ba","11","56","ef","f3","55","90","40","94","c4",
    "3d","ff","1d","64","6d","24","7e","fa","ea","66","03","a4","80","b8","fd","8b",
    "4f","81","08","59","49","bd","4c","37","dc","f8","99","f4","77","7f","1b","22",
    "2c","0f","d1","e7","6c","2a","c7","2d","18","d2","01","9c","4a","26","97","d9",
    "78","a1","42","fe","07","a9","46","1a","8f","a7","ad","41","32","50","4b","62"
]

evaluar_e_imprimir("I3 del paper", I3, {
    "nl": 112, "dsac": 380, "du": 4, "bn": 2,
    "ciclos": 1, "min_ciclo": 256, "lp": 0.015625
})

contar_puntos_fijos("I3", I3)
