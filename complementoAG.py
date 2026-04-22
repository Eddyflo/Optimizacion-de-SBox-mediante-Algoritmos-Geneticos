import random
from generar_sbox import hex_a_int, int_a_hex


def aplicar_cx(p1_hex, p2_hex):
    """
    Cycle Crossover (CX) sobre S-boxes en formato hex.
    Convierte a int internamente, aplica CX, devuelve hex.
    """
    p1 = hex_a_int(p1_hex)
    p2 = hex_a_int(p2_hex)
    size = len(p1)

    h1 = [-1] * size
    h2 = [-1] * size

    visitado = [False] * size
    ciclos = []

    for start in range(size):
        if visitado[start]:
            continue
        ciclo = []
        idx = start
        while not visitado[idx]:
            visitado[idx] = True
            ciclo.append(idx)
            idx = p1.index(p2[idx])
        ciclos.append(ciclo)

    for k, ciclo in enumerate(ciclos):
        for idx in ciclo:
            if k % 2 == 0:
                h1[idx] = p1[idx]
                h2[idx] = p2[idx]
            else:
                h1[idx] = p2[idx]
                h2[idx] = p1[idx]

    return int_a_hex(h1), int_a_hex(h2)


def aplicar_scramble(sbox_hex):
    """
    Mutación scramble sobre S-box en hex.
    Baraja un segmento aleatorio de mínimo 2 elementos.
    """
    sbox = sbox_hex[:]
    size = len(sbox)
    idx1 = random.randint(0, size - 3)
    idx2 = random.randint(idx1 + 2, size - 1)

    segmento = sbox[idx1:idx2]
    random.shuffle(segmento)
    sbox[idx1:idx2] = segmento
    return sbox


def aplicar_swap(sbox_hex, n_swaps=3):
    """
    Mutación swap: intercambia n pares de posiciones aleatorias.
    Más suave que scramble.
    """
    sbox = sbox_hex[:]
    for _ in range(n_swaps):
        i, j = random.sample(range(len(sbox)), 2)
        sbox[i], sbox[j] = sbox[j], sbox[i]
    return sbox


def seleccion_torneo(poblacion, scores, k=3):
    """
    Selección por torneo: elige k individuos al azar, devuelve el mejor.
    """
    aspirantes  = random.sample(list(range(len(poblacion))), k)
    ganador_idx = max(aspirantes, key=lambda i: scores[i])
    return poblacion[ganador_idx][:]
