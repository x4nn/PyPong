# +/- 670 lines code

# todo add theme (better design)
# todo mss als je in main op die instructie knoppen drukt, ze zo een geel filterke hebben dajje ze indrukt als test of uw knoppen werken
# todo fix dat hoe hoger of lager je de bal hit, hoe sneller hij zal gaan als beloning (y speed verhogen of verlagen)

from scripts.ball import Ball
from scripts.button import Button
from scripts.palet import Palet
from scripts.utils import load_image, check_button_hover

import pygame as py
import time, os, sys

def resource_path(path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)

class Game:
    def __init__(self):

        self.screen_size = (800, 600)
        self.FPS = 60
        self.bg = (70,70,70)
        self.font = 'Arial'

        self.screen = py.display.set_mode(self.screen_size)
        self.clock = py.time.Clock()

        self.assets = {
            'background': load_image('background.jpg'),
            'start_img': load_image('buttons/start.png'),
            'quit_img': load_image('buttons/quit.png'),
            'ball': load_image('movables/ball.png'),
            'trail': load_image('movables/trail.png'),
            'pvb_img': load_image('modes/pvb.png'),
            'pvp_img': load_image('modes/pvp.png'),
            'bot_img': load_image('movables/bot.png'),
            'p1_img': load_image('movables/player1.png'),
            'p2_img': load_image('movables/player2.png'),
            's_key': load_image('keys/s.png'),
            'x_key': load_image('keys/x.png'),
            'up_key': load_image('keys/up.png'),
            'down_key': load_image('keys/down.png')
        }

        py.mixer.init()

        self.sfx = {
            'hit': py.mixer.Sound(resource_path('data/sfx/hit.wav')),
            'wall_hit': py.mixer.Sound(resource_path('data/sfx/hit.wav')),
            'point': py.mixer.Sound(resource_path('data/sfx/point.wav')),
            'gameover': py.mixer.Sound(resource_path('data/sfx/gameover.wav'))
        }

        self.sfx['hit'].set_volume(0.7)
        self.sfx['wall_hit'].set_volume(0.2)
        self.sfx['point'].set_volume(0.5)

        
        self.bg_img = (70, 70, 70)

        BUTTON_SCALE = 3
        self.start_button = Button(int(self.screen.get_width() / 2) - int(self.assets['start_img'].get_width() * BUTTON_SCALE / 2), 250, self.assets['start_img'], 'start', BUTTON_SCALE)
        self.quit_button = Button(int(self.screen.get_width() / 2) - int(self.assets['quit_img'].get_width() * BUTTON_SCALE / 2), 350, self.assets['quit_img'], 'quit', BUTTON_SCALE)

        MODE_SCALE = 1
        self.pvb_button = Button(int(self.screen.get_width() / 2) - int(self.assets['pvb_img'].get_width() * MODE_SCALE / 2), 225, self.assets['pvb_img'], 'pvb', MODE_SCALE)
        self.pvp_button = Button(int(self.screen.get_width() / 2) - int(self.assets['pvp_img'].get_width() * MODE_SCALE / 2), 325, self.assets['pvp_img'], 'pvp', MODE_SCALE)

        self.distance_from_wall = 25
        self.PALET_SCALE = 2
        self.BOT = Palet(self.screen, (self.screen.get_width() - self.distance_from_wall - (int(self.assets['bot_img'].get_width())*self.PALET_SCALE), int(self.screen.get_height()/2) - int(self.assets['bot_img'].get_height()/2)), self.assets['bot_img'], self.PALET_SCALE)
        self.BOT_main = Palet(self.screen, (self.distance_from_wall, int(self.screen.get_height()/2) - int(self.assets['p1_img'].get_height()/2)), self.assets['p1_img'], self.PALET_SCALE)
        self.player1 = Palet(self.screen, (self.distance_from_wall, int(self.screen.get_height()/2) - int(self.assets['p1_img'].get_height()/2)), self.assets['p1_img'], self.PALET_SCALE)
        self.player2 = Palet(self.screen, (self.screen.get_width() - self.distance_from_wall - (int(self.assets['p2_img'].get_width())*self.PALET_SCALE), int(self.screen.get_height()/2) - int(self.assets['p2_img'].get_height()/2)), self.assets['p2_img'], self.PALET_SCALE)
        self.movement_p1 = [False, False]
        self.movement_p2 = [False, False]

        self.score_left = 0
        self.score_right = 0
        self.MAX_SCORE = 3

        self.vert_ball_speed = 5
        ball_size = 16
        self.ball = Ball(self, (self.screen.get_width()/2 - ball_size/2, self.screen.get_height()/2), self.assets['ball'], 1, ball_size)
        self.point_scored = False

    # main menu screen
    def main(self):
        py.display.set_caption('Main')
        py.init()
        py.font.init()

        py.mixer.music.load('data/music.wav')
        py.mixer.music.set_volume(0.5)
        py.mixer.music.play(-1)

        while True:
            self.screen.fill(self.bg) # background
            # self.screen.blit(self.bg, (0, 0))

            self.bg_gameplay()
            self.title('2D Ping Pong', 'x4n')

            self.start_button.render(self.screen)
            self.quit_button.render(self.screen)

            check_button_hover()
            self.check_main_events(self.start_button, self.quit_button)

            py.display.update()
            self.clock.tick(self.FPS)

    def title(self, title, name):
        font_size = 40
        game_name = py.font.SysFont(self.font, font_size)
        creator = py.font.SysFont(self.font, font_size//2)

        t1 = game_name.render(title, False, (255, 255, 0))
        t2 = creator.render('by: ' + name, False, (255, 200, 100))

        self.screen.blit(t1, (self.screen.get_width()//2 - t1.get_width()//2, 30))
        self.screen.blit(t2, (self.screen.get_width()//2 - t2.get_width()//2, 30 + t1.get_height()))

    def check_main_events(self, start_b, quit_b):
        mpos = py.mouse.get_pos()

        for event in py.event.get():
                if event.type == py.QUIT or (quit_b.rect.collidepoint(mpos) and event.type == py.MOUSEBUTTONDOWN):
                    py.quit()
                    quit()

                if start_b.rect.collidepoint(mpos):
                    if event.type == py.MOUSEBUTTONDOWN:
                        self.choose_mode()

    # choose mode screen
    def choose_mode(self):
        py.display.set_caption('Choose mode')
         
        while True:
            self.screen.fill(self.bg) # background

            self.instructions()

            self.pvb_button.render(self.screen)
            self.pvp_button.render(self.screen)

            check_button_hover()
            self.check_mode_events(self.pvb_button, self.pvp_button)

            py.display.update()
            self.clock.tick(self.FPS)

    def instructions(self):
        key_s = py.transform.scale(self.assets['s_key'], (40, 40))
        key_x = py.transform.scale(self.assets['x_key'], (40, 40))
        key_up = py.transform.scale(self.assets['up_key'], (40, 40))
        key_down = py.transform.scale(self.assets['down_key'], (40, 40))

        font_size = 20
        y = 33
        left = py.font.SysFont(self.font, font_size)
        right = py.font.SysFont(self.font, font_size)

        t1 = left.render('Controls left:', False, (255, 255, 255))
        t2 = right.render('Controls right:', False, (255, 255, 255))

        self.screen.blit(t1, (10, y))
        self.screen.blit(t2, (self.screen.get_width() - t2.get_width() - 100, y))

        self.screen.blit(key_s, (t1.get_width() + 25, 10))
        self.screen.blit(key_x, (t1.get_width() + 25, 13 + key_s.get_height()))
        self.screen.blit(key_up, (self.screen.get_width() - t2.get_width() - 100 + t2.get_width() + 15, 10))
        self.screen.blit(key_down, (self.screen.get_width() - t2.get_width() - 100 + t2.get_width() + 15, 13 + key_s.get_height()))

    def check_mode_events(self, mode1_b, mode2_b): # add if more modes later
        mpos = py.mouse.get_pos()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()

            if mode1_b.rect.collidepoint(mpos):
                if event.type == py.MOUSEBUTTONDOWN:
                    self.ball.center_on_board()
                    py.mixer.music.set_volume(0.05)
                    self.player_vs_computer()
            if mode2_b.rect.collidepoint(mpos):
                if event.type == py.MOUSEBUTTONDOWN:
                    self.ball.center_on_board()
                    py.mixer.music.set_volume(0.05)
                    self.player_vs_player()
            
    # player vs computer
    def player_vs_computer(self):
        py.display.set_caption('player vs computer')

        py.font.init() # todo delete normaal        
        self.countdown()

        self.reset_score()
        while True:
            self.screen.fill(self.bg) # bg         

            self.render_scoreboard()

            self.draw_center_line()

            self.player1.update(self.screen, self.movement_p1)
            self.player1.render(self.screen)

            self.BOT.bot_update(self.screen, self.ball)
            self.BOT.render(self.screen)

            self.ball.update(self.screen, self.player1, self.BOT)
            self.ball.render(self.screen)

            self.check_game_events()

            self.check_score()

            py.display.update()
            self.clock.tick(self.FPS)
    
    # player vs player
    def player_vs_player(self):
        py.display.set_caption('player vs player')

        py.font.init() # todo delete normaal        
        self.countdown()

        self.reset_score()
        while True:
            self.screen.fill(self.bg) # bg         

            self.render_scoreboard()

            self.draw_center_line()

            self.player1.update(self.screen, self.movement_p1)
            self.player1.render(self.screen)

            self.player2.update(self.screen, self.movement_p2)
            self.player2.render(self.screen)

            self.ball.update(self.screen, self.player1, self.player2)
            self.ball.render(self.screen)

            self.check_game_events()

            self.check_score()

            py.display.update()
            self.clock.tick(self.FPS)

    # game over screen
    def game_over(self, winner):
        py.display.set_caption('Game Over')
        py.init()
        py.font.init()

        self.reset_score()

        py.mixer.music.stop()
        self.sfx['gameover'].play(0)

        while True:
            self.screen.fill(self.bg) # background

            font_size = 60
            my_font = py.font.SysFont(self.font, font_size)

            # Render the text
            gameover_text = winner + ' won the game!'
            gameover = my_font.render(gameover_text, False, (255, 255, 255))

            # Get the width and height of the text
            text_width, text_height = gameover.get_size()

            # Calculate the position for the text to be centered
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            center_x = (screen_width - text_width) // 2
            center_y = (screen_height - text_height) // 2

            # Blit the text at the calculated position
            self.screen.blit(gameover, (center_x, center_y))

            py.display.update()
            py.time.delay(2000)

            self.main()
            
    def reset_score(self):
        self.score_left = 0
        self.score_right = 0

    # general
    def draw_center_line(self):
        loop = True
        thickness = 5
        length = 30
        gap = 10
        i = 0

        center_screen = (int(self.screen.get_width()/2), int(self.screen.get_height()/2))

        while loop:
            y = (i * length) + (i * gap)
            square = py.Rect(int(self.screen.get_width()/2) - thickness/2, y, thickness, length)
            py.draw.rect(self.screen, (255, 255, 255), square)
            i += 1

            if (i * length) + (i * gap) > self.screen.get_height():
                loop = False

        radius = 18
        py.draw.circle(self.screen, (255, 255, 255), (center_screen[0], center_screen[1]+8), radius, 4)
        py.draw.circle(self.screen, self.bg, (center_screen[0], center_screen[1]+8), radius-4)

    def check_game_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.main()

                if event.key == py.K_s:
                    self.movement_p1[0] = True
                if event.key == py.K_x:
                    self.movement_p1[1] = True
                if event.key == py.K_UP:
                    self.movement_p2[0] = True
                if event.key == py.K_DOWN:
                    self.movement_p2[1] = True

            if event.type == py.KEYUP:
                if event.key == py.K_s:
                    self.movement_p1[0] = False
                if event.key == py.K_x:
                    self.movement_p1[1] = False
                if event.key == py.K_UP:
                    self.movement_p2[0] = False
                if event.key == py.K_DOWN:
                    self.movement_p2[1] = False

    def countdown(self):
        font_size = 90
        my_font = py.font.SysFont(self.font, font_size)

        for i in range(3, 0, -1):
            self.screen.fill(self.bg)

            self.player1.render(self.screen)
            self.BOT.render(self.screen)

            text_surface = my_font.render(str(i), False, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen_size[0]/2 - font_size/2, self.screen_size[1]/2 - font_size/2))

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()

            py.display.update()
            time.sleep(1)
            self.clock.tick(self.FPS)

    def render_scoreboard(self):
        font_size = 60
        distance_from_left_wall = 275
        padding = 10
        my_font = py.font.SysFont(self.font, font_size)

        text_left = my_font.render(str(self.score_left), False, (255, 255, 255))
        text_right = my_font.render(str(self.score_right), False, (255, 255, 255))

        bg_l = py.Rect(distance_from_left_wall-padding, self.screen.get_height()/2 - 15 - padding, 50 + padding, font_size+ 2*padding)
        bg_r = py.Rect(self.screen.get_width() - distance_from_left_wall - font_size/2 - padding, self.screen.get_height()/2 - 15 - padding, 50 + padding, font_size+ 2*padding)
        py.draw.rect(self.screen, self.bg, bg_l)
        py.draw.rect(self.screen, self.bg, bg_r)

        self.screen.blit(text_left, (distance_from_left_wall, self.screen.get_height()/2 - font_size/2))
        self.screen.blit(text_right, (self.screen.get_width() - distance_from_left_wall - font_size/2, self.screen.get_height()/2 - font_size/2))

    def update_scoreboard(self, score_left):
        if score_left:
            self.score_left += 1
        else:
            self.score_right += 1

    def check_score(self):
        if self.score_left == self.MAX_SCORE:
            self.game_over('Left side')
        if self.score_right == self.MAX_SCORE:
            self.game_over('Right side')
        
    def bg_gameplay(self):
        self.BOT_main.bot_update(self.screen, self.ball)
        self.BOT_main.render(self.screen)

        self.BOT.bot_update(self.screen, self.ball)
        self.BOT.render(self.screen)

        self.ball.update(self.screen, self.BOT_main, self.BOT, True)
        self.ball.render(self.screen)

# Game().player_vs_computer()
# Game().player_vs_player()
# Game().choose_mode()
Game().main()