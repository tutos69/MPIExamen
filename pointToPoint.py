from mpi4py import MPI
import time
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.rank
# print("my rank is : ", rank)

if rank == 0:
  # tm = int(input("Ingrese el tamaño de la matriz: "))
  size_ = (1024, 1024)
  matriz1 = np.random.randint(10, size=size_).astype("float") / 100
  matriz2 = np.random.randint(10, size=size_).astype("float") / 100
  producto_res = np.dot(matriz1, matriz2)
  filas = np.vsplit(matriz1, 8)
  columnas = matriz2
  inicio = time.time()
  for i in range(1, 9):
    fila = filas[i-1]
    destination_process = i
    comm.send([fila, columnas], dest=destination_process)
  comm.send([producto_res,inicio], dest=9)

for kk in range(1, 9):
  if rank == kk:
    data = comm.recv(source=0)
    # print(len(data[0][0]))
    filas_a = len(data[0])
    filas_b = len(data[1])
    columnas_a = len(data[0][0])
    columnas_b = len(data[1][0])
    size_ = (filas_a, columnas_a)
    calculo = np.zeros(dtype=float, shape=size_)
    for i in range(filas_a):
      for j in range(columnas_b):
        suma = 0
        for k in range(columnas_a):
          suma += data[0][i][k] * data[1][k][j]
        calculo[i][j] = suma
    envia1 = calculo
    destination_process = 9
    comm.send(envia1, dest=destination_process)


if rank == 9:
  data2 = list([0, 0, 0, 0, 0, 0, 0, 0])
  respuestaNumpy = comm.recv(source=0)
  for i in range(1, 9):
    data2[i-1] = comm.recv(source=i)    
  ListaUnida = np.concatenate((data2[0], data2[1], data2[2], data2[3], data2[4], data2[5], data2[6], data2[7]), axis=0)
  fin = time.time()
  print('¿Los resultados son correctos?', np.allclose(ListaUnida, respuestaNumpy[0]))
  print("El proceso de multiplicar las matrices paralelamente PuntoAPunto se ejecutó en %d segundos" % (fin - respuestaNumpy[1]))
