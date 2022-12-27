import sys
import os
import json
import pygame as pg
import numpy as np
from NeuralNetwork import NeuralNetwork


# game class
class FlappyJuan:
    def __init__(self, size):
        self.w = size  # width
        self.h = size  # height
        self.window = pg.display.set_mode((size, size))  # pygame window
        self.speed = 2  # speed of scrolling
        self.state = 0  # game state: start, playing, game-over
        self.highScore = 0  # high score of run
        self.counted = False  # helper variable for accurate pipe counting
        self.juan = Juan(self)  # player
        self.fileName = "./Resources/BestJuanJson.txt"  # file path for json of weights
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


# player class
class Juan(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()  # pygame sprite constructor
        self.acc = 0  # acceleration
        self.vel = -1  # velocity
        self.angle = 0  # angle
        self.gravity = 0.5  # strength of gravity
        self.flapStrength = 20  # strength of flap
        self.score = 0  # pipes passed
        self.spriteImg = pg.transform.rotozoom(pg.image.load('./Resources/FlappyJuan.png'), 0, 0.3)  # player image
        self.rect = self.spriteImg.get_rect(center=(game.w * 4 / 13, game.h / 4))  # rect.x and .y hold coords of pipe
        self.mask = pg.mask.from_surface(self.spriteImg)  # mask of pipe for collisions
        self.game = game  # instance of flappy juan

    # drawing the player into the scene
    def draw(self, surface):
        surface.blit(pg.transform.rotate(self.spriteImg, self.angle), self.rect)

    # apply force, physics
    def applyForce(self, force):
        self.acc += force

    # moving the player, physics
    def update(self, pipePassed):
        self.applyForce(self.gravity)
        if self.rect.y >= 0:
            self.vel += self.acc
            self.angle = -self.vel * 2
            self.rect.y += self.vel
        else:
            self.rect.y = 0
            self.vel = 0
        self.acc = 0
        if pipePassed:
            self.score += 1

    # apply upward flap force
    def flap(self):
        self.vel = 0
        self.applyForce(-self.flapStrength * self.gravity)

    # test for collision with first pipe
    def collide(self):
        return self.rect.y + self.spriteImg.get_height() > self.game.h or pg.sprite.spritecollide(
            self, pg.sprite.GroupSingle(self.game.nextPipes()[0]), False, pg.sprite.collide_mask)

    # return the score of the juan
    def getScore(self):
        return self.score


# AI class
class JuanAI(Juan):
    def __init__(self, game):
        super().__init__(game)  # Juan class Constructor
        self.spriteImg = self.spriteImg.convert_alpha()  # AI can have transparency
        self.spriteImg.set_alpha(100)
        self.collided = False  # has collided with pipe
        self.fitness = 0  # fitness score, higher = better
        self.brain = NeuralNetwork(8, 12, 2, 0.1)  # brain neural net to determine flaps

    # moving the player, physics
    def update(self, pipePassed):
        if self.collide() or self.collided:
            self.collided = True
            self.rect.x -= self.game.speed
        else:
            self.think()
            if pipePassed:
                self.fitness += 101
            else:
                self.fitness += 1
            super().update(pipePassed)

    # take in inputs: self y, dist from pipe, pipe y, pipe gap
    def think(self):
        pipes = self.game.nextPipes()
        p1, p2 = pipes
        inputs = np.array([[self.rect.y / self.game.h,
                            self.vel / 100,
                            p1.rect.x / self.game.w,
                            (p1.rect.y + (p1.gap / 2)) / self.game.h,
                            (p1.rect.y - (p1.gap / 2)) / self.game.h,
                            p2.rect.x / self.game.w,
                            (p2.rect.y + (p2.gap / 2)) / self.game.h,
                            (p2.rect.y - (p2.gap / 2)) / self.game.h]])
        outputs = self.brain.feedForward(inputs)
        if outputs[0][0] > outputs[0][1]:
            self.flap()

    # mutate for new generation
    def mutate(self, rate, amount):
        self.brain.mutate(rate, amount)

    # convert to JSON
    def toJSON(self):
        return {
            "score": self.score,
            "brain": self.brain.toJSON()
        }

    @staticmethod
    # construct from JSON
    def fromJSON(json, game):
        juan = JuanAI(game)
        juan.brain = NeuralNetwork.fromJSON(json["brain"])
        return juan


# pipe class
class Pipe(pg.sprite.Sprite):
    def __init__(self, x_, y_):
        super().__init__()  # pygame sprite constructor
        self.sarahT = pg.transform.rotozoom(pg.image.load(
            './Resources/PipeySarah.png'), 180, 0.4)  # top pipe image
        self.sarahB = pg.transform.rotozoom(pg.image.load(
            './Resources/PipeySarah.png'), 0, 0.4)  # bottom pipe image
        self.gap = np.random.randint(175, 250)  # gap size between top and bottom
        self.sarah = self.makePipe().convert_alpha()  # combined pipe image
        self.rect = self.sarah.get_rect(center=(x_, y_))  # rect.x and .y hold coords of pipe
        self.mask = pg.mask.from_surface(self.sarah)  # mask of pipe for collisions

    # combines the two pipe images with given gap dist apart
    def makePipe(self):
        pipe = pg.Surface((self.sarahB.get_width(),
                           2 * self.sarahB.get_height() + self.gap),
                          pg.SRCALPHA)
        pipe.blit(self.sarahT, (0, 0))
        pipe.blit(self.sarahB, (0, self.sarahB.get_height() + self.gap))
        return pipe

    # drawing the pipe into the scene
    def draw(self, surface):
        surface.blit(self.sarah, self.rect)

    # moving the pipe
    def update(self, speed):
        self.rect.x -= speed


if __name__ == "__main__":
    # initiate and run
    fj = FlappyJuan(600)
    fj.play()
