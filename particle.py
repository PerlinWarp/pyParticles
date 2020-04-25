import random
import pygame
import numpy as np

from settings import w_width, w_height, friction


class Particle():
    def __init__(self):
        self.pos = np.array([300,400])
        self.vel = np.random.randint(-2,2,size=2)
        self.acc = np.zeros(2)
        self.r = 5
        self.c = (255,20,20)

    def __repr__(self):
        return "Pos: " + str(self.pos) +"\n"+ "Vel: " + str(self.vel)

    def update(self):
        self.vel = self.vel + self.acc

        # Apply friction
        self.vel *= (1.0 - friction)
        self.acc = np.zeros(2)

        self.pos = self.pos + self.vel

        # Sanity checks
        self.pos[0] = self.pos[0]%(w_width - self.r)
        self.pos[1] = self.pos[1]%(w_height - self.r)

    def draw(self,screen):
        pygame.draw.circle(screen, self.c, self.pos.astype(int), self.r)


class PlayerParticle(Particle):
    def __init__(self):
        super().__init__()
        self.c = (255,255,255)

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.acc[1] += 1
        if pressed[pygame.K_DOWN]: self.acc[1] -= 1
        if pressed[pygame.K_LEFT]: self.acc[0] -= 1
        if pressed[pygame.K_RIGHT]: self.acc[0] += 1
        super().update()
