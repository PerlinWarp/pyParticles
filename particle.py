import random
import pygame
import numpy as np

from settings import w_width, w_height, friction


class Particle():
    def __init__(self,typ,c):
        self.type = typ
        self.c = c

        self.r = 5
        self.pos = np.array([random.randint(self.r, w_width-self.r)
                            ,random.randint(self.r, w_height-self.r)],dtype='float64')
        self.vel = np.random.randint(-2,2,size=2)
        self.acc = np.zeros(2)

    def __repr__(self):
        return "Pos: " + str(self.pos) +"\n"+ "Vel: " + str(self.vel)

    def run(self,screen):
        self.draw(screen)

    def draw(self,screen):
        pygame.draw.circle(screen, self.c, self.pos.astype(int), self.r)


class PlayerParticle(Particle):
    def __init__(self):
        self.c = (255,255,255)
        super().__init__(0,self.c)

    def run(self, screen):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.acc[1] += 1
        if pressed[pygame.K_DOWN]: self.acc[1] -= 1
        if pressed[pygame.K_LEFT]: self.acc[0] -= 1
        if pressed[pygame.K_RIGHT]: self.acc[0] += 1
        super().run(screen)


class Population():
    def __init__(self, screen):
        self.types = 4
        self.size = 10
        self.screen = screen
        self.particles = [PlayerParticle()]

        self.rules = {}
        # Generate the rules
        for t in range(self.types):
            min_r = random.randint(0,4)
            max_r = random.randint(0,4)
            attr = random.randint(-2,2)
            self.rules[t] = [min_r, max_r, attr]

        # Generate the properties of our classes
        for i in range(self.types):
            c = (random.randint(20,255),random.randint(20,255),random.randint(20,255))

            for j in range(self.size):
                self.particles.append(Particle(i,c))

    def interactions(self):
        '''
        Applying all the rules to the particles
        '''
        for i in self.particles:
            for j in self.particles:
                # Get distance between particles
                d = np.linalg.norm(i.pos-j.pos)

                if (d > 2):
                    # The max interaction distance
                    continue
                if (d < i.r):
                    i.acc = 2






    def run(self):
        self.interactions()

        for p in self.particles:
            p.vel = p.vel + p.acc

            # Apply friction
            #p.vel = p.vel * (1.0 - friction)
            p.acc = np.zeros(2)

            p.pos = p.pos + p.vel

            # Sanity checks
            p.pos[0] = p.pos[0]%(w_width - p.r)
            p.pos[1] = p.pos[1]%(w_height - p.r)

            # Draw the particles 
            p.run(self.screen)

