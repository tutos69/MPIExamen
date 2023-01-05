import numpy as np
import time
from mpi4py import MPI


def multiplicacion_matrices_paralela(params):
    numero_proceso = params["section"]
    matriz1 = params["matriz1"]
    matriz2 = params["matriz2"]
    columnas_a = len(matriz1[0])
    columnas_b = len(matriz2[0])
    filas_por_proceso = int(len(matriz1) / 8)
    multiplicacion = np.zeros(dtype=float, shape=(filas_por_proceso, len(matriz1)))
    for i in range(numero_proceso * filas_por_proceso, (numero_proceso + 1) * filas_por_proceso):
        for j in range(columnas_b):
            suma = 0
            for k in range(columnas_a):
                suma += matriz1[i][k] * matriz2[k][j]
            multiplicacion[i - (numero_proceso * filas_por_proceso)][j] = suma
    return multiplicacion


comm=MPI.COMM_WORLD
rank = comm.rank

if rank==0:
    size_ = (512, 512)
    matriz1 = np.random.randint(10, size=size_).astype("float") / 100
    matriz2 = np.random.randint(10, size=size_).astype("float") / 100

    numero_procesos = 8
    matriz_multiplicacion_paralela = np.zeros(dtype=float, shape=(size_[0], size_[1]))
    matriz_multiplicacion_paralela_comp = np.zeros(dtype=float, shape=(numero_procesos, int(size_[0] / numero_procesos), size_[1]))
    inicio = time.time()
    comm.send({"section": 0, "matriz1": matriz1, "matriz2": matriz2}, dest=1)
    comm.send({"section": 1, "matriz1": matriz1, "matriz2": matriz2}, dest=2)
    comm.send({"section": 2, "matriz1": matriz1, "matriz2": matriz2}, dest=3)
    comm.send({"section": 3, "matriz1": matriz1, "matriz2": matriz2}, dest=4)
    
    comm.send({"section": 4, "matriz1": matriz1, "matriz2": matriz2},dest=5)
    comm.send({"section": 5, "matriz1": matriz1, "matriz2": matriz2},dest=6)
    comm.send({"section": 6, "matriz1": matriz1, "matriz2": matriz2},dest=7)
    comm.send({"section": 7, "matriz1": matriz1, "matriz2": matriz2},dest=8)

    data1=comm.recv(source=1)
    data2=comm.recv(source=2)
    data3=comm.recv(source=3)
    data4=comm.recv(source=4)

    data5=comm.recv(source=5)
    data6=comm.recv(source=6)
    data7=comm.recv(source=7)
    data8=comm.recv(source=8)


    matriz_multiplicacion_paralela_comp[0] = data1
    matriz_multiplicacion_paralela_comp[1] = data2
    matriz_multiplicacion_paralela_comp[2] = data3
    matriz_multiplicacion_paralela_comp[3] = data4

    matriz_multiplicacion_paralela_comp[4]= data5
    matriz_multiplicacion_paralela_comp[5]= data6
    matriz_multiplicacion_paralela_comp[6]= data7
    matriz_multiplicacion_paralela_comp[7]= data8

    fin = time.time()
    tiempo_paralelo = fin - inicio
    print("El proceso de multiplicar las matrices paralelamente PuntoAPunto se ejecutó en %d segundos" % (fin - inicio))
    paralela_res = np.reshape(
    matriz_multiplicacion_paralela_comp, (size_[0], size_[1]))
    # print("Mis resultados obtenidos en paralelo")
    # for i in range(4):
    #     print("%f" % (paralela_res[i][i]))
    # print('Resultados de numpy')
    producto_res = np.dot(matriz1, matriz2)
    #producto_res = producto_res.T
    # for i in range(4):
        # print("%f" % (producto_res[i][i]))

        # print(np.array(matriz_multiplicacion_paralela_comp).shape)

    print('¿Los resultados son correctos?',np.allclose(producto_res, paralela_res))

   
if rank==1:
    data=comm.recv(source=0)
    multiplicacion = multiplicacion_matrices_paralela(data)
    comm.send(multiplicacion,dest=0)

if rank==2:
    data=comm.recv(source=0)
    multiplicacion = multiplicacion_matrices_paralela(data)
    comm.send(multiplicacion,dest=0)

if rank==3:
    data=comm.recv(source=0)
    multiplicacion = multiplicacion_matrices_paralela(data)
    comm.send(multiplicacion,dest=0)

if rank==4:
    data=comm.recv(source=0)
    multiplicacion = multiplicacion_matrices_paralela(data)
    comm.send(multiplicacion,dest=0)

if rank == 5:
    data =comm.recv(source=0)
    resultante = multiplicacion_matrices_paralela(data)
    comm.send(resultante,dest=0)
if rank == 6:
    data =comm.recv(source=0)
    resultante = multiplicacion_matrices_paralela(data)
    comm.send(resultante,dest=0)
if rank == 7:
    data =comm.recv(source=0)
    resultante = multiplicacion_matrices_paralela(data)
    comm.send(resultante,dest=0)
if rank == 8:
    data =comm.recv(source=0)
    resultante = multiplicacion_matrices_paralela(data)
    comm.send(resultante,dest=0)