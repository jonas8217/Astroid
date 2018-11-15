import pygame
from math import pi,cos,sin,sqrt
from random import randint,random
from Astroid import astroid
from Projectile import projectile


class Game:
        def __init__(self):
                self.state = 0
                #State 0: Menu
                #State 1: Game
                #State 2: Pause
                self.spd = 0.0
                self.ro = 0
                self.x = 400
                self.y = 300
                self.points = 0
                self.vel = [0.0,0.0]
                self.astr = []
                self.pjct = []
                self.notp = True
                #self.ship_point_list = 

                

                self.astr.append(astroid(100,100,3))
                self.astr.append(astroid(100,100,1))
                self.astr.append(astroid(100,100,2))


        def tick(self, pg, pressed):
                if self.state == 1:
                        
                        #controls
                        if pressed[pg.K_UP] and self.spd < 5:
                                self.spd += 0.4
                        if pressed[pg.K_DOWN] and self.spd > 0:
                                self.spd -= 0.1
                        if self.spd < 0:
                                self.spd = 0
                        if pressed[pg.K_LEFT]:
                                self.ro -= 4
                        if pressed[pg.K_RIGHT]:
                                self.ro += 4
                        
                        if pressed[pg.K_SPACE] and self.notp:
                                self.notp = False
                                shoot(self.pjct,self.x,self.y,self.ro)
                        elif not pressed[pg.K_SPACE]:
                                self.notp = True

                        #ship_movement_de-acc
                        self.spd *= 0.99
                        
                        #ship_movement_calc
                        dir = mapFromTo(self.ro,0,360,0.0,2*pi)
                        self.vel = [cos(dir)*self.spd,sin(dir)*self.spd]
                        #print(self.vel)

                        #movement_execution
                        self.x += self.vel[0]
                        self.y += self.vel[1]
                        move_astroids(self.astr)
                        move_projectiles(self.pjct)

                        #ship_rotation


                        #looping
                        ##player
                        if self.x < 10:
                                self.x = float(790)
                        elif self.x > 790:
                                self.x = float(10)
                        if self.y < 10:
                                self.y = float(590)
                        elif self.y > 590:
                                self.y = float(10)

                        ##astroids
                        for i in range(len(self.astr)):
                                if self.astr[i].x < 10:
                                        self.astr[i].x = float(790)
                                elif self.astr[i].x > 790:
                                        self.astr[i].x = float(10)
                                if self.astr[i].y < 10:
                                        self.astr[i].y = float(590)
                                elif self.astr[i].y > 590:
                                        self.astr[i].y = float(10)
                        ##projectiles
                        for i in range(len(self.pjct)):
                                if self.pjct[i].x < 10:
                                        self.pjct[i].x = float(790)
                                elif self.pjct[i].x > 790:
                                        self.pjct[i].x = float(10)
                                if self.pjct[i].y < 10:
                                        self.pjct[i].y = float(590)
                                elif self.pjct[i].y > 590:
                                        self.pjct[i].y = float(10)
                        
                        #delete_projectieles
                        plist = []
                        for i in range(len(self.pjct)):
                                if vec_length(self.pjct[i].vel) < 0.1:
                                        plist.append(i)
                        for i in range(len(plist)):
                                del plist[i]
                                del self.pjct[i]        

                        #collision
                        self.hit(self.pjct,self.astr)


                        


        def hit(self,p,a):
                plist = []
                alist = []
                if len(p)*len(a) > 0:
                        for i in range(0,len(p)):
                                for j in range(0,len(a)):
                                        if dist(p[i].x,a[j].x,p[i].y,a[j].y) < a[j].size*10:
                                                plist.append(i)
                                                split_a = a[j].split()
                                                if split_a != None:
                                                        a.append(split_a)
                                                else:
                                                        alist.append(j)
                for i in plist:
                        del self.pjct[i]
                        for j in range(len(plist)-1):
                                del plist[j]
                for i in alist:
                        del self.astr[i]
                        for j in range(len(alist)-1):
                                del alist[j]
        
        def collision(self):
                pass


        def start_game(self):
                if self.state == 0:
                        self.state = 1
                        self.points = 0

        def end_game(self):
                if self.state > 0:
                        self.state = 0

        def toggle_pause(self):
                if self.state == 1:
                        self.state = 2
                else:
                        self.state = 1

        def started(self):
                if self.state > 0:
                        return True
                else:
                        return False

def move_astroids(a):
        for i in range(len(a)):
                a[i].move()

def move_projectiles(p):
        for i in range(len(p)):
                p[i].move()

def shoot(p,x,y,ro):
        dir = mapFromTo(ro,0,360,0.0,2*pi)
        vel = [cos(dir)*4,sin(dir)*4]
        p.append(projectile(x,y,vel))


def mapFromTo(x,a,b,c,d):
        y = (x-a)/(b-a)*(d-c)+c
        return y

def dist(x1,x2,y1,y2):
        d = sqrt(((x1-x2)**2)+((y1-y2)**2))
        return d

def vec_length(vec):
        l = sqrt(vec[0]**2+vec[1]**2)
        return l

"""
def Ship_pointlist(ro):
        A = 
        B = (-5,5)
        C = (10,0)
"""



def draw_game():
        if game.state == 0:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(380, 280, 80, 50))
                screen.blit(myfont.render("MENU", 1, (255, 255, 255)), (400, 300))
        elif game.state == 1:
                screen.fill((0, 10, 20))
                #pygame.transform.rotate(screen, game.ro % 360)
                pygame.draw.polygon(screen, (255,255,255), [(-5,-5),(-5,5),(10,0)], 1)

                if len(game.astr) > 0:
                        for i in range(len(game.astr)):
                                pygame.draw.circle(screen, (255, 255, 255), (int(game.astr[i].x), int(game.astr[i].y)), game.astr[i].size*10, 2)
                if len(game.pjct) > 0:
                        for i in range(len(game.pjct)):
                                pygame.draw.circle(screen, (255, 255, 255), (int(game.pjct[i].x), int(game.pjct[i].y)), 1, 0)
                screen.blit(myfont.render("Points: {}".format(game.points), 1, (255, 255, 0)), (100, 100))
        elif game.state == 2:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(380, 280, 80, 50))
                screen.blit(myfont.render("PAUSE", 1, (255, 255, 255)), (400, 300))


pygame.init()
screen = pygame.display.set_mode((800, 600))
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)

done = False

game = Game()

clock = pygame.time.Clock()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game.toggle_pause()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if game.started():
                                game.end_game()
                        else:
                                game.start_game()

        pressed = pygame.key.get_pressed()

        game.tick(pygame, pressed)
        draw_game()

        pygame.display.flip()
        clock.tick(60)
