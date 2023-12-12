from math import *


def sigmoid(x) -> float:
    return 1 / (1 + pow(e, -x))


def call(test):

    array = [[test[min(j, lengths[0] - 1)] * (i == 0) for j in range(lengths[i])] for i in range(n)]

    for i in range(1, n):
        for j in range(lengths[i]):
            for k in range(lengths[i - 1]):
                array[i][j] += array[i - 1][k] * weights[i - 1][k][j]
            array[i][j] += biases[i][j]
            array[i][j] = sigmoid(array[i][j])

    anss = [(array[n - 1][i], i) for i in range(lengths[n - 1])]
    anss.sort()
    print(anss[-1][1], anss[-2][1], anss[-3][1])


inp = open("train", "r")
read = inp.readlines()

n = int(read[0])
lengths = list(map(int, read[1].split()))
biases = [[] for _ in range(n)]
cnt = 0
raw = list(map(float, read[3].split()))
for i in range(n):
    for j in range(lengths[i]):
        biases[i].append(raw[cnt])
        cnt += 1
weights = [[] for _ in range(n - 1)]
cnt = 0
raw = list(map(float, read[2].split()))
for i in range(n - 1):
    for k in range(lengths[i]):
        weights[i].append([])
        for j in range(lengths[i + 1]):
            weights[i][k].append(raw[cnt])
            cnt += 1
