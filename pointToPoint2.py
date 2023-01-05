from mpi4py import MPI
import time
import numpy as np


comm = MPI.COMM_WORLD
tamanio=comm.Get_size()
rank = comm.rank
print("my rank is : ", rank)

if rank == 0:
  tm = int(input("Ingrese el tamaño de la matriz: "))
  size_ = (tm, tm)
  matriz1 = np.random.randint(10, size=size_).astype("float") / 100
  matriz2 = np.random.randint(10, size=size_).astype("float") / 100
  producto_res = np.dot(matriz1, matriz2)
  filas = np.vsplit(matriz1, tamanio-2)
  columnas = matriz2
  for i in range(1, tamanio-1):
    fila = filas[i-1]
    destination_process = i
    comm.send([fila, columnas], dest=destination_process)
  comm.send(producto_res, dest=tamanio-1)

for kk in range(1, tamanio-1):
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
    destination_process = tamanio-1
    comm.send(envia1, dest=destination_process)


if rank == tamanio-1:
  data2 = list()
  # ListaUnida = list()
  respuestaNumpy = comm.recv(source=0)
  for i in range(1, tamanio-1):
    data2.append(comm.recv(source=i)) 
    # print(np.shape(data2[i-1]))  
    # ListaUnida.append(data2[i-1],axis=0)
    ListaUnida = np.concatenate(data2, axis=0)
    # print(np.shape(ListaUnida))


  # ListaUnida = np.concatenate((data2[0], data2[1], data2[2], data2[3], data2[4], data2[5], data2[6], data2[7]), axis=0)
  # print(np.shape(data2[0]))
  # print(np.shape(ListaUnida))
 
  print('¿Los resultados son correctos?', np.allclose(ListaUnida, respuestaNumpy))
