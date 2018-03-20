import pygame, functools
from yagui import App
from gui.splash import Background, Splash, HelpButton, StartButton
from gui.main import PlaylistEntryBox, UploadEntryBox, GoButton, WarningText, BackButton
from gui.help import HelpSplash, BackwardButton, ForwardButton

class YTPApp(App):
    def __init__(self):
        App.__init__(self)
        # Window
        self.set_caption(caption = 'Youtube to Podcast')
        self.set_icon(icon_path = 'res/img/icon.png')
        # Background
        self.background = self.add_element(element = Background())
        # Splash
        self.splash = self.add_element(element = Splash())
        self.help_button = self.add_element(element = HelpButton())
        self.start_button = self.add_element(element = StartButton())
        # Main
        self.playlist_entry_box = self.add_element(element = PlaylistEntryBox())
        self.upload_entry_box = self.add_element(element = UploadEntryBox())
        self.go_button = self.add_element(element = GoButton())
        self.warning_text = self.add_element(element = WarningText())
        self.back_button = self.add_element(element = BackButton())
        # Help
        self.help_splash = self.add_element(element = HelpSplash())
        self.backward_button = self.add_element(element = BackwardButton())
        self.forward_button = self.add_element(element = ForwardButton())

    def lock_inputs(self):
        self.go_button.disallow_click()
        self.playlist_entry_box.disallow_input()
        self.upload_entry_box.disallow_input()

    def unlock_inputs(self):
        self.go_button.allow_click()
        self.playlist_entry_box.allow_input()
        self.upload_entry_box.allow_input()

    def slide_splash(self, y):
        self.splash.image.y += y
        self.help_button.box.y += y
        self.help_button.label.y += y
        self.start_button.box.y += y
        self.start_button.label.y += y

    def slide_main(self, y):
        self.playlist_entry_box.label.y += y
        self.playlist_entry_box.box.y += y
        self.playlist_entry_box.input.y += y
        self.upload_entry_box.label.y += y
        self.upload_entry_box.box.y += y
        self.upload_entry_box.input.y += y
        self.go_button.box.y += y
        self.go_button.label.y += y
        self.warning_text.label.y += y
        self.back_button.box.y += y
        self.back_button.label.y += y

    def slide_help(self, y):
        self.help_splash.image.y += y
        self.backward_button.box.y += y
        self.backward_button.label.y += y
        self.forward_button.box.y += y
        self.forward_button.label.y += y