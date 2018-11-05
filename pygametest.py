import pygame
import math
from random import randint

class Game:
        def __init__(self):
                self.state = 0
                #State 0: Menu
                #State 1: Game
                #State 2: Pause
                self.x = 100
                self.y = 100
                self.points = 0
                self.target = [250, 250]
                

        def tick(self, pg, pressed):
                if self.state == 1:
                        if pressed[pg.K_UP]: 
                                self.y -= 3
                        if pressed[pg.K_DOWN]: 
                                self.y += 3
                        if pressed[pg.K_LEFT]: 
                                self.x -= 3
                        if pressed[pg.K_RIGHT]: 
                                self.x += 3
                        if math.sqrt((self.target[0] - self.x)**2 + (self.target[1] - self.y)**2) < 40:
                                self.points += 1
                                self.target = [randint(0,800), randint(0,600)]
        
        def start_game(self):
                if self.state == 0:
                        self.state = 1     
                        self.points = 0
                        self.x = 100
                        self.y = 100
                        self.target = [randint(0,800), randint(0,600)]

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

def draw_game():
                if game.state == 0:
                        pygame.draw.rect(screen, (30,30,30), pygame.Rect(380, 280, 80, 50))
                        screen.blit(myfont.render("MENU", 1, (255,255,255)), (400, 300))
                elif game.state == 1:
                        screen.fill((0,10,20))
                        pygame.draw.rect(screen, (10,123,50), pygame.Rect(game.x, game.y, 50, 50))
                        pygame.draw.rect(screen, (123,50,10), pygame.Rect(game.target[0], game.target[1], 50, 50))
                        screen.blit(myfont.render("Points: {}".format(game.points), 1, (255,255,0)), (100, 100))
                elif game.state == 2:
                        pygame.draw.rect(screen, (30,30,30), pygame.Rect(380, 280, 80, 50))
                        screen.blit(myfont.render("PAUSE", 1, (255,255,255)), (400, 300))

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

