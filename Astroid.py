from random import randint,random
from math import pi,cos,sin

class astroid:
    def __init__(self,x,y,size = randint(1,3)):
        self.sqrdt = randint(0,3)
        self.x = x
        self.y = y
        self.size = size
        self.vel = [0.0,0.0]
        dir = random()*2*pi
        self.vel = [cos(dir),sin(dir)]
        sp = mapFromTo(random(),0.0,1.0,1.0,3)
        self.vel[0] = self.vel[0]*sp
        self.vel[1] = self.vel[1]*sp


    def move(self):
        self.x += self.vel[0]
        self.y += self.vel[1]

    def split(self):
        self.size -= 1

        if self.size == 0:
            return None
        else:
            dir = random()*2*pi
            self.vel = [cos(dir),sin(dir)]
            sp = mapFromTo(random(),0.0,1.0,1.0,2.0)
            self.vel[0] = self.vel[0]*sp
            self.vel[1] = self.vel[1]*sp
            a = astroid(self.x,self.y,self.size)
            return a

def mapFromTo(x,a,b,c,d):
        y = (x-a)/(b-a)*(d-c)+c
        return y


