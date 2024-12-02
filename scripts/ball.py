import pygame as py
import time
import random

class Ball:

    trail_created = False
    
    def __init__(self, game, pos, image, scale=1, size=16):
        self.init_pos = list(pos)
        self.pos = list(pos)
        self.image = py.transform.scale(image, (size*scale, size*scale))
        self.speed = [7, 5]
        self.scale = scale
        self.size = size
        self.game = game

    def trail(self):

        center_circle = list(self.rect().center)

        if not self.game.point_scored:

            for i in range(8): # 8

                if self.speed[0] > 0 and self.speed[1] > 0:
                    center_circle[0] += self.speed[0] * -1
                    center_circle[1] += self.speed[1] * -1

                elif self.speed[0] > 0 and self.speed[1] < 0:
                    center_circle[0] += self.speed[0] * -1
                    center_circle[1] += self.speed[1] * -1

                elif self.speed[0] < 0 and self.speed[1] > 0:
                    center_circle[0] += self.speed[0] * -1
                    center_circle[1] += self.speed[1] * -1

                else:
                    center_circle[0] += self.speed[0] * -1
                    center_circle[1] += self.speed[1] * -1

                py.draw.circle(self.game.screen, (88, 0, 0), center_circle, (self.size//2) - i)

    def rect(self):
        return py.Rect(self.pos[0], self.pos[1], self.size*self.scale, self.size*self.scale)

    def update(self, screen, palet_left, palet_right, main_screen=False):
        self.pos[0] += self.speed[0]

        # palet collision
        if self.rect().colliderect(palet_right):
            self.game.sfx['hit'].play(0)

            if self.game.point_scored:
                self.game.point_scored = False
                self.speed[1] = self.game.vert_ball_speed

            if self.rect().centery > palet_right.rect().centery:
                self.speed[1] = self.game.vert_ball_speed
                self.speed[1] = abs(self.speed[1]) + random.randint(-2, 2)
            elif self.rect().centery == palet_right.rect().centery:
                self.speed[1] = 0
            else:
                self.speed[1] = self.game.vert_ball_speed
                self.speed[1] = -abs(self.speed[1]) - random.randint(-2, 2)

            self.speed[0] *= -1
            self.pos[0] -= self.size

        # palet collision
        if self.rect().colliderect(palet_left):
            self.game.sfx['hit'].play(0)
            
            if self.game.point_scored:
                self.game.point_scored = False
                self.speed[1] = self.game.vert_ball_speed

            if self.rect().centery > palet_left.rect().centery:
                self.speed[1] = self.game.vert_ball_speed
                self.speed[1] = abs(self.speed[1]) + random.randint(-2, 2)
            elif self.rect().centery == palet_left.rect().centery:
                self.speed[1] *= random.choice([-1, 1])
            else:
                self.speed[1] = self.game.vert_ball_speed
                self.speed[1] = -abs(self.speed[1]) - random.randint(-2, 2)

            self.speed[0] *= -1
            self.pos[0] += self.size

        # wall collision
        if self.pos[0] + self.size > screen.get_width(): 
            self.game.sfx['point'].play(0)
            self.update_score(screen, True, palet_left, palet_right, main_screen)
        if self.pos[0] < 2:
            self.game.sfx['point'].play(0)
            self.update_score(screen, False, palet_left, palet_right, main_screen)

        self.pos[1] += self.speed[1]
        if self.pos[1] + self.size > screen.get_height():
            self.speed[1] *= -1
            self.pos[1] -= self.size
            self.game.sfx['wall_hit'].play(0)
        if self.pos[1] < 2:
            self.speed[1] *= -1
            self.pos[1] += self.size
            self.game.sfx['wall_hit'].play(0)

    def update_score(self, screen, is_left_score, left_palet, right_palet, main_screen):
        self.center_on_board()

        self.game.update_scoreboard(is_left_score)

        self.render(screen)

        if not main_screen:
            self.game.render_scoreboard()

        left_palet.pos[1] = int(screen.get_height()/2) - int(self.game.assets['p1_img'].get_height()/2) 
        right_palet.pos[1] = int(screen.get_height()/2) - int(self.game.assets['p1_img'].get_height()/2)

        if not main_screen:
            py.display.update()
            time.sleep(2)

    def center_on_board(self):
        self.pos[0] = self.init_pos[0]
        self.pos[1] = self.init_pos[1]
        self.speed[1] = 0
        self.game.point_scored = True

    def render(self, surf):
        self.trail()

        img = self.image
        img.set_colorkey((0,0,0))
        surf.blit(img, (self.pos[0], self.pos[1]))