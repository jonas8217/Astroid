import pygame
from math import pi, cos, sin, sqrt
from random import randint
from Astroid import Astroid
from Projectile import Projectile
from highscoreLogger import Logger
import pickle

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

                #Astroid and projectile list
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
                                self.death_init()

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
                                self.shoot()

                        #ship_movement_de-acc
                        self.vel[0] *= 0.985
                        self.vel[1] *= 0.985

                        #movement_execution
                        self.x += self.vel[0]
                        self.y += self.vel[1]
                        for i in self.astr:
                                i.move()
                        for i in self.pjct:
                                i.move()

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

                        ##Astroids
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
                        if self.collision():
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
                                self.astr.append(Astroid(50, 50 + randint(0, 700), 3))
                        if side == 1:
                                self.astr.append(Astroid(50 + randint(0, 500), 50, 3))
                        if side == 2:
                                self.astr.append(Astroid(750, 50 + randint(0, 700), 3))
                        if side == 3:
                                self.astr.append(Astroid(50 + randint(0, 500), 550, 3))

        def ship_hit(self):
                self.shield -= 1
                if self.shield > 0:
                        self.death_init()
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
        
        def collision(self):
                hit = False
                if len(self.astr) > 0:
                        for i in range(len(self.astr)):
                                di = dist(self.x, self.astr[i].x, self.y, self.astr[i].y)
                                if di < 4 + self.astr[i].size * 10:
                                        hit = True
                return hit
        
        def shoot(self):
                dir = mapFromTo(self.ro, 0, 360, 0.0, 2 * pi)
                vel = [cos(dir) * 8, sin(dir) * 8]
                self.pjct.append(Projectile(self.x + cos(dir) * 8, self.y + sin(dir) * 8, vel))

        def Ship_pointlist(self):
                lst = [[8, 135], [8, 225], [8, 0]]
                ship_point_list = []
                for i in range(3):
                        dir = mapFromTo(self.ro + lst[i][1], 0, 360, 0.0, 2 * pi)
                        P = [self.x + cos(dir) * lst[i][0], self.y + sin(dir) * lst[i][0]]
                        ship_point_list.append(P)
                return ship_point_list

        def Ship_thrust_pointlist(self):
                lst = [[6, 160], [10, 180], [6, 200]]
                ship_thrust_point_list = []
                for i in range(3):
                        dir = mapFromTo(self.ro + lst[i][1], 0, 360, 0.0, 2 * pi)
                        P = [self.x + cos(dir) * lst[i][0], self.y + sin(dir) * lst[i][0]]
                        ship_thrust_point_list.append(P)
                return ship_thrust_point_list

        def death_init(self):
                self.pause_counter += 1
                if not self.dead:
                        self.x = 400
                        self.y = 300
                        self.ro = 0
                        self.vel = [0.0, 0.0]
                        self.dead = True
                        self.pjct = []
                        self.temp_astr = self.astr.copy()
                        self.astr = []

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
                        for i in range(5):
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

        def highscore_input(self):
                if self.state == 1:
                        self.state = 3

        def started(self):
                if self.state > 0:
                        return True
                else:
                        return False


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