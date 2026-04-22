import numpy as np
import galois
from soluciones_candidatas import generar_poblacion_inicial

print("Iniciando generación...")
candidatos = generar_poblacion_inicial(10000)



# 1. CONFIGURACIÓN DEL CAMPO DE GALOIS (AES)
# El polinomio irreducible de Rijndael es: x^8 + x^4 + x^3 + x + 1 (0x11B)
# galois.GF(2**8) por defecto usa un polinomio primitivo diferente, 
# así que debemos forzar el de AES explícitamente.
AES_GF = galois.GF(2**8, irreducible_poly=0x11b)

def byte_a_bits(valor_byte):
    """Convierte un entero (0-255) a un vector columna de 8 bits (numpy array)."""
    # Formato little-endian para la multiplicación matricial estándar de AES
    bits = [(valor_byte >> i) & 1 for i in range(8)]
    return np.array(bits, dtype=int)

def bits_a_byte(vector_bits):
    """Convierte un vector de 8 bits a un entero."""
    valor = 0
    for i in range(8):
        valor |= int(vector_bits[i]) << i
    return valor

def construir_sbox_desde_matriz(matriz_candidata, vector_constante=0x63):
    """
    Convierte una Matriz Candidata (Genotipo) en una S-box completa (Fenotipo).
    
    Args:
        matriz_candidata: Matriz 8x8 de 0s y 1s (numpy array).
        vector_constante: Entero (por defecto 0x63 como en AES).
        
    Returns:
        Una lista de 256 enteros representando la S-box.
    """
    sbox = []
    # convertimos el objeto de galois a un array de numpy puro para las operaciones bit a bit
    matriz_enteros = np.array(matriz_candidata, dtype = int)

    # Convertir constante V a vector de bits para la operación XOR final
    vector_v = byte_a_bits(vector_constante)
    
    for x in range(256):
        # --- PASO PRIMITIVO 1: INVERSA MULTIPLICATIVA ---
        # Si x es 0, su inversa es 0. Si no, calculamos en GF(2^8)
        if x == 0:
            inv_x_int = 0
        else:
            # Creamos el elemento en el campo y calculamos su inversa
            poly_x = AES_GF(x)
            inv_x_poly = np.reciprocal(poly_x) 
            inv_x_int = int(inv_x_poly) # Convertir de vuelta a entero puro
            
        # --- PASO PRIMITIVO 2: TRANSFORMACIÓN AFÍN ---
        # Fórmula: S(x) = (M * inv_x) XOR V
        
        # 1. Convertir la inversa a vector de bits
        inv_x_bits = byte_a_bits(inv_x_int)
        
        # 2. Multiplicación Matricial sobre GF(2)
        # Usamos producto punto estándar y luego módulo 2
        producto = np.dot(matriz_enteros, inv_x_bits) % 2
        
        # 3. Suma del vector constante (equivalente a XOR en binario)
        resultado_bits = (producto + vector_v) % 2
        
        # 4. Convertir bits finales a byte y guardar
        sbox_val = bits_a_byte(resultado_bits)
        sbox.append(sbox_val)
        
    return sbox

def hex_a_int(lista_hex):
    """
    Convierte una lista de strings hexadecimales a una lista de enteros.
    Útil para procesar la S-box en el Algoritmo Genético.
    """
    return [int(x, 16) if isinstance(x, str) else x for x in lista_hex]

def int_a_hex(lista_int):
    """
    Convierte una lista de enteros a su representación hexadecimal (0x00).
    Útil para exportar la S-box final.
    """
    return [format(x, '#04x') for x in lista_int]

def crear_poblacion_inicial(tamano_poblacion):
    """
    Puente para generar la población usando las matrices candidatas.
    """
    poblacion = []
    # Usamos los candidatos generados al inicio del script
    for i in range(min(tamano_poblacion, len(candidatos))):
        sbox_lista = construir_sbox_desde_matriz(candidatos[i])
        # Convertimos a hex para que sea consistente con el resto del flujo del AG
        poblacion.append(int_a_hex(sbox_lista))
    return poblacion
