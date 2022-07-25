import time

import math
import numpy
import numpy as np

# Neural network class with one hidden layer
class NeuralNetwork:
    def __init__(self, inputNum, hiddenNum, outputNum, learningRate):
        self.numI = inputNum # number of inputs
        self.numH = hiddenNum # number of hidden layer nodes
        self.numO = outputNum # number of outputs
        self.lr = learningRate # learning rate of the nueral net
        self.wI = np.random.randn(hiddenNum, inputNum) # create input weights array
        self.wO = np.random.randn(outputNum, hiddenNum) # create hidden layer weights array
        self.biasH = np.random.randn(hiddenNum, 1) # create hidden weights bias
        self.biasO = np.random.randn(outputNum, 1) # create output weights bias
        self.count = 0 # counter for keying track of the number of datasets passed through

    # get output from a given input array
    def feedForward(self, inputArray):
        # calculate outputs at hidden layer
        inputMatrix = np.transpose(inputArray).reshape(self.numI, 1)
        hidden = np.dot(self.wI, inputMatrix)
        hidden += self.biasH
        hidden = numpy.reshape(list(map(sigmoid, hidden)), (self.numH, 1))

        # calculate outputs at output layer
        output = np.dot(self.wO, hidden)
        output += self.biasO
        output = numpy.reshape(list(map(sigmoid, output)), (self.numO, 1))

        # transpose back into array
        output = np.transpose(output)
        return output

    # updates nodes based on input dataset and expected output
    def train(self, inputArray, targetArray):
        # calculate outputs at hidden layer
        inputMatrix = np.transpose(inputArray).reshape(self.numI, 1)
        hidden = self.wI @ inputMatrix
        hidden += self.biasH
        hidden = numpy.reshape(list(map(sigmoid, hidden)), (self.numH, 1))

        # calculate outputs at output layer
        output = self.wO @ hidden
        output += self.biasO
        output = numpy.reshape(list(map(sigmoid, output)), (self.numO, 1))

        # calculate output error
        outError = np.transpose(targetArray).reshape(self.numO, 1)
        outError -= output

        #  calculate output gradient
        outGradient = numpy.reshape(list(map(dsigmoid, output)), (self.numO, 1))

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
        hiddenGradient = list(map(dsigmoid, hidden))
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
            
    # make a copy of this nueral network to a new object
    def copy(self):
        nn = NeuralNetwork(self.numI, self.numH, self.numO, self.lr)
        nn.wI = self.wI.copy()
        nn.wO = self.wO.copy()
        nn.biasH = self.biasH.copy()
        nn.biasO = self.biasO.copy()
        return nn
    
    # add random variation to weights
    def mutate(self, rate, amount):
        r = np.random.rand()
        if r < rate:
            self.wI = matMutate(self.wI, amount)
            self.wO = matMutate(self.wO, amount)
            self.biasH = matMutate(self.biasH, amount)
            self.biasO = matMutate(self.biasO, amount)
    
    # print out the weights
    def print(self):
        print(self.wI)
        print(self.wO)
        print(self.biasH)
        print(self.biasO)
        print()


# Class for organizing inputs and outputs for a dataset
class NNData:
    def __init__(self, inputArray, targetArray, label=None):
        self.input = inputArray
        self.target = targetArray
        self.label = label


# sigmoid function for activation        
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# d'sigmoid function for back propigation
def dsigmoid(x):
    return x * (1 - x)

# add random variance
def mutate(x, amount):
    return x + np.random.normal(0, amount)

# mutate matrix or array
def matMutate(mat, amount):
    m = lambda x : mutate(x, amount)
    return np.reshape(list(map(m, mat)), mat.shape)


# testing
    
# start_time = time.time()
# testArray = [0.0, 1.0]
# targetArray = [1.0]
# testNN = NeuralNetwork(2, 5, 1, 0.1)
# print(testNN.feedForward(testArray))
# testNN.train(testArray, targetArray)
# print(testNN.feedForward(testArray))
# print("--- %s seconds ---" % (time.time() - start_time))
