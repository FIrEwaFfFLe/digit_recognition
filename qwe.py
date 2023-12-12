import matplotlib.image as img
from numpy import *


def get():
    image = img.imread("9.png").tolist()
    return [image[i // 28][i % 28][0] for i in range(784)]
