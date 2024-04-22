import numpy as np
import random as rnd
from matplotlib import pyplot as plt
from mpi4py import MPI
import time as tm

start = tm.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def estimatePI(N):
    '''
    N: Hits + Misses (Total number of throws)
    '''

    result = []

    for i in range(len(N)):
        # M: Hits (starting from 0)
        M = 0
        for j in range(int(N[i])):

            x = rnd.random()
            y = rnd.random()
            r_squared = x * x + y * y

            if (r_squared < 1):
                M = M + 1
        Pi = 4.0 * M / N[i]
        result.append(Pi)

    return result, M


# N = [1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7]
N = [1e7 // size]

Pi_results = estimatePI(N)

diff_list = []
for i in range(len(Pi_results[0])):
    diff_list.append(np.abs(Pi_results[0][i] - np.pi))

# print(Pi_results)

print(
    str(Pi_results[1]) + " hits on core " + str(rank) + " out of " + str(N) +
    " throws.")

throwsAllCores = N[0] * size
hitAllCores = comm.allreduce(Pi_results[1], op=MPI.SUM)

if rank == 0:
    print(
        str(hitAllCores) + " hits on all cores, with " + str(throwsAllCores) +
        "throws.")

    pi = 4.0 * float(hitAllCores) / float(throwsAllCores)
    print("parallel pi = ", pi)

    end = tm.time()
    print("Run in " + str(end - start) + " seconds.")
