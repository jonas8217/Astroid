from random import randint,random
from math import pi,cos,sin

class astroid:
    def __init__(self,x,y,size):
        self.sqrdt = randint(0,3)
        self.x = 0
        self.y = 0
        self.size = 0
        self.vel = [0.0,0.0]
        dir = random(0.0,2*pi)
        self.vel = [cos(dir),sin(dir)]
        self.vel = self.vel*random(1.0,3)


    def move(self):
        self.x += self.vel[0]
        self.y += self.vel[1]

    def split(self):
        self.size -= 1

        if self.size == 0:
            return 0
        else:
            dir = random(0.0,2*pi)
            self.vel = [cos(dir),sin(dir)]
            self.vel = self.vel*random(1.0,3)
            return self.size


