import pygame
from math import pi, cos, sin, sqrt
from random import randint
from Astroid import astroid
from Projectile import projectile
import pygame_textinput
from highscoreLogger import Logger
import pickle
import base64
import io

class Game:
        def __init__(self):
                self.logger = Logger()

                self.state = 0
                #State 0: Menu
                #State 1: Game
                #State 2: Pause
                #State 3: Highscore input

                #player/ship variables
                self.ro = 0
                self.x = 400
                self.y = 300
                self.points = 0
                self.shield = 3
                self.stage = 0
                self.vel = [0.0, 0.0]
                self.dead = False
                self.thrust_counter = 0
                self.thrust = False

                #astroid and projectile list
                self.astr = []
                self.pjct = []

                #game fase handeling variables
                self.counter = 0
                self.pause_counter = 0

                #Highscore definitions
                self.scores = self.get_highscores()[:10]
                self.localScores = self.get_local_highscores()[:5]

        def tick(self, pg, pressed):
                if self.state == 1:

                        #stage
                        if len(self.astr) == 0 and not self.dead:
                                self.pause_counter += 1
                                if self.pause_counter >= 40:
                                        self.pause_counter = 0
                                        self.newStage()

                        #check_if_dead
                        if self.dead:
                                self.game_shieldloss_init()

                        #ship_direction_calc
                        dir = mapFromTo(self.ro, 0, 360, 0.0, 2 * pi)

                        #controls
                        if pressed[pg.K_UP] and vec_length(self.vel) < 8:
                                self.vel[0] += cos(dir) * 0.2
                                self.vel[1] += sin(dir) * 0.2
                                self.thrust = True
                        else:
                                self.thrust = False
                        if pressed[pg.K_LEFT]:
                                self.ro -= 5
                        if pressed[pg.K_RIGHT]:
                                self.ro += 5
                        self.counter += 1
                        if pressed[pg.K_SPACE] and self.counter >= 25:
                                self.counter = 0
                                shoot(self.pjct, self.x, self.y, self.ro)

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
                        if len(self.astr) * len(self.pjct) > 0:
                                self.points += self.hit(self.pjct, self.astr)
                        if collision(self.x, self.y, self.astr):
                                self.ship_hit()

                if self.state == 4:
                        self.reload()

        def newStage(self):
                self.stage += 1
                self.pjct = []
                newAstr = self.stage * 1.5 + 4
                for i in range(int(newAstr)):
                        side = i % 4
                        if side == 0:
                                self.astr.append(astroid(50, 50 + randint(0, 700), 3))
                        if side == 1:
                                self.astr.append(astroid(50 + randint(0, 500), 50, 3))
                        if side == 2:
                                self.astr.append(astroid(750, 50 + randint(0, 700), 3))
                        if side == 3:
                                self.astr.append(astroid(50 + randint(0, 500), 550, 3))

        def ship_hit(self):
                self.shield -= 1
                if self.shield > 0:
                        self.game_shieldloss_init()
                else:
                        self.highscore_input()

        def hit(self, p, a):
                points = 0
                plist = []
                alist = []
                if len(p) * len(a) > 0:
                        for i in range(len(p)):
                                for j in range(len(a)):
                                        if dist(p[i].x, a[j].x, p[i].y, a[j].y) < a[j].size * 10 + 1:
                                                plist.append(i)
                                                split_a = a[j].split()
                                                if split_a is not None:
                                                        a.append(split_a)
                                                        points += 100 * (split_a.size + 1)
                                                else:
                                                        alist.append(j)
                                                        points += 100

                for i in uniq(plist)[::-1]:
                        del self.pjct[i]

                for i in uniq(alist)[::-1]:
                        del self.astr[i]

                return points

        def game_shieldloss_init(self):
                self.pause_counter += 1
                if not self.dead:
                        self.x = 400
                        self.y = 300
                        self.ro = 0
                        self.vel = [0.0, 0.0]

                        self.pjct = []
                        self.temp_astr = self.astr.copy()
                        self.astr = []
                        self.dead = True
                elif self.pause_counter >= 40:
                        self.pause_counter = 0
                        self.dead = False
                        for i in range(len(self.temp_astr)):
                                side = i % 4
                                if side == 0:
                                        self.temp_astr[i].x, self.temp_astr[i].y = (50, 50 + randint(0, 700))
                                if side == 1:
                                        self.temp_astr[i].x, self.temp_astr[i].y = (50 + randint(0, 500), 50)
                                if side == 2:
                                        self.temp_astr[i].x, self.temp_astr[i].y = (750, 50 + randint(0, 700))
                                if side == 3:
                                        self.temp_astr[i].x, self.temp_astr[i].y = (50 + randint(0, 500), 550)
                        self.astr = self.temp_astr. copy()

        def save_highscore(self, name):
                #Pickle database

                try:
                        with open('highscore.txt', 'rb') as f:
                                scores = pickle.load(f)  #score = {'Name':'','Score':0,'Stage':0} layout of stored indexes
                except:
                        print('No Scorefile, creating score file')
                        score = {'Name': '', 'Score': 0, 'Stage': 0}
                        scores = []
                        for i in range(10):
                                scores.append(score)
                        with open('highscore.txt', 'wb') as f:
                                pickle.dump(scores, f)
                for i in range(len(scores)):
                        if self.points > scores[i]['Score']:
                                newHigh = {'Name': str(name), 'Score': self.points, 'Stage': self.stage}
                                scores.insert(i, newHigh)
                                break
                scores = scores[:10]
                self.localScores = scores[:5]
                with open('highscore.txt', 'wb') as f:
                        print('saving scorefile')
                        pickle.dump(scores, f)

                if self.points > 0:
                        self.logger.post_score('Astroid', self.points, str(name), self.stage)

                scores = []
                try:
                        for s in self.logger.get_scores('Astroid'):
                                scores.append({'Name': s['Opt1'], 'Score': s['Score'], 'Stage': s['Opt2']})
                        scores = sorted(scores, key=lambda scores: scores['Score'], reverse=True)
                except:
                        print('server database error')

                self.state = 4

        def reload(self, state=0):
                self.state = state
                self.ro = 0
                self.x = 400
                self.y = 300
                self.points = 0
                self.shield = 3
                self.stage = 0
                self.vel = [0.0, 0.0]
                self.astr = []
                self.pjct = []
                self.counter = 0
                self.scores = self.get_highscores()[:10]
                self.localScores = self.get_local_highscores()[:5]

        def get_highscores(self):
                scores = []
                try:
                        for s in self.logger.get_scores('Astroid'):
                                scores.append({'Name': s['Opt1'], 'Score': s['Score'], 'Stage': s['Opt2']})
                        return sorted(scores, key=lambda scores: scores['Score'], reverse=True)
                except:
                        print('server database error')
                        return []

        def get_local_highscores(self):
                try:
                        with open('highscore.txt', 'rb') as f:
                                scores = pickle.load(f)  #score = {'name':'','score':0,'stage':0}
                except:
                        print('No Scorefile, creating score file')
                        score = {'Name': '', 'Score': 0, 'Stage': 0}
                        scores = []
                        for i in range(10):
                                scores.append(score)
                        with open('highscore.txt', 'wb') as f:
                                pickle.dump(scores, f)
                return scores

        def start_game(self):
                if self.state == 0:
                        self.state = 1
                        self.reload(1)

        def end_game(self):
                if self.state > 0:
                        self.state = 0

        def toggle_pause(self):
                if self.state == 1:
                        self.state = 2
                        self.scores = self.get_highscores()[:10]
                        self.localScores = self.get_local_highscores()[:5]
                elif self.state == 2:
                        self.state = 1

        def started(self):
                if self.state > 0:
                        return True
                else:
                        return False

        def highscore_input(self):
                if self.state == 1:
                        self.state = 3


