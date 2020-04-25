import pygame
import numpy as np
import random

from settings import w_width, w_height
import particle as P

pygame.init()
screen = pygame.display.set_mode((w_width, w_height))
done = False
clock = pygame.time.Clock()
        
population = P.Population(screen)

while not done:
        clock.tick(60) # Cap the frame rate
        screen.fill((0,0,0))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        # Run the particles
        population.run()

        pygame.display.flip()

