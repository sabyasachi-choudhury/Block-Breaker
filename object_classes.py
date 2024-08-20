import pygame
from pygame.locals import *

# Width and height
s_width = 700
s_height = 800

# Block dims
b_width = 96
b_height = 26


# Block white
class BlueBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BlueBlock, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("BlueBlock.jpg").convert(), (b_width, b_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.id = 'BB'


# Red Block
class RedBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(RedBlock, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("RedBlock.jpg").convert(), (b_width, b_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.id = 'RB'


# Yellow Block
class YellowBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(YellowBlock, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("YellowBlock.jpg").convert(), (b_width, b_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.id = 'YB'


# Grey Block
class GreenBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(GreenBlock, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("GreenBlock.jpg").convert(), (b_width, b_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.id = 'GB'


# Immovable block
class Immovable(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Immovable, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("block_tiles_blue.png").convert(), (b_width, 2 * b_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.id = 'IM'


# Paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super(Paddle, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("Paddle.png").convert(), (int(1.5 * b_width), b_height))
        self.rect = self.image.get_rect(center=(s_width / 2, s_height - 70))
        self.image.set_colorkey((255, 255, 255))
        self.id = 'PD'

    def paddle_motion(self, press, speed):
        if press[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if press[K_RIGHT]:
            self.rect.move_ip(speed, 0)

        if self.rect.right > s_width:
            self.rect.right = s_width
        elif self.rect.left < 0:
            self.rect.left = 0


# Ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("breakout ball.png").convert(), (b_height, b_height))
        self.rect = self.image.get_rect(center=(s_width / 2, s_height - 105))
        self.image.set_colorkey((255, 255, 255, 255))
        self.id = 'BALL'


# BG for extra screens
class ExtraBG(pygame.sprite.Sprite):
    def __init__(self, w, h, a, b, c):
        super(ExtraBG, self).__init__()
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect(center=(s_width / 2, -s_height / 2))
        self.image.fill((a, b, c))


# Hearts
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Heart, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("heart pixel art 48x48.png").convert(), (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        og_surf = self.image
        self.image = pygame.transform.rotate(og_surf, 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.set_colorkey((0, 0, 0))


# End screen
class EndBG(pygame.sprite.Sprite):
    def __init__(self):
        super(EndBG, self).__init__()
        self.image = pygame.Surface((s_width, s_height))
        self.rect = self.image.get_rect(center=(s_width / 2, -0.5 * s_height))
        self.image.fill((255, 144, 41))


# Retry button
class Retry(pygame.sprite.Sprite):
    def __init__(self):
        super(Retry, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("Retry.png").convert(), (220, 100))
        self.rect = self.image.get_rect(center=(s_width / 2, 280))


# Moving block
class Moving(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Moving, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("MovingBlock.png").convert(), (b_width, b_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.id = 'MB'
        self.vel = 1

    def motion(self):
        self.rect.move_ip(self.vel, 0)
        if self.rect.right > 700 or self.rect.left < 0:
            self.vel = -self.vel