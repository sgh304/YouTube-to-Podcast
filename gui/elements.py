import pygame, pyperclip
from yagui import Element, Sprite, Label

class Button(Element):
    def on_app(self):
        self.highlighted = False

    # Actions
    def mouse_move(self, pos):
        if self.box.rect.collidepoint(pos):
            if not self.highlighted:
                self.highlight()
        else:
            if self.highlighted:
                self.dehighlight()

    def highlight(self):
        self.highlighted = True

    def dehighlight(self):
        self.highlighted = False

    def mouse_down(self, button, pos):
        if self.box.rect.collidepoint(pos):
            self.on_click()

    # Draw
    def draw(self, area):
        self.box.draw(area)
        self.label.draw(area)

class TextEntryBox(Element):
    def __init__(self):
        Element.__init__(self)
        self.focused = False
        self.input_allowed = True

    def on_app(self):
        Element.on_app(self)
        self.make_label()
        self.make_box()
        self.make_input()

    def allow_input(self):
        self.input_allowed = True

    def disallow_input(self):
        self.input_allowed = False

    def key_down(self, key):
        if self.focused and self.input_allowed:
            key_to_char = {pygame.K_a: 'a', pygame.K_b: 'b', pygame.K_c: 'c', pygame.K_d: 'd', pygame.K_e: 'e', pygame.K_f: 'f', pygame.K_g: 'g',
                pygame.K_h: 'h', pygame.K_i: 'i', pygame.K_j: 'j', pygame.K_k: 'k', pygame.K_l: 'l', pygame.K_m: 'm', pygame.K_n: 'n', pygame.K_o: 'o',
                pygame.K_p: 'p', pygame.K_q: 'q', pygame.K_r: 'r', pygame.K_s: 's', pygame.K_t: 't', pygame.K_u: 'u', pygame.K_v: 'v', pygame.K_w: 'w',
                pygame.K_x: 'x', pygame.K_y: 'y', pygame.K_z: 'z', pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3', pygame.K_4: '4',
                pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8', pygame.K_9: '9', pygame.K_SPACE: ' '}
            if key in key_to_char:
                self.input.text += key_to_char[key]
            elif key == pygame.K_BACKSPACE:
                self.input.text = self.input.text[:-1]

    def mouse_down(self, button, pos):
        if button == 1 and self.box.rect.collidepoint(pos):
            self.focused = True
        elif self.focused:
            self.focused = False
        if button == 3 and self.box.rect.collidepoint(pos):
            self.input.text = pyperclip.paste()

    # Draw
    def draw(self, area):
        self.label.draw(area)
        self.box.draw(area)
        self.input.draw(area)
