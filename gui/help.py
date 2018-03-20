import pygame
from yagui import Element, Sprite, Label
from gui.elements import Button
from gui.constants import *


class HelpSplash(Element):
    def on_app(self):
        Element.on_app(self)
        self.image = Sprite(app = self.app, surface = pygame.image.load('res/img/help1.png').convert(), x = 0, y = 300)
        self.current = 1

    # Draw
    def draw(self, area):
        self.image.draw(area)

class BackwardButton(Button):
    def on_app(self):
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_75px_gray.png').convert(), x = 10, y = 560)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = 'Back', x = 10, y = 560, color = COLOR.WHITE, center_x = 75)

    def on_click(self):
        if self.app.help_splash.current > 1:
            self.app.help_splash.current -= 1
            self.app.help_splash.image.surface = pygame.image.load('res/img/help' + str(self.app.help_splash.current) + '.png').convert()

class ForwardButton(Button):
    def on_app(self):
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_75px_gray.png').convert(), x = 415, y = 560)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = 'Next', x = 415, y = 560, color = COLOR.WHITE, center_x = 75)

    def on_click(self):
        if self.app.help_splash.current < 3:
            self.app.help_splash.current += 1
            self.app.help_splash.image.surface = pygame.image.load('res/img/help' + str(self.app.help_splash.current) + '.png').convert()
        else:
            def to_splash():
                if self.box.y == 560:
                    self.app.help_splash.current = 1
                    self.app.help_splash.image.surface = pygame.image.load('res/img/help1.png').convert()
                    self.remove_update_function(function = to_splash)
                else:
                    self.app.slide_splash(y = 20)
                    self.app.slide_help(y = 20)
            self.add_update_function(function = to_splash)