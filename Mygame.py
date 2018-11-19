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
                self.counter = 0

                

                self.astr.append(astroid(100,100,3))
                self.astr.append(astroid(400,100,1))
                self.astr.append(astroid(700,100,2))
                self.astr.append(astroid(100,500,3))
                self.astr.append(astroid(400,500,1))
                self.astr.append(astroid(700,500,2))


        def tick(self, pg, pressed):
                if self.state == 1:
                        
                        #ship_movement_calc
                        dir = mapFromTo(self.ro,0,360,0.0,2*pi)

                        #controls
                        if pressed[pg.K_UP] and vec_length(self.vel) < 8:
                                self.vel[0] += cos(dir)*0.2
                                self.vel[1] += sin(dir)*0.2
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
                        self.vel[0] *= 0.985
                        self.vel[1] *= 0.985
                        

                        #movement_execution
                        self.x += self.vel[0]
                        self.y += self.vel[1]
                        move_astroids(self.astr)
                        move_projectiles(self.pjct)

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
                                if vec_length(self.pjct[i].vel) < 0.4:
                                        plist.append(i)
                        for i in range(len(plist)):
                                del plist[i]
                                del self.pjct[i]        

                        #collision
                        self.points += self.hit(self.pjct,self.astr)
                        if collision(self.x,self.y,self.astr):
                                pass


        def loss(self):
                pass


        def hit(self,p,a):
                points = 0
                plist = []
                alist = []
                if len(p)*len(a) > 0:
                        for i in range(len(p)):
                                for j in range(len(a)):
                                        if dist(p[i].x,a[j].x,p[i].y,a[j].y) < a[j].size*10:
                                                plist.append(i)
                                                split_a = a[j].split()
                                                if split_a != None:
                                                        a.append(split_a)
                                                        points += 100*(split_a.size+1)
                                                else:
                                                        alist.append(j)
                                                        points += 100
                                                 
                for i in plist:
                        del self.pjct[i]
                        for j in range(len(plist)-1):
                                del plist[j]
                for i in alist:
                        del self.astr[i]
                        for j in range(len(alist)-1):
                                del alist[j]
                return points


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
        vel = [cos(dir)*8,sin(dir)*8]
        p.append(projectile(x+cos(dir)*8,y+sin(dir)*8,vel))

def collision(x,y,a):
        hit = False
        for i in range(len(a)-1):
                di = dist(x,a[i].x,y,a[i].y)
                if di < 4+a[i].size*10:
                        hit = True
        return hit


def mapFromTo(x,a,b,c,d):
        y = (x-a)/(b-a)*(d-c)+c
        return y

def dist(x1,x2,y1,y2):
        d = sqrt(((x1-x2)**2)+((y1-y2)**2))
        return d

def vec_length(vec):
        l = sqrt(vec[0]**2+vec[1]**2)
        return l


def Ship_pointlist(ro,x,y):
        l = [[8,135],[8,225],[8,0]]
        ship_point_list = []
        for i in range(3):
                dir = mapFromTo(ro+l[i][1],0,360,0.0,2*pi)
                P = [x+cos(dir)*l[i][0],y+sin(dir)*l[i][0]]
                ship_point_list.append(P)
        return ship_point_list



def draw_game():
        if game.state == 0:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(380, 280, 80, 50))
                screen.blit(myfont.render("MENU", 1, (255, 255, 255)), (400, 300))
        elif game.state == 1:
                screen.fill((0, 10, 20))
                #pygame.transform.rotate(screen, game.ro % 360)
                pygame.draw.polygon(screen, (255,255,255), Ship_pointlist(game.ro,game.x,game.y), 1)

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
