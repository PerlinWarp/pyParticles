import random
import pygame
import numpy as np

from settings import w_width, w_height, FRICTION, RADIUS, DIAMETER


class Particle():
    def __init__(self,typ,c):
        self.type = typ
        self.c = c
        self.pos = np.array([random.randint(RADIUS, w_width-RADIUS)
                            ,random.randint(RADIUS, w_height-RADIUS)],dtype='float64')
        self.vel = np.random.randint(-2,2,size=2)
        self.acc = np.zeros(2)

    def __repr__(self):
        return "Pos: " + str(self.pos) +"\n"+ "Vel: " + str(self.vel)

    def run(self,screen):
        self.draw(screen)

    def draw(self,screen):
        pygame.draw.circle(screen, self.c, self.pos.astype(int), RADIUS)


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
        self.types = 5
        self.size = 20
        self.screen = screen
        self.particles = [PlayerParticle()]

        min_r_lower = 0
        min_r_upper = 20
        max_r_lower = 20
        max_r_upper = 70

        # Generate the rules
        self.rules = [[0]*self.types for i in range(self.types)]
        # Generate the rules
        for i in range(self.types):
            for j in range(self.types):    
                if (i<j):       
                    min_r = max(random.randint(min_r_lower,min_r_upper),DIAMETER)
                    max_r = max(random.randint(max_r_lower,max_r_upper),min_r)
                    attr = random.randint(-2,2)
                    self.rules[i][j] = [min_r, max_r, attr]
                elif (i == j):
                    min_r = DIAMETER
                    max_r = max(random.randint(max_r_lower, max_r_upper),min_r)
                    attr = random.randint(-2,2)
                    self.rules[i][j] = [min_r, max_r, attr]
                else:
                    self.rules[i][j] = self.rules[j][i]

        # Generate the properties of our classes
        for i in range(self.types):
            c = (random.randint(20,255),random.randint(20,255),random.randint(20,255))

            for j in range(self.size):
                self.particles.append(Particle(i,c))

    def interactions(self):
        '''
        Applying all the rules to the particles
        '''
        r_smooth = 2

        for i in self.particles:
            for j in self.particles:
                min_r = self.rules[i.type][j.type][0]
                max_r = self.rules[i.type][j.type][1]
                attr = self.rules[i.type][j.type][2]

                # Get distance between particles
                d = i.pos - j.pos

                r = np.linalg.norm(d)
                if (r > max_r or r < 0.01):
                    continue

                d = d / r 
                # Calculate force
                if r  > min_r:
                    numer = 2.0 * abs(r - 0.5*(max_r + min_r))
                    denom = max_r - min_r
                    f = attr * (1 - numer/denom)
                else:
                    f = r_smooth*min_r*(1.0/(min_r + r_smooth) - 1.0/(r+r_smooth))

                i.vel = i.vel + f*d



    def run(self):
        self.interactions()

        for p in self.particles:
            p.vel = p.vel + p.acc

            # Apply friction
            p.vel = p.vel * (1-FRICTION)
            p.acc = np.zeros(2)

            p.pos = p.pos + p.vel

            # Sanity checks
            p.pos[0] = p.pos[0]%(w_width - RADIUS)
            p.pos[1] = p.pos[1]%(w_height - RADIUS)

            # Draw the particles 
            p.run(self.screen)

