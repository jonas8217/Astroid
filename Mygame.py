import pygame
from math import pi,cos,sin
from random import randint,random


class Game:
        def __init__(self):
                self.state = 0
                #State 0: Menu
                #State 1: Game
                #State 2: Pause
                self.spd = 0.0
                self.ro = 0
                self.y = 300
                self.x = 400
                self.points = 0
                self.vel = [0.0,0.0]
                

        def tick(self, pg, pressed):
                if self.state == 1:
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

                        dir = mapFromTo(self.ro,0,360,0.0,2*pi)
                        self.vel = [cos(dir)*self.spd,sin(dir)*self.spd]
                        print(self.vel)
                        self.x += self.vel[0]
                        self.y += self.vel[1]


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

def mapFromTo(x,a,b,c,d):
   y = (x-a)/(b-a)*(d-c)+c
   return y

def draw_game():
        if game.state == 0:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(380, 280, 80, 50))
                screen.blit(myfont.render("MENU", 1, (255, 255, 255)), (400, 300))
        elif game.state == 1:
                screen.fill((0, 10, 20))
                pygame.draw.rect(screen, (10, 123, 50), pygame.Rect(game.x, game.y, 50, 50))
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
