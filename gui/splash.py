import pygame
from yagui import Element, Sprite, Label
from gui.elements import Button
from gui.constants import *

class Background(Element):
    def __init__(self):
        Element.__init__(self)

    def on_app(self):
        surface = pygame.Surface((500, 300))
        surface.fill((255, 255, 255))
        self.image = Sprite(app = self.app, surface = surface, x = 0, y = 0)

    def draw(self, area):
        self.image.draw(area)

class Splash(Element):
    def on_app(self):
        self.image = Sprite(app = self.app, surface = pygame.image.load('res/img/splash.png').convert(), x = 0, y = 0)

    # Draw
    def draw(self, area):
        self.image.draw(area)

class HelpButton(Button):
    def on_app(self):
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_150px_red.png').convert(), x = 50, y = 230)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 42), text = 'Help', x = 50, y = 230, color = COLOR.WHITE, center_x = 150, center_y = 60)

    # Actions
    def highlight(self):
        Button.highlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_gray.png').convert()

    def dehighlight(self):
        Button.dehighlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_red.png').convert()

    def on_click(self):
        def to_help():
            if self.box.y == -70:
                self.remove_update_function(function = to_help)
            else:
                self.app.slide_splash(y = -20)
                self.app.slide_help(y = -20)
        self.add_update_function(function = to_help)

class StartButton(Button):
    def on_app(self):
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_150px_red.png').convert(), x = 300, y = 230)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 42), text = 'Start', x = 300, y = 230, color = COLOR.WHITE, center_x = 150, center_y = 60)

    # Actions
    def highlight(self):
        Button.highlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_gray.png').convert()

    def dehighlight(self):
        Button.dehighlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_red.png').convert()

    def on_click(self):
        def to_main():
            if self.box.y == -70:
                self.remove_update_function(function = to_main)
            else:
                self.app.slide_splash(y = -20)
                self.app.slide_main(y = -20)
        self.add_update_function(function = to_main)