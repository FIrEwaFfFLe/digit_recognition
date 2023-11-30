from keras.datasets import mnist
from numpy import *

(train_X, train_y), (test_X, test_y) = mnist.load_data()


qwe = open("training_data.txt", "w")
a, b = train_X.tolist(), train_y.tolist()
end = []
for i in range(60000):
    first = []
    second = [0.01] * 10
    for j in range(28):
        for k in range(28):
            print(a[i][j][k] / 255, end=" ", file=qwe)
    second[b[i]] = 0.99
    print(*second, end=" ", file=qwe)
qwe.close()

