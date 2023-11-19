from generation import *
from math import *


def sigmoid(x) -> float:
    return 1 / (1 + pow(e, -x))


def ReLU(x) -> float:
    return max(0, x)


inp = open("train", "r")
read = inp.readlines()

n = eval(read[0])
lengths = eval(read[1])
weights = eval(read[2])
biases = eval(read[3])

while True:
    test = list(map(float, input().split()))

    array = [[test[min(j, lengths[0] - 1)] * (i == 0) for j in range(lengths[i])] for i in range(n)]

    for i in range(1, n):
        for j in range(lengths[i]):
            for k in range(lengths[i - 1]):
                array[i][j] += array[i - 1][k] * weights[i - 1][k][j]
            array[i][j] += biases[i][j]
            array[i][j] = sigmoid(array[i][j])

    print(*[array[n - 1][i] for i in range(lengths[n - 1])])
