from math import *
from generation import *


class average:
    def __init__(self):
        self.summer = 0
        self.count = 0
        self.avg = 0

    def add(self, other):
        self.summer += other
        self.count += 1
        self.avg = self.summer / self.count


def sigmoid(x) -> float:
    return 1 / (1 + pow(e, -x))


def sigmoid_prime(x) -> float:
    sig = sigmoid(x)
    return sig * (1 - sig)


def ReLU(x) -> float:
    return max(0, x)


data = open("train", "w")

n = 8
lengths = [2, 10, 10, 10, 10, 10, 10, 1]
biases = [[randint(-500, 500) / 100 * (i != 0) for _ in range(lengths[i])] for i in range(n)]
weights = [[[randint(-500, 500) / 100 for _ in range(lengths[i + 1])] for _ in range(lengths[i])] for i in range(n - 1)]
test_cases = 1000000
# form of testing list: [[|input data|, |output data|], [...], ...]
testing = get_multi(test_cases)
C = []

repeats = 5
batch_size = 10
learning_rate = 1

for repeat in range(repeats):

    for batch in range(0, test_cases, batch_size):

        gradient_weights = [[[average() for _ in range(lengths[i + 1])] for _ in range(lengths[i])] for i in range(n - 1)]
        gradient_biases = [[average() for _ in range(lengths[i])] for i in range(n)]
        C_cur = average()

        for current_test in range(batch, batch + batch_size):
            test = testing[current_test]
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
            C_cur_cur = 0
            for i in range(lengths[n - 1]):
                C_cur_cur += pow(array[n - 1][i] - y[i], 2)
            C_cur.add(C_cur_cur)

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
                    gradient_biases[i][j].add(d_bias_z[i][j])
            for i in range(n - 1):
                for k in range(lengths[i]):
                    for j in range(lengths[i + 1]):
                        gradient_weights[i][k][j].add(d_weights[i][k][j])
            '''
            print(d_bias_z, d_array, d_weights, sep='\n')
            print(test[0])
            print(weights)
            print(biases)
            print(z)
            print(array)
            '''

        C.append(C_cur.avg)
        print(batch, C[-1])

        for i in range(n):
            for j in range(lengths[i]):
                biases[i][j] -= gradient_biases[i][j].avg * learning_rate

        for i in range(n - 1):
            for k in range(lengths[i]):
                for j in range(lengths[i + 1]):
                    weights[i][k][j] -= gradient_weights[i][k][j].avg * learning_rate

print(n, lengths, weights, biases, sep="\n", file=data)
