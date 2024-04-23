import numpy as np
import random as rnd
from matplotlib import pyplot as plt


def estimatePI(N):
    '''
    This function estimates the value of Pi
    Params:
    N - Hits + Misses (Total number of throws)

    Returns - array of pi estimates
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

    return result


# Throws list
N = [1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7]

Pi_results = estimatePI(N)

# difference to determine the error in the convergence.
diff_list = []
for i in range(len(Pi_results)):
    diff_list.append(np.abs(Pi_results[i] - np.pi))

plt.plot(np.array(N), diff_list, label="abs(estimatePi - Pi)")
plt.legend()
plt.xscale('log')
plt.xlabel("number of throws")
plt.yscale('log')
plt.ylabel("convergence")
plt.savefig("convergence_test.pdf")
