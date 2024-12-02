import pygame as py
import random

class Palet:
    def __init__(self, surf, pos, image, scale, size=(6,32)):
        self.surf = surf
        self.pos = list(pos)
        self.size = size
        self.scale = scale
        self.image = py.transform.scale(image, (size[0]*scale, size[1]*scale))

        self.speed = 5

    def rect(self):
        return py.Rect(self.pos[0], self.pos[1], self.size[0]*self.scale, self.size[1]*self.scale)

    def update(self, screen, movement):
        if movement[0]:
            self.pos[1] -= self.speed
        if movement[1]:
            self.pos[1] += self.speed

        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] + self.size[1]*self.scale > screen.get_height():
            self.pos[1] = screen.get_height() - self.size[1]*self.scale

    def bot_update(self, screen, ball):
        ball_y = ball.rect().centery

        caption = py.display.get_caption()

        if not caption[0] == 'Main': #  or caption[0] == 'Choose mode' or caption[0] == 'Options'
            if self.rect().centery <= ball_y:
                self.pos[1] += self.speed - random.randint(-2, 3)
            elif self.rect().centery >= ball_y:
                self.pos[1] -= self.speed - random.randint(-2, 3)
        else:
            if self.rect().centery <= ball_y:
                if abs(ball.speed[1]) != 0:
                    self.pos[1] += abs(ball.speed[1])
                else:
                    self.pos[1] = random.choice([ball.pos[1], ball.pos[1]-20])
            elif self.rect().centery >= ball_y:
                if abs(ball.speed[1]) != 0:
                    self.pos[1] -= abs(ball.speed[1])
                else:
                    self.pos[1] = random.choice([ball.pos[1], ball.pos[1]-20])

        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] + self.size[1]*self.scale > screen.get_height():
            self.pos[1] = screen.get_height() - self.size[1]*self.scale

    def render(self, surf):
        surf.blit(self.image, (self.pos[0], self.pos[1]))