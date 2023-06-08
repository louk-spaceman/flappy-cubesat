import pygame

class Cubesat:
    def __init__(self, WIDTH: int, HEIGHT: int):
        cubesat_width = int(HEIGHT/10)
        self.x = int(WIDTH/30)
        self.y = int(HEIGHT/2)
        self.velocity = -HEIGHT/73
        self.gravity = HEIGHT/2000
        self.width = cubesat_width
        self.height = cubesat_width

    def flap(self, HEIGHT: int):
        self.velocity = int(-HEIGHT/73)
        #sound_effect.play()

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)