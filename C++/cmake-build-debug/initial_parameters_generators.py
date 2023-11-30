from random import *


n = 4
lengths = [785, 17, 17, 10]
biases = [[] for i in range(n)]
for i in range(n):
    if i == 0:
        biases[i] = [0] * lengths[i]
    else:
        biases[i] = [randint(-500, 500) / 100 for _ in range(lengths[i])]
weights = [[[] for _ in range(lengths[i])] for i in range(n - 1)]
for i in range(n - 1):
    for j in range(lengths[i]):
        if i != n - 2:
            weights[i][j] = [randint(-500, 500) / 100 for _ in range(lengths[i + 1] - 1)]
        else:
            weights[i][j] = [randint(-500, 500) / 100 for _ in range(lengths[i + 1])]
file = open("parameters.txt", "w")
print(n, file=file)
print(*lengths, file=file)
for i in range(n):
    print(*biases[i], file=file, end=" ")
print(file=file)
for i in range(n - 1):
    for j in range(lengths[i]):
        print(*weights[i][j], file=file, end=" ")
