from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()



size_ = (2, 2)
# matriz1 = numpy.random.randint(10, size=size_).astype("float") / 100
# matriz2 = numpy.random.randint(10, size=size_).astype("float") / 100

# print(size)
senddata = numpy.random.randint(10, size=size_).astype("float") / 100
recvdata = numpy.random.randint(10, size=size_).astype("float") / 100
comm.Alltoall(senddata,recvdata)


print(rank, "  \n ",  senddata ,"  \n \n ", recvdata)