def move_astroids(a):
        for i in range(len(a)):
                a[i].move()


def move_projectiles(p):
        for i in range(len(p)):
                p[i].move()


def shoot(p, x, y, ro):
        dir = mapFromTo(ro, 0, 360, 0.0, 2 * pi)
        vel = [cos(dir) * 8, sin(dir) * 8]
        p.append(projectile(x + cos(dir) * 8, y + sin(dir) * 8, vel))


def collision(x, y, a):
        hit = False
        if len(a) > 0:
                for i in range(len(a)):
                        di = dist(x, a[i].x, y, a[i].y)
                        if di < 4 + a[i].size * 10:
                                hit = True
        return hit


def mapFromTo(x, a, b, c, d):
        y = (x - a) / (b - a) * (d - c) + c
        return y


def dist(x1, x2, y1, y2):
        d = sqrt(((x1 - x2)**2) + ((y1 - y2)**2))
        return d


def vec_length(vec):
        lenght = sqrt(vec[0]**2 + vec[1]**2)
        return lenght


def uniq(lst):
        seen = set()
        uniq = []
        for x in lst:
                if x not in seen:
                        uniq.append(x)
                        seen.add(x)
        uniq.sort()
        return uniq


def Ship_pointlist(ro, x, y):
        lst = [[8, 135], [8, 225], [8, 0]]
        ship_point_list = []
        for i in range(3):
                dir = mapFromTo(ro + lst[i][1], 0, 360, 0.0, 2 * pi)
                P = [x + cos(dir) * lst[i][0], y + sin(dir) * lst[i][0]]
                ship_point_list.append(P)
        return ship_point_list

