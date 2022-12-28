import numpy as np

from Juan import Juan
from NeuralNetwork import NeuralNetwork


# AI class
class JuanAI(Juan):
    def __init__(self, game):
        super().__init__(game)  # Juan class Constructor
        self.spriteImg = self.spriteImg.convert_alpha()  # AI can have transparency
        self.spriteImg.set_alpha(100)
        self.collided = False  # has collided with pipe
        self.fitness = 1  # fitness score, higher = better
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
