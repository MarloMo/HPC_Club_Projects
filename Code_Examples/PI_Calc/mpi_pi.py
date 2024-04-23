import numpy as np
import random as rnd
from matplotlib import pyplot as plt
from mpi4py import MPI
import time as tm

###
# Use this terminal command to run:
# $ mpirun -np 3 python3.12 mpi_pi.py
###

start = tm.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def estimatePI(N):
    '''
    This function estimates the value of Pi
    Params:
    N - Hits + Misses (Total number of throws)

    Returns - array of pi estimates and number of hits
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


# Divide the darts to throw among the processors,
# instead of each processor throwing the total
N = [1e7 // size]

Pi_results = estimatePI(N)

print(
    str(Pi_results[1]) + " hits on core " + str(rank) + " out of " + str(N) +
    " throws.")

# Have on processor add up the totals accross all the processors
throwsAllCores = N[0] * size
hitAllCores = comm.allreduce(Pi_results[1], op=MPI.SUM)

# Computes Pi
if rank == 0:
    print(
        str(hitAllCores) + " hits on all cores, with " + str(throwsAllCores) +
        "throws.")

    pi = 4.0 * float(hitAllCores) / float(throwsAllCores)
    print("parallel pi = ", pi)

    end = tm.time()
    print("Run in " + str(end - start) + " seconds.")
