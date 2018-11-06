from math import pi,cos,sin

class projectile:
    def __init__(self,x,y,vel):
        self.x = x
        self.y = y
        self.vel = vel

    def move(self):
        self.x += self.vel[0]
        self.y += self.vel[1]