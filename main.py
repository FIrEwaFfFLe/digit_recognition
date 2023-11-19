from math import *
from generation import *


def sigmoid(x) -> float:
    return 1 / (1 + pow(e, -x))


def sigmoid_prime(x) -> float:
    sig = sigmoid(x)
    return sig * (1 - sig)


def ReLU(x) -> float:
    return max(0, x)


data = open("train", "w")

n = 5
lengths = [3, 5, 9, 9, 7]
biases = [[randint(-500, 500) / 100 * (i != 0) for _ in range(lengths[i])] for i in range(n)]
weights = [[[randint(-500, 500) / 100 for _ in range(lengths[i + 1])] for _ in range(lengths[i])] for i in range(n - 1)]
# form of testing list: [[|input data|, |output data|], [...], ...]
testing = get_natsum(30)
C = []

for repeat in range(1000):
    for test in testing:

        # test performing
        array = [[test[0][min(j, lengths[0] - 1)] * (i == 0) for j in range(lengths[i])] for i in range(n)]
        z = [[test[0][min(j, lengths[0] - 1)] * (i == 0) for j in range(lengths[i])] for i in range(n)]
        y = [test[1][i] for i in range(lengths[n - 1])]

        for i in range(1, n):
            for j in range(lengths[i]):
                for k in range(lengths[i - 1]):
                    array[i][j] += array[i - 1][k] * weights[i - 1][k][j]
                array[i][j] += biases[i][j]
                z[i][j] = array[i][j]
                array[i][j] = sigmoid(array[i][j])

        # cost function
        C_cur = 0
        for i in range(lengths[n - 1]):
            C_cur += pow(array[n - 1][i] - y[i], 2)
        C.append(C_cur)

        # derivative calculations
        d_bias_z = [[0] * lengths[i] for i in range(n)]
        d_array = [[0] * lengths[i] for i in range(n)]
        d_weights = [[[0] * lengths[i + 1] for _ in range(lengths[i])] for i in range(n - 1)]

        for i in range(lengths[n - 1]):
            d_array[n - 1][i] = 2 * (array[n - 1][i] - y[i])
            d_bias_z[n - 1][i] = d_array[n - 1][i] * sigmoid_prime(z[n - 1][i])
        for i in range(n - 2, -1, -1):
            for k in range(lengths[i]):
                for j in range(lengths[i + 1]):
                    d_weights[i][k][j] = d_bias_z[i + 1][j] * array[i][k]
                    d_array[i][k] += d_bias_z[i + 1][j] * weights[i][k][j]
                d_bias_z[i][k] = d_array[i][k] * sigmoid_prime(z[i][k])

        # gradient descent
        for i in range(n):
            for j in range(lengths[i]):
                biases[i][j] -= d_bias_z[i][j]
        for i in range(n - 1):
            for k in range(lengths[i]):
                for j in range(lengths[i + 1]):
                    weights[i][k][j] -= d_weights[i][k][j]
        '''
        print(d_bias_z, d_array, d_weights, sep='\n')
        print(test[0])
        print(weights)
        print(biases)
        print(z)
        print(array)
        '''

print(C[0], C[-1])
print(n, lengths, weights, biases, sep="\n", file=data)
