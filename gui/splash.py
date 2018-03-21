import pygame
from yagui import Element, Sprite, Label
from gui.elements import Button
from gui.constants import *

class Splash(Element):
    '''The main element of the Splash "screen," displays a logo image.'''
    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        self.image = Sprite(app = self.app, surface = pygame.image.load('res/img/splash.png').convert(), x = 0, y = 0)

    # DRAW
    def draw(self, area):
        '''Draws this element's drawables within the specified area onto the App's display.'''
        self.image.draw(area)

class HelpButton(Button):
    # APP 
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_150px_red.png').convert(), x = 50, y = 230)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 42), text = 'Help', x = 50, y = 230, color = COLOR.WHITE, center_x = 150, center_y = 60)

    # ACTIONS
    def highlight(self):
        '''Called when the button is hovered over. Changes the color of the box.'''
        Button.highlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_gray.png').convert()

    def dehighlight(self):
        '''Called when the button is no longer hovered over. Changes the color of the box.'''
        Button.dehighlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_red.png').convert()

    def on_click(self):
        '''Called when this button is clicked. Nagivates to the Help "screen."'''
        def to_help():
            if self.box.y == -70:
                self.remove_update_function(function = to_help)
            else:
                self.app.slide_splash(y = -20)
                self.app.slide_help(y = -20)
        self.add_update_function(function = to_help)

class StartButton(Button):
    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_150px_red.png').convert(), x = 300, y = 230)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 42), text = 'Start', x = 300, y = 230, color = COLOR.WHITE, center_x = 150, center_y = 60)

    # ACTIONS
    def highlight(self):
        '''Called when the button is hovered over. Changes the color of the box.'''
        Button.highlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_gray.png').convert()

    def dehighlight(self):
        '''Called when the button is no longer hovered over. Changes the color of the box.'''
        Button.dehighlight(self)
        self.box.surface = pygame.image.load('res/img/button_150px_red.png').convert()

    def on_click(self):
        '''Called when this button is clicked. Nagivates to the Main "screen."'''
        def to_main():
            if self.box.y == -70:
                self.remove_update_function(function = to_main)
            else:
                self.app.slide_splash(y = -20)
                self.app.slide_main(y = -20)
        self.add_update_function(function = to_main)