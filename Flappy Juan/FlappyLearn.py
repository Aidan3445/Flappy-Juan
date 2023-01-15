import sys
import os
import json
import pygame as pg
import numpy as np

from FlappyJuan import FlappyJuan
from JuanAI import JuanAI


# game class
class FlappyLearn(FlappyJuan):
    def __init__(self, size, popSize, fileName=None, mutateRate=None, mutateAmount=None, cont=False):
        super().__init__(size, fileName)
        if mutateRate is None:
            self.mutateRate = 0.25
        else:
            self.mutateRate = mutateRate  # rate of mutation between generations
        if mutateAmount is None:
            self.mutateAmount = 0.1
        else:
            self.mutateAmount = mutateAmount  # amount of mutation between generations
        self.runSpeed = 1
        self.popSize = popSize  # size of each generation
        self.gen = 0  # generation number
        self.numAlive = popSize  # number of juans that are not collided, starts at full pop
        if cont:
            self.loadPop()
        else:
            self.juans = self.generatePopulation()  # list of birds in current population

    # reset game
    def reset(self):
        super().reset()
        self.gen += 1
        self.juans = self.generatePopulation(self.juans)

    # make new random population
    def generatePopulation(self, prev=None):
        pop = []
        if prev is None:
            for i in range(self.popSize):
                pop.append(JuanAI(self))
        else:
            total = 0
            for juan in prev:
                total += juan.fitness
            for juan in prev:
                juan.fitness /= total
            for i in range(self.popSize):
                pop.append(self.pickChild(prev))
        return pop

    # picks child from a population based on fitness
    def pickChild(self, pop):
        index = 0
        r = np.random.rand()
        while r > 0:
            r = r - pop[index].fitness
            index += 1
        index -= 1
        parentJson = pop[index].toJSON()
        child = JuanAI.fromJSON(parentJson, self)
        child.mutate(self.mutateRate, self.mutateAmount)
        return child

    # load a population of children of the best ever
    def loadPop(self):
        savedMutateRate = self.mutateRate
        self.mutateRate = 1  # guarantee mutation
        pop = []
        for i in range(self.popSize):
            pop.append(self.loadJuan())
        self.juans = self.generatePopulation(pop)
        self.mutateRate = savedMutateRate  # reset rate

    # update player, obstacles, and score
    def update(self):
        pipePassed = super().update()
        self.numAlive = self.popSize
        for juan in self.juans:
            juan.update(pipePassed)
            if juan.collided:
                self.numAlive -= 1
        if self.numAlive == 0 and (not self.showBest or self.bestEver.collided):
            self.reset()
        return pipePassed

    # draw and display game
    def draw(self):
        self.window.fill('white')
        font = pg.font.SysFont(None, 30)
        text = font.render("Score: " + str(self.getScore()), True, 'red')
        align = text.get_rect(topleft=(10, 10))
        self.window.blit(text, align)
        text = font.render("High Score: " + str(self.highScore), True, 'red')
        align = text.get_rect(topleft=(10, 40))
        self.window.blit(text, align)
        text = font.render("Generation: " + str(self.gen), True, 'red')
        align = text.get_rect(topleft=(10, 70))
        self.window.blit(text, align)
        text = font.render("Alive: " + str(self.numAlive), True, 'red')
        align = text.get_rect(topleft=(10, 100))
        self.window.blit(text, align)
        self.bestEver.draw(self.window)  # draw best juan
        if not self.showBest:
            for juan in self.juans:  # draw all juans
                juan.draw(self.window)
        for sarah in self.sarahs:
            sarah.draw(self.window)

    # methods to run every frame
    def onTick(self):
        for i in range(self.runSpeed):
            self.update()
        self.draw()

    # pygame run loop
    def play(self):
        pg.init()
        pg.font.init()
        clock = pg.time.Clock()
        while True:
            score = self.getScore()
            if score > self.highScore and self.numAlive > 0:
                self.highScore = score
                self.saveJuan()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.saveJuan()
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:  # toggle showing the best only or all
                        self.showBest ^= 1  # best only runs significantly smoother
                    if event.key == pg.K_RETURN:
                        self.reset()
                    # speed up and slow down generations
                    elif event.key == pg.K_1:
                        self.runSpeed = 1
                    elif event.key == pg.K_2:
                        self.runSpeed = 5
                    elif event.key == pg.K_3:
                        self.runSpeed = 20
                    elif event.key == pg.K_4:
                        self.runSpeed = 100
            self.onTick()
            pg.display.update()
            clock.tick()

    # save high score to json if the current high score is higher than the saved one
    def saveJuan(self):
        newScore = True
        if os.path.exists(self.fileName):
            with open(self.fileName, "r") as f:
                newScore = newScore and self.highScore > json.load(f)["score"]
        else:
            with open(self.fileName, "w") as f:
                juanInfo = JuanAI(self).toJSON()
                json.dump(juanInfo, f)
        if newScore:
            maxFitness = 0
            maxJuan = None
            for juan in self.juans:
                if juan.fitness > maxFitness:
                    maxFitness = juan.fitness
                    maxJuan = juan
            self.writeJsonJuan(maxJuan)

    # writes given juan to json file
    def writeJsonJuan(self, maxJuan):
        juanInfo = maxJuan.toJSON()
        with open(self.fileName, "w") as f:
            json.dump(juanInfo, f)

    # load juan from file
    def loadJuan(self):
        if not os.path.exists(self.fileName):
            with open(self.fileName, "w") as f:
                juanInfo = JuanAI(self).toJSON()
                json.dump(juanInfo, f)
        with open(self.fileName) as f:
            data = json.load(f)
        return JuanAI.fromJSON(data, self)

    def getScore(self):
        best = self.bestEver
        if not best.collided:
            return best.getScore()
        for juan in self.juans:
            if not juan.collided:
                return juan.getScore()
        return 0
