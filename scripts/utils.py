import pygame as py
import os, sys

from .button import Button

BASIC_PATH = 'data/images/'

def resource_path(path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)

def load_image(path):
    img_url = resource_path(BASIC_PATH + path)
    img = py.image.load(img_url)
    return img

def check_button_hover():
    mpos = py.mouse.get_pos()

    for button in Button.all_buttons:
        if button.rect.collidepoint(mpos):
            button.active()
        else:
            button.inactive()