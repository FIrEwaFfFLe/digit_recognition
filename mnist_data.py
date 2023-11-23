from keras.datasets import mnist

(train_X, train_y), (test_X, test_y) = mnist.load_data()

qwe = open("testing_data", "w")
a, b = test_X.tolist(), test_y.tolist()
end = []
for i in range(10000):
    first = []
    second = [0] * 10
    for j in range(28):
        for k in range(28):
            first.append(a[i][j][k] / 255)
    second[b[i]] = 1
    end.append([first, second])
print(end, file=qwe)
