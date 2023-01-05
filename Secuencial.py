import numpy as np   
import multiprocessing



size_ = (128,128)
matriz1 = np.random.randint(10, size=size_).astype("float") / 100
matriz2 = np.random.randint(10, size=size_).astype("float") / 100
print("hola")
import time
inicio = time.time()

filas_a = len(matriz1)
filas_b = len(matriz2)
columnas_a = len(matriz1[0])
columnas_b = len(matriz2[0])

if columnas_a != filas_b:
    print('No es posible realizar la multiplicacion de matrices')

producto = np.zeros(dtype=float, shape=size_)
for i in range(filas_a):
    for j in range(columnas_b):
        suma = 0
        for k in range(columnas_a):
            suma += matriz1[i][k] * matriz2[k][j]
        producto[i][j] = suma
fin = time.time()
print("El proceso de multiplicar las matrices secuencialmente se ejecutó en %d segundos" % (fin - inicio))