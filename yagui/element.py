import pygame

class Element:
    '''An object that represents some grouped logic within an App, likely containing Drawables'''
    # INIT
    def __init__(self):
        self.frame = 0
        self.update_functions = []
        self.cleanup_functions = []

    # APP
    def set_app(self, app):
        '''Associates an App with this Element'''
        self.app = app
        self.on_app()

    # ACTIONS
    def key_down(self, key):
        pass

    def key_up(self, key):
        pass

    def mouse_down(self, button, pos):
        pass

    def mouse_up(self, button, pos):
        pass

    def mouse_move(self, pos):
        pass

    # UPDATE
    def update(self):
        '''Called every frame, handles the Element's logic'''
        for function in self.update_functions:
            function()
        self.frame += 1

    def add_update_function(self, function):
        self.update_functions.append(function)

    def remove_update_function(self, function):
        self.update_functions.remove(function)

    # CLEANUP
    def cleanup(self):
        '''Called when the App is closed, calls all cleanup functions'''
        for function in self.cleanup_functions:
            function()
    
    def add_cleanup_function(self, function):
        self.cleanup_functions.append(function)

    def remove_cleanup_function(self, function):
        self.cleanup_functions.remove(function)

    # DRAW
    def draw(self, area):
        pass

    # OVERRIDES
    def on_app(self):
        pass