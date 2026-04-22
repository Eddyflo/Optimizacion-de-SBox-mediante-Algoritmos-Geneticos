# Optimizacion-de-SBox-mediante-Algoritmos-Geneticos
Este proyecto se enfoca en la generación y optimización de cajas de sustitución (S-Boxes) con propiedades criptograficas mejores. Se combina la generación algebraica basada en Campos de Galois con un Algoritmo Genético. 


## Descripcion técnica de Archivos
* **main.py** Es el controlador principal del proyecto. Dirije el flujo generacional, gestiona la selección de individuos y controla la convergencia de la población.

* **generar_sbox.py** Aquí se impleta la trasnformación afín e Inversa Multiplicativa sobre el campo de Galois utilizando el polinomio irreducible de Rijndael ($0x11B$).

* **complementoAG.py** Motor evolutivo que contiene la definición formal de los operadores de cruce (Cycle Crossover - CX) y mutaciones (Scramble y Swap) sobre permutaciones.

* **fitness.py** Interfaz de comunicación que utiliza el módulo `subprocess` para ejecutar el evaluador externo y recuperar las métricas de aptitud de **evaluador.c**

* **evaluador.c** Este es el núcleo de cálculo intensivo desarrollado en C. Evalúa 9 métricas criptográficas de forma nativa para optimizar el tiempo de ejecución del Algoritmo Genético.


## Requisitos y Dependencias
Para la correcta ejecución del entorno del proyecto en windows o Linux se necesita:

* **Lenguajes**: Python 3.9+ y compilador GCC.
* **Bibliotecas de Python**:
    * `numpy`: Gestión de arreglos y operaciones bit a bit.
    * `galois`: Aritmética de campos finitos.
* **Herramientas de compilación**: GCC (vía w64devkit en Windows) para generar el binario del evaluador. 
Aunque se inlucye el archivo evaluador.exe es recomdame contar con esta herramienta en caso de que se requiera volver a compilar `evaluador.c`

## Intrucciones de Instalación y de Uso

### Clonación del Repositorio
```bash
git clone https://github.com/Eddyflo/Optimizacion-de-SBox-mediante-Algoritmos-Geneticos

```
## Compilación del Evaluador

```
# Para Windows (.exe)
gcc evaluador.c -o evaluador.exe

#Para linux
gcc evaluador.c -o evaluador
```

## Ejecución del Proyecto

```
pyhton main.py
```