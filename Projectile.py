

class projectile:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel

    def move(self):
        self.vel[0] *= 0.995
        self.vel[1] *= 0.995
        self.x += self.vel[0]
        self.y += self.vel[1]
