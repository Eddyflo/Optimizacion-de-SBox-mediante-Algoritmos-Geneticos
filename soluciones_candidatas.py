import numpy as np
from galois import GF # Librería recomendada para campos finitos


# Definir el campo GF(2) para verificar invertibilidad de matrices
GF2 = GF(2)

def generar_poblacion_inicial(tamano=10000):
    poblacion = []
    
    while len(poblacion) < tamano:
        # 1. Generar matriz aleatoria 8x8 de bits
        matriz_candidata = GF2.Random((8, 8))
        
        # 2. Verificar si es invertible (Determinante != 0 en GF(2))
        if np.linalg.det(matriz_candidata) != 0:
            # Es válida, la agregamos
            poblacion.append(matriz_candidata)
            
    return poblacion

# Generamos las 10,000 matrices
candidatos = generar_poblacion_inicial()
print(f"Generadas {len(candidatos)} matrices invertibles.")

"""for i, matriz in enumerate(candidatos[:5]):  # Mostrar solo las primeras 5 para no saturar la salida
    print(f"Matriz {i+1}:\n{matriz}\n")
"""