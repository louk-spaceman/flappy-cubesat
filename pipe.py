import pygame
import random

class Pipe:
    def __init__(self, WIDTH: int, HEIGHT: int, score: int):
        self.x = WIDTH + 50
        self.y_gap = int(HEIGHT/2 - (score/69)*(HEIGHT/2))
        self.top_height = random.randint(75,HEIGHT-self.y_gap-75)
        self.bottom_height = HEIGHT - self.top_height - self.y_gap
        self.speed = WIDTH/50
        self.scored = False

    def off_screen(self):
        return self.x < -100

    def update(self, WIDTH: int, HEIGHT: int):
        pipe_width = int(WIDTH/20)
        self.x -= self.speed
        self.top_rect = pygame.Rect(self.x, 0, pipe_width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, HEIGHT - self.bottom_height, pipe_width, self.bottom_height)
        self.top_invisible_rect = pygame.Rect(self.x, -100000, pipe_width, 100000)
        self.bottom_invisible_rect = pygame.Rect(self.x, HEIGHT, pipe_width, 100000)

    def collision(self, cubesat):
        if cubesat.rect.colliderect(self.top_rect) or cubesat.rect.colliderect(self.bottom_rect) or cubesat.rect.colliderect(self.top_invisible_rect) or cubesat.rect.colliderect(self.bottom_invisible_rect):
            return True
        return False