import pygame as pg


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
        self.spriteImg = pg.transform.rotozoom(pg.image.load(
            'Resources/FlappyJuan.png'), 0, 0.3)  # player image
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
