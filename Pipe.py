import numpy as np
import pygame as pg


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
