from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
   # tm = int(input("Ingrese el tamaño de la matriz: "))
   size_ = (2048, 2048)
   matriz1 = np.random.randint(10, size=size_).astype("float") / 100
   matriz2 = np.random.randint(10, size=size_).astype("float") / 100
   producto_res = np.dot(matriz1, matriz2)
   filas = np.vsplit(matriz1, 8)
   columnas = matriz2
   array_to_share = [[filas[0],columnas],[filas[1],columnas],[filas[2],columnas],[filas[3],columnas],[filas[4],columnas],[filas[5],columnas],[filas[6],columnas],[filas[7],columnas],producto_res] 
           
else:
   array_to_share = None

def calculoMatriz(matrizs):
   filas = matrizs[0]
   columnas = matrizs[1]
   filas_a = len(filas)
   filas_b = len(columnas)
   columnas_a = len(filas[0])
   columnas_b = len(columnas[0])
   size_ = (filas_a, columnas_a)
   calculo = np.zeros(dtype=float, shape=size_)
   for i in range(filas_a):
      for j in range(columnas_b):
         suma = 0
         for k in range(columnas_a):
            suma += filas[i][k] * columnas[k][j]
         calculo[i][j] = suma
   return calculo

recvbuf = comm.scatter(array_to_share, root=0)
for kk in range(8):
   if rank == kk:
      envia1 = calculoMatriz(recvbuf)
      comm.send(envia1, dest=8)

if rank == 8:
   respuestaNumpy = recvbuf
   data2 = list([0, 0, 0, 0, 0, 0, 0, 0])
   for i in range(8):
      data2[i] = comm.recv(source=i)
   ListaUnida = np.concatenate((data2[0], data2[1], data2[2], data2[3], data2[4], data2[5], data2[6], data2[7]), axis=0)
   print('¿Los resultados son correctos?', np.allclose(ListaUnida, respuestaNumpy))
