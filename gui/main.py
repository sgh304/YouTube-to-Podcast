import pygame, threading, os
from yagui import Element, Sprite, Label
from gui.elements import Button, TextEntryBox
from gui.constants import *
from files import upload_to_vlc
from youtube import get_playlist_info, PlaylistInfoException, start_download_video_audio_process
from webdriver import TimeoutException

class PlaylistEntryBox(TextEntryBox):
    def make_label(self):
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 32), text = 'YouTube Playlist URL', x = 50, y = 330, color = COLOR.BLACK, center_x = 400)
    
    def make_box(self):
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/box_400px.png').convert(), x = 50, y = 370)

    def make_input(self):
        self.input = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 20), text = '', x = 52, y = 374, color = COLOR.BLACK, limit_x = 396)

class UploadEntryBox(TextEntryBox):
    def make_label(self):
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 32), text = 'VLC Upload Address', x = 50, y = 420, color = COLOR.BLACK, center_x = 400)
    
    def make_box(self):
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/box_400px.png').convert(), x = 50, y = 460)

    def make_input(self):
        self.input = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 20), text = '', x = 52, y = 464, color = COLOR.BLACK, limit_x = 396)

class GoButton(Button):
    def __init__(self):
        Button.__init__(self)
        self.click_allowed = True

    def on_app(self):
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_150px_red.png').convert(), x = 175, y = 530)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 42), text = 'Go', x = 175, y = 530, color = COLOR.WHITE, center_x = 150, center_y = 60)

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
            self.app.warning_text.label.text = ''
            self.app.lock_inputs()
            self.get_playlist_info()

    def get_playlist_info(self):
        def get_playlist_info_then_download():
            try:
                playlist = get_playlist_info(url = self.app.playlist_entry_box.input.text)
                self.download_playlist(playlist = playlist)
            except PlaylistInfoException:
                self.app.warning_text.label.text = 'Error getting playlist info! Check the playlist URL.'
                self.app.unlock_inputs()
        threading.Thread(target = get_playlist_info_then_download).start()

    def download_playlist(self, playlist):
        playlist_folder = os.path.join('downloads', playlist.name)
        processes = []
        for video in playlist.videos:
            video_path = os.path.join(playlist_folder, video.name) + '.%(ext)s'
            process = start_download_video_audio_process(url = video.url, path = video_path)
            processes.append(process)
        def check_download_status():
            for process in processes:
                if process.poll() == None:
                    return
                elif process.poll() != 0:
                    self.app.warning_text.label.text = 'Error downloading a video! Check the playlist.'
                    self.remove_update_function(function = check_download_status)
                    self.remove_cleanup_function(function = kill_processes)
                    self.app.unlock_inputs()
                    return
            self.remove_update_function(function = check_download_status)
            self.remove_cleanup_function(function = kill_processes)
            self.upload_podcast(playlist_folder = playlist_folder)
        self.add_update_function(function = check_download_status)
        def kill_processes():
            for process in processes:
                if not process.poll():
                    process.kill()
        self.add_cleanup_function(function = kill_processes)

    def upload_podcast(self, playlist_folder):
        def upload_podcast_then_finish():
            if not self.app.upload_entry_box.input.text:
                self.app.warning_text.label.text = 'Error upoading to VLC. Check the address and your internet.'
                self.app.unlock_inputs()
            try:
                upload_to_vlc(upload_url = self.app.upload_entry_box.input.text, playlist_folder = playlist_folder)
            except TimeoutException:
                self.app.warning_text.label.text = 'Error upoading to VLC. Check the address and your internet.'
                self.app.unlock_inputs()
        threading.Thread(target = upload_podcast_then_finish).start()

class WarningText(Element):
    def on_app(self):
        Element.on_app(self)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = '', x = 0, y = 310, color = COLOR.RED, center_x = 500)

    def draw(self, area):
        self.label.draw(area)

class BackButton(Button):
    def on_app(self):
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_75px_gray.png').convert(), x = 415, y = 310)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = 'Back', x = 415, y = 310, color = COLOR.WHITE, center_x = 75)

    def on_click(self):
        if not self.app.go_button.click_allowed:
            for cleanup_function in self.app.go_button.cleanup_functions:
                cleanup_function()
        def to_splash():
            if self.box.y == 310:
                self.remove_update_function(function = to_splash)
            else:
                self.app.slide_splash(y = 20)
                self.app.slide_main(y = 20)
        self.add_update_function(function = to_splash)