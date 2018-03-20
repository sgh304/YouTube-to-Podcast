import pygame

class Element:
    def __init__(self):
        self.frame = 0
        self.update_functions = []
        self.cleanup_functions = []

    # App
    def set_app(self, app):
        self.app = app
        self.on_app()

    # Actions
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

    # Update
    def update(self):
        for function in self.update_functions:
            function()
        self.frame += 1

    def add_update_function(self, function):
        self.update_functions.append(function)

    def remove_update_function(self, function):
        self.update_functions.remove(function)

    # Cleanup
    def cleanup(self):
        for function in self.cleanup_functions:
            function()
    
    def add_cleanup_function(self, function):
        self.cleanup_functions.append(function)

    def remove_cleanup_function(self, function):
        self.cleanup_functions.remove(function)

    # Draw
    def draw(self, area):
        pass

    # Overrides
    def on_app(self):
        pass