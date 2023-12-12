from keras.datasets import mnist

(train_X, train_y), (test_X, test_y) = mnist.load_data()


a, b = train_X.tolist(), train_y.tolist()
end = [0] * 10
for i in range(60000):
    end[b[i]] += 1
print(end)

