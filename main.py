import pygame
import numpy as np
import random

from settings import w_width, w_height
import particle as P

pygame.init()
screen = pygame.display.set_mode((w_width, w_height))
done = False


p = P.Particle()
pl = P.PlayerParticle()

particles = [p,pl]
clock = pygame.time.Clock()
        
print(p)

while not done:
        clock.tick(60) # Cap the frame rate
        screen.fill((0,0,0))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        for p in particles:
            p.update()
            p.draw(screen)

        pygame.display.flip()

