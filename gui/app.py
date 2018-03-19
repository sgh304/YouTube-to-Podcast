# YAGUI
import pygame
import pyperclip
import os
import threading
from yagui import App, Element, Sprite, Label
from youtube import get_playlist_info, convert_playlist, PlaylistInfoException
from files import upload_to_vlc

class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

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
        self.app.get_element('splash').slide_up()

    # Draw
    def draw(self, area):
        self.box.draw(area)
        self.label.draw(area)

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
        self.app.to_main()

    # Draw
    def draw(self, area):
        self.box.draw(area)
        self.label.draw(area)

class TextEntryBox(Element):
    def __init__(self):
        Element.__init__(self)
        self.focused = False

    def on_app(self):
        Element.on_app(self)
        self.make_label()
        self.make_box()
        self.make_input()

    def key_down(self, key):
        if self.focused:
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

    def draw(self, area):
        self.label.draw(area)
        self.box.draw(area)
        self.input.draw(area)

class PlaylistEntryBox(TextEntryBox):
    def make_label(self):
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 32), text = 'YouTube Playlist URL', x = 50, y = 350, color = COLOR.BLACK, center_x = 400)
    
    def make_box(self):
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/box_400px.png').convert(), x = 50, y = 390)

    def make_input(self):
        self.input = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 20), text = '', x = 52, y = 394, color = COLOR.BLACK, limit_x = 396)

class UploadEntryBox(TextEntryBox):
    def make_label(self):
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 32), text = 'VLC Upload Address', x = 50, y = 440, color = COLOR.BLACK, center_x = 400)
    
    def make_box(self):
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/box_400px.png').convert(), x = 50, y = 480)

    def make_input(self):
        self.input = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 20), text = '', x = 52, y = 484, color = COLOR.BLACK, limit_x = 396)

class GoButton(Button):
    def __init__(self):
        Button.__init__(self)
        self.click_allowed = True

    def on_app(self):
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_150px_red.png').convert(), x = 175, y = 550)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 42), text = 'Go', x = 175, y = 550, color = COLOR.WHITE, center_x = 150, center_y = 60)

    # Actions
    def highlight(self):
        Button.highlight(self)
        if self.click_allowed:
            self.box.surface = pygame.image.load('res/img/button_150px_gray.png').convert()

    def dehighlight(self):
        Button.dehighlight(self)
        if self.click_allowed:
            self.box.surface = pygame.image.load('res/img/button_150px_red.png').convert()

    def allow_click(self):
        self.click_allowed = True
        self.label.text = 'Go'

    def disallow_click(self):
        self.click_allowed = False
        self.label.text = 'Wait...'

    def on_click(self):
        if self.click_allowed:
            threading.Thread(target = self.app.go).start()

    # Draw
    def draw(self, area):
        self.box.draw(area)
        self.label.draw(area)

class Warning(Element):
    def on_app(self):
        Element.on_app(self)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = '', x = 0, y = 330, color = COLOR.RED, center_x = 500)

    def draw(self, area):
        self.label.draw(area)

class YTPApp(App):
    def __init__(self):
        App.__init__(self)
        self.set_caption(caption = 'Youtube to Podcast')
        self.set_icon(icon_path = 'res/img/icon.png')
        self.background = self.add_element(element = Background())
        self.splash = self.add_element(element = Splash())
        self.help_button = self.add_element(element = HelpButton())
        self.start_button = self.add_element(element = StartButton())
        self.playlist_entry_box = self.add_element(element = PlaylistEntryBox())
        self.upload_entry_box = self.add_element(element = UploadEntryBox())
        self.go_button = self.add_element(element = GoButton())
        self.warning = self.add_element(element = Warning())
        self.going = False

    def to_help(self):
        pass

    def to_main(self):
        def slide_up():
            if self.splash.image.y <= -300:
                self.remove_element(element = self.splash)
                self.remove_element(element = self.help_button)
                self.remove_element(element = self.start_button)
            self.splash.image.y -= 20
            self.help_button.box.y -= 20
            self.help_button.label.y -= 20
            self.start_button.box.y -= 20
            self.start_button.label.y -= 20
            self.playlist_entry_box.label.y -= 20
            self.playlist_entry_box.box.y -= 20
            self.playlist_entry_box.input.y -= 20
            self.upload_entry_box.label.y -= 20
            self.upload_entry_box.box.y -= 20
            self.upload_entry_box.input.y -= 20
            self.go_button.box.y -= 20
            self.go_button.label.y -= 20
            self.warning.label.y -= 20
        self.splash.add_update_function(function = slide_up)

    def go(self):
        self.go_button.disallow_click = True
        playlist_url = self.playlist_entry_box.input.text
        upload_url = self.upload_entry_box.input.text

        try:
            if playlist_url:
                # Set up download environment
                playlist = get_playlist_info(playlist_url)
                playlist_folder = os.path.join('downloads', playlist.name)
                # Download
                convert_playlist(playlist = playlist, playlist_folder = playlist_folder)
                # Upload
                if upload_url:
                    upload_to_vlc(upload_url = upload_url, playlist_folder = playlist_folder)
        except PlaylistInfoException:
            self.warning.label.text = 'Error getting playlist info! Check the playlist URL.'
        finally:
            self.go_button.allow_click = True