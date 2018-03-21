import pygame
from yagui import Element, Sprite, Label
from gui.elements import Button
from gui.constants import *

class HelpSplash(Element):
    '''The main element of the Help "screen," displays images that serve as a tutorial for using the app.'''
    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Element.on_app(self)
        self.image = Sprite(app = self.app, surface = pygame.image.load('res/img/help1.png').convert(), x = 0, y = 300)
        self.current = 1

    # DRAW
    def draw(self, area):
        '''Draws this element's drawables within the specified area onto the App's display.'''
        self.image.draw(area)

class BackwardButton(Button):
    '''A button on the Help "screen" that lets the user navigate backward through the tutorial slides.'''
    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_75px_gray.png').convert(), x = 10, y = 560)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = 'Back', x = 10, y = 560, color = COLOR.WHITE, center_x = 75)

    # ACTIONS
    def on_click(self):
        '''Called when this button is clicked. Navigates backward through the tutorial slides if possible.'''
        if self.app.help_splash.current > 1:
            self.app.help_splash.current -= 1
            self.app.help_splash.image.surface = pygame.image.load('res/img/help' + str(self.app.help_splash.current) + '.png').convert()

class ForwardButton(Button):
    '''A button on the Help "screen" that lets the user navigate forward through the tutorial slides.'''
    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_75px_gray.png').convert(), x = 415, y = 560)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = 'Next', x = 415, y = 560, color = COLOR.WHITE, center_x = 75)

    # ACTIONS
    def on_click(self):
        '''Called when this button is clicked. Navigates forward through the tutorial slides if possible or, at the end of the slides,
        returns the user to the Splash "screen" again.'''
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