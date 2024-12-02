import pygame as py

class Button:

    all_buttons = set()

    def __init__(self, x, y, image, type, scale=1):
        height = image.get_height()
        width = image.get_width()
        
        self.x = x
        self.y = y
        self.type = type
        self.image = py.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image.set_colorkey((0,0,0))
        self.rect = py.Rect(x-10, y-10, width*scale +20, height*scale +20)
        self.color = (255,255,255)

        self.all_buttons.add(self)

    def render(self, surf):
        surf.blit(self.image, (self.x, self.y))
        py.draw.rect(surf, self.color, self.rect, 3)

    def active(self):
        self.color = (255,0,0)

    def inactive(self):
        self.color = (255,255,255)

