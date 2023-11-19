from random import *


def get_natsum(amount):
    tests = []
    for i in range(amount):
        inp = [randint(0, 1) for _ in range(3)]
        s = inp[0] + inp[1] * 2 + inp[2] * 3
        outp = [0] * 7
        outp[s] = 1
        tests.append([inp, outp])
    return tests


def get_multi(amount):
    tests = []
    for i in range(amount):
        inp = [randint(0, 10000) / 10000 for _ in range(2)]
        outp = [inp[0] * inp[1]]
        tests.append([inp, outp])
    return tests
