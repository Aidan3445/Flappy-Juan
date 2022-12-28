import sys
import os
import json
import pygame as pg
import numpy as np

from Juan import Juan
from JuanAI import JuanAI
from Pipe import Pipe


# game class
class FlappyJuan:
    def __init__(self, size, fileName=None):
        self.w = size  # width
        self.h = size  # height
        self.window = pg.display.set_mode((size, size))  # pygame window
        self.speed = 2  # speed of scrolling
        self.state = 0  # game state: start, playing, game-over
        self.highScore = 0  # high score of run
        self.counted = False  # helper variable for accurate pipe counting
        self.juan = Juan(self)  # player
        if fileName is None:
            self.fileName = "./Resources/BestJuanJson.txt"
        else:
            self.fileName = fileName  # file path for json of weights
        self.bestEver = self.loadJuan()  # load AI juan from the given file path
        self.showBest = False  # whether to draw the AI Juan
        self.sarahs = [Pipe(self.w,
                            np.random.randint(150, 450)),
                       Pipe(self.w + 300,
                            np.random.randint(150, 450)),
                       Pipe(self.w + 600,
                            np.random.randint(150, 450))]  # obstacles

    # reset game
    def reset(self):
        self.counted = False
        self.juan = Juan(self)
        self.bestEver = self.loadJuan()
        self.sarahs = [Pipe(self.w,
                            np.random.randint(150, 450)),
                       Pipe(self.w + 300,
                            np.random.randint(150, 450)),
                       Pipe(self.w + 600,
                            np.random.randint(150, 450))]

    # load juan from file
    def loadJuan(self):
        if os.path.exists(self.fileName):
            with open(self.fileName) as f:
                data = json.load(f)
            return JuanAI.fromJSON(data, self)
        return False

    # update player, obstacles, and score
    def update(self):
        pipePassed = False
        if self.juan.collide():
            self.state = 2
        for sarah in self.sarahs:
            sarah.update(self.speed)
        if self.nextPipes()[0] != self.sarahs[0] and not self.counted:
            pipePassed = True
            self.counted = True
        if self.sarahs[0].rect.x < -100:
            self.sarahs.pop(0)
            self.sarahs.append(Pipe(self.w + 254, np.random.randint(150, 450)))
            self.counted = False
        self.juan.update(pipePassed)
        if self.bestEver:
            self.bestEver.update(pipePassed)
        else:
            self.showBest = False
        return pipePassed

    # returns closest 2 pipes in front of the player
    def nextPipes(self):
        closestIndex = None
        closestDist = float('inf')
        for i in range(len(self.sarahs)):
            sarah = self.sarahs[i]
            d = sarah.rect.x - (self.w * 4 / 13)
            if closestDist > d > - sarah.sarah.get_width():
                closestIndex = i
                closestDist = d
        return [self.sarahs[closestIndex], self.sarahs[closestIndex + 1]]

    # draw and display game
    def draw(self):
        self.window.fill('white')
        font = pg.font.SysFont(None, 30)
        text = font.render("Score: " + str(self.juan.getScore()), True, 'red')
        align = text.get_rect(topleft=(10, 10))
        self.window.blit(text, align)
        text = font.render("High Score: " + str(self.highScore), True, 'red')
        align = text.get_rect(topleft=(10, 40))
        self.window.blit(text, align)
        if self.showBest:
            self.bestEver.draw(self.window)
        self.juan.draw(self.window)
        for sarah in self.sarahs:
            sarah.draw(self.window)

    # display start screen
    def startScreen(self):
        self.window.fill('white')
        font = pg.font.SysFont(None, 50)
        text = font.render("SPACE BAR TO PLAY", True, 'black')
        textCenter = text.get_rect(center=(self.w / 2, self.h * 2 / 3))
        self.window.blit(text, textCenter)
        font = pg.font.SysFont(None, 25)
        text = font.render("PRESS ENTER TO TOGGLE GHOST", True, 'gray')
        textCenter = text.get_rect(center=(self.w / 2, self.h * 5 / 6))
        self.window.blit(text, textCenter)

    # display end screen
    def endScreen(self):
        self.startScreen()
        font = pg.font.SysFont(None, 50)
        endText = font.render("GAME OVER", True, 'red')
        endCenter = endText.get_rect(center=(self.w / 2, self.h / 3))
        self.window.blit(endText, endCenter)
        scoreText = font.render(str(self.juan.getScore()), True, 'red')
        scoreCenter = scoreText.get_rect(center=(self.w / 2, self.h / 2))
        self.window.blit(scoreText, scoreCenter)

    # methods to run every frame
    def onTick(self):
        if self.state == 1:
            self.update()
            self.draw()
        elif self.state == 0:
            self.startScreen()
        else:
            self.endScreen()

    # pygame run loop
    def play(self):
        pg.init()
        pg.font.init()
        while True:
            self.highScore = max(self.juan.score, self.highScore)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.showBest ^= 1
                    if event.key == pg.K_SPACE:
                        if self.state == 1:
                            self.juan.flap()
                        else:
                            self.state = 1
                            self.reset()
            self.onTick()
            pg.display.update()
            pg.time.Clock().tick(60)
