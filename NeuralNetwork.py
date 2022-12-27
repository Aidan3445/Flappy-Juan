import math
import numpy
import numpy as np


# Neural network class with one hidden layer
class NeuralNetwork:
    def __init__(self, inputNum, hiddenNum, outputNum, learningRate):
        self.numI = inputNum  # number of inputs
        self.numH = hiddenNum  # number of hidden layer nodes
        self.numO = outputNum  # number of outputs
        self.lr = learningRate  # learning rate of the neural net
        self.wI = np.random.randn(hiddenNum, inputNum)  # create input weights array
        self.wO = np.random.randn(outputNum, hiddenNum)  # create hidden layer weights array
        self.biasH = np.random.randn(hiddenNum, 1)  # create hidden weights bias
        self.biasO = np.random.randn(outputNum, 1)  # create output weights bias
        self.count = 0  # counter for keying track of the number of datasets passed through

    # get output from a given input array
    def feedForward(self, inputArray):
        # calculate outputs at hidden layer
        inputMatrix = np.transpose(inputArray).reshape(self.numI, 1)
        hidden = np.dot(self.wI, inputMatrix)
        hidden += self.biasH
        hidden = numpy.reshape(list(map(self.sigmoid, hidden)), (self.numH, 1))

        # calculate outputs at output layer
        output = np.dot(self.wO, hidden)
        output += self.biasO
        output = numpy.reshape(list(map(self.sigmoid, output)), (self.numO, 1))

        # transpose back into array
        output = np.transpose(output)
        return output

    # updates nodes based on input dataset and expected output
    def train(self, inputArray, targetArray):
        # calculate outputs at hidden layer
        inputMatrix = np.transpose(inputArray).reshape(self.numI, 1)
        hidden = self.wI @ inputMatrix
        hidden += self.biasH
        hidden = numpy.reshape(list(map(self.sigmoid, hidden)), (self.numH, 1))

        # calculate outputs at output layer
        output = self.wO @ hidden
        output += self.biasO
        output = numpy.reshape(list(map(self.sigmoid, output)), (self.numO, 1))

        # calculate output error
        outError = np.transpose(targetArray).reshape(self.numO, 1)
        outError -= output

        #  calculate output gradient
        outGradient = numpy.reshape(list(map(self.dsigmoid, output)), (self.numO, 1))

        outGradient *= outError
        outGradient *= self.lr

        # apply gradient to weights
        hiddenT = np.transpose(hidden)
        WhDelta = outGradient @ hiddenT
        self.wO += WhDelta
        self.biasO += outGradient

        #  calculate hidden error
        WhT = np.transpose(self.wO)
        hiddenError = WhT @ outError

        #  calculate hidden gradient
        hiddenGradient = list(map(self.dsigmoid, hidden))
        hiddenGradient *= hiddenError
        hiddenGradient *= self.lr

        #  apply gradient to weights
        inputT = np.transpose(inputMatrix)
        WiDelta = hiddenGradient @ inputT
        self.wI += WiDelta
        self.biasH += hiddenGradient

        # update trained count
        self.count += 1

    # repeated training of large dataset
    def trainLoop(self, data, reps):
        for i in range(0, reps, 1):
            d: NNData = np.random.choice(data)
            self.train(d.input, d.target)

    def mutate(self, rate, amount):
        r = np.random.rand()
        if r < rate:
            self.wI = self.matMutate(self.wI, amount)
            self.wO = self.matMutate(self.wO, amount)
            self.biasH = self.matMutate(self.biasH, amount)
            self.biasO = self.matMutate(self.biasO, amount)

    # add random variation to weights
    # make a copy of this neural network to a new object
    def copy(self):
        nn = NeuralNetwork(self.numI, self.numH, self.numO, self.lr)
        nn.wI = self.wI.copy()
        nn.wO = self.wO.copy()
        nn.biasH = self.biasH.copy()
        nn.biasO = self.biasO.copy()
        return nn

    # print out the weights
    def print(self):
        print(self.wI)
        print(self.wO)
        print(self.biasH)
        print(self.biasO)
        print()

    # convert to JSON
    def toJSON(self):
        return {
            "numI": self.numI,
            "numH": self.numH,
            "numO": self.numO,
            "lr": self.lr,
            "wI": self.wI.tolist(),
            "wO": self.wO.tolist(),
            "biasH": self.biasH.tolist(),
            "biasO": self.biasO.tolist(),
            "count": self.count
        }

    @staticmethod
    # construct from JSON
    def fromJSON(json):
        nn = NeuralNetwork(1, 1, 1, 1)
        nn.numI = json["numI"]
        nn.numH = json["numH"]
        nn.numO = json["numO"]
        nn.lr = json["lr"]
        nn.wI = np.array(json["wI"])
        nn.wO = np.array(json["wO"])
        nn.biasH = np.array(json["biasH"])
        nn.biasO = np.array(json["biasO"])
        nn.count = json["count"]
        return nn

    @staticmethod
    # sigmoid function for activation
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    @staticmethod
    # d'sigmoid function for back propagation
    def dsigmoid(x):
        return x * (1 - x)

    @staticmethod
    # mutate matrix or array
    def matMutate(mat, amount):
        # add random variance
        def mutate(val, amount):
            return val + np.random.normal(0, amount)
        return np.reshape(list(map(lambda x: mutate(x, amount), mat)), mat.shape)


# Class for organizing inputs and outputs for a dataset
class NNData:
    def __init__(self, inputArray, targetArray, label=None):
        self.input = inputArray
        self.target = targetArray
        self.label = label
