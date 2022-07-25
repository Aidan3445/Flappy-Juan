import sys
import pygame as pg
import NeuralNetwork as nn


class XOR:
    def __init__(self):
        self.w = 600
        self.h = 600
        self.res = 10
        self.cols = int(self.w / self.res)
        self.rows = int(self.h / self.res)
        self.net = nn.NeuralNetwork(2, 5, 1, 0.1)
        self.data = [
            nn.NNData([1.0, 0.0], [1.0]),
            nn.NNData([0.0, 1.0], [1.0]),
            nn.NNData([1.0, 1.0], [0.0]),
            nn.NNData([0.0, 0.0], [0.0])
        ]


def run(world: XOR):
    window = pg.display.set_mode((world.w, world.h))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        for i in range(0, world.cols, 1):
            for j in range(0, world.rows, 1):
                x1 = i / world.cols
                x2 = j / world.rows
                inputArray = [x1, x2]
                y = int(world.net.feedForward(inputArray) * 255)
                pg.draw.rect(window, (y, y, y),
                             pg.Rect(i * world.res, j * world.res, world.res, world.res))

        font = pg.font.SysFont(None, 24)
        trainCount = font.render(str(world.net.count) + " Trained", True, (255, 0, 0))
        center = trainCount.get_rect(center=(world.w / 2, world.h / 2))
        window.blit(trainCount, center)
        pg.display.update()
        world.net.trainLoop(world.data, 1000)


xor = XOR()
pg.init()
pg.font.init()
run(xor)
