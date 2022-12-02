import random
import sys
import NeuralNetwork as nn
import numpy as np
import matplotlib.pyplot as plt


class Parabola:
    def __init__(self, a, b, c):
        self.A = a
        self.B = b
        self.C = c
        self.net = nn.NeuralNetwork(1, 5, 1, 0.1)
        # take in point (2), produce A, B, and C for
        # parabola Ax^2 + Bx + C

    def curve(self, x):
        return self.A * (x ** 2) + self.B * x + self.C

    def makeNNData(self, x):
        # print(x, ", ", self.curve(x))
        return nn.NNData(x, [self.curve(x)])


par = Parabola(-1, 0.01, 1)
dList = []
dataSize = 100000
for i in range(dataSize):
    d = par.makeNNData(random.randrange(-1000, 1000) / 1000)
    dList.append(d)
    par.net.train(d.input, d.target)

for i in range(0, dataSize, int(dataSize / 100)):
    pt = dList[i]
    x = pt.input
    y = par.net.feedForward(x)
    plt.plot(x, y, marker="o", markersize=5, markerfacecolor="black")

a = np.linspace(-1, 1, 1000)
plt.plot(a, par.curve(a))
plt.grid()
plt.show()
