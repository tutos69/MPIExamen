from mpi4py import MPI
import time
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def calculoMatriz(pos,matriz):
    filas = np.vsplit(matriz[0], 8)
    columnas = matriz[1]
    fila = filas[pos]
    filas_a = len(fila)
    filas_b = len(columnas)
    columnas_a = len(fila[0])
    columnas_b = len(columnas[0])
    size_ = (filas_a, columnas_a)
    calculo = np.zeros(dtype=float, shape=size_)
    for i in range(filas_a):
        for j in range(columnas_b):
            suma = 0
            for k in range(columnas_a):
                suma += fila[i][k] * columnas[k][j]
            calculo[i][j] = suma
    return calculo

data = 0

if rank == 0:
    size_ = (64, 64)
    matriz1 = np.random.randint(10, size=size_).astype("float") / 100
    matriz2 = np.random.randint(10, size=size_).astype("float") / 100
    matrices = [matriz1,matriz2]
    data = calculoMatriz(rank,matrices)
    for kk in range(1, 8): 
        comm.send(matrices, dest=kk)

for mt in range(1, 8): 
    if rank == mt:
        datos =comm.recv(source=0) 
        data = calculoMatriz(mt,datos)
 

data2 = comm.gather(data, root=0)
if rank == 0:
    producto_res = np.dot(matriz1, matriz2)
    paralela_res = np.reshape(data2, size_)
    print('¿Los resultados son correctos?', np.allclose(paralela_res, producto_res))