def Ship_thrust_pointlist(ro, x, y):
        lst = [[6, 160], [10, 180], [6, 200]]
        ship_thrust_point_list = []
        for i in range(3):
                dir = mapFromTo(ro + lst[i][1], 0, 360, 0.0, 2 * pi)
                P = [x + cos(dir) * lst[i][0], y + sin(dir) * lst[i][0]]
                ship_thrust_point_list.append(P)
        return ship_thrust_point_list


def draw_game():
        if game.state == 0:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 600))

                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(360, 280, 80, 40))
                screen.blit(myfont.render("MENU", 1, (255, 255, 255)), (381, 291))

        elif game.state == 1:
                screen.fill((0, 10, 20))
                #pygame.transform.rotate(screen, game.ro % 360)
                pygame.draw.polygon(screen, (255, 255, 255), Ship_pointlist(game.ro, game.x, game.y), 1)
                if game.thrust_counter > 9:
                        game.thrust_counter = 0
                if 0 <= game.thrust_counter <= 5 and game.thrust:
                        pygame.draw.polygon(screen, (255, 255, 255), Ship_thrust_pointlist(game.ro, game.x, game.y), 1)
                game.thrust_counter += 1



                if len(game.astr) > 0:
                        for i in range(len(game.astr)):
                                pygame.draw.circle(screen, (255, 255, 255), (int(game.astr[i].x), int(game.astr[i].y)), game.astr[i].size * 10, 2)
                if len(game.pjct) > 0:
                        for i in range(len(game.pjct)):
                                pygame.draw.circle(screen, (255, 255, 255), (int(game.pjct[i].x), int(game.pjct[i].y)), 2, 0)
                screen.blit(myfont.render("Points: {}".format(game.points), 1, (255, 255, 0)), (20, 20))
                screen.blit(myfont.render("Shield: {}".format(game.shield), 1, (255, 255, 0)), (20, 35))
                screen.blit(myfont.render("Stage: {}".format(game.stage), 1, (255, 255, 0)), (20, 50))
                game.textinput = pygame_textinput.TextInput()
        elif game.state == 2:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(360, 280, 80, 40))
                screen.blit(myfont.render("PAUSE", 1, (255, 255, 255)), (377, 291))

        if game.state == 2 or game.state == 0:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(570, 10, 210, 40 + 15 * len(game.scores)))
                screen.blit(myfont.render("Highscores:", 1, (255, 255, 0)), (590, 20))
                for i, j in enumerate(game.scores):
                        screen.blit(myfont.render(str(j['Name']) + ': ' + str(j['Score']) + ' at ' + str(j['Stage']), 1, (255, 255, 0)), (590, 35 + i * 15))

                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(260, 400, 300, 120))
                screen.blit(myfont.render("Controls:", 1, (255, 255, 255)), (270, 405))
                screen.blit(myfont.render("Thrust: Up Arrow", 1, (255, 255, 255)), (280, 420))
                screen.blit(myfont.render("Turn: Left and Right Arrows", 1, (255, 255, 255)), (280, 435))
                screen.blit(myfont.render("Shoot: Spacebar", 1, (255, 255, 255)), (280, 450))
                screen.blit(myfont.render("Pause: p", 1, (255, 255, 255)), (280, 465))
                screen.blit(myfont.render("Exit Game/New Game: ESC", 1, (255, 255, 255)), (280, 480))
                screen.blit(myfont.render("Sumbmit Score: Enter", 1, (255, 255, 255)), (280, 495))

                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(570, 400, 210, 30 + 15 * len(game.localScores)))
                screen.blit(myfont.render("Local Highscores:", 1, (255, 255, 0)), (590, 405))
                for i, j in enumerate(game.localScores):
                        screen.blit(myfont.render(str(j['Name']) + ': ' + str(j['Score']) + ' at ' + str(j['Stage']), 1, (255, 255, 0)), (590, 420 + i * 15))

        elif game.state == 3:
                screen.fill((225, 225, 225))
                if game.textinput.update(events) and len(game.textinput.get_text()) > 0:
                        game.save_highscore(game.textinput.get_text())
                screen.blit(game.textinput.get_surface(), (10, 10))


pygame.init()
try:
        icon = "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"
        icon = io.BytesIO(base64.b64decode(icon))
        pygame.display.set_icon(pygame.image.load(icon))
except:
        print('idk man')
pygame.display.set_caption('Astroid')
screen = pygame.display.set_mode((800, 600))
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)

done = False

game = Game()

clock = pygame.time.Clock()

while not done:
        events = pygame.event.get()
        for event in events:
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game.toggle_pause()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not game.dead:
                        if game.started():
                                game.end_game()
                        else:
                                game.start_game()

        pressed = pygame.key.get_pressed()

        game.tick(pygame, pressed)

        draw_game()
        pygame.display.flip()
        clock.tick(60)
