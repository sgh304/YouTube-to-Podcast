import pygame, threading, os
from yagui import Element, Sprite, Label
from gui.elements import Button, TextEntryBox
from gui.constants import *
from files import upload_to_vlc
from youtube import get_playlist_info, PlaylistInfoException, start_download_video_audio_process
from webdriver import TimeoutException

class PlaylistEntryBox(TextEntryBox):
    '''The text entry box where the user inputs the link to the YouTube playlist they wish to convert to a podcast.'''
    # APP
    def make_label(self):
        '''Called when this text entry box is associated with an App, creates the label drawable'''
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 32), text = 'YouTube Playlist URL', x = 50, y = 330, color = COLOR.BLACK, center_x = 400)
    
    def make_box(self):
        '''Called when this text entry box is associated with an App, creates the box drawable'''
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/box_400px.png').convert(), x = 50, y = 370)

    def make_input(self):
        '''Called when this text entry box is associated with an App, creates the input drawable'''
        self.input = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 20), text = '', x = 52, y = 374, color = COLOR.BLACK, limit_x = 396)

class UploadEntryBox(TextEntryBox):
    '''The text entry box where the user inputs the address to which the podcast files can be uploaded to the VLC app.'''
    # APP
    def make_label(self):
        '''Called when this text entry box is associated with an App, creates the label drawable'''
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 32), text = 'VLC Upload Address', x = 50, y = 420, color = COLOR.BLACK, center_x = 400)
    
    def make_box(self):
        '''Called when this text entry box is associated with an App, creates the box drawable'''
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/box_400px.png').convert(), x = 50, y = 460)

    def make_input(self):
        '''Called when this text entry box is associated with an App, creates the input drawable'''
        self.input = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 20), text = '', x = 52, y = 464, color = COLOR.BLACK, limit_x = 396)

class GoButton(Button):
    '''The button that starts the conversion process'''
    # INIT
    def __init__(self):
        Button.__init__(self)
        self.click_allowed = True

    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_150px_red.png').convert(), x = 175, y = 530)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 42), text = 'Go', x = 175, y = 530, color = COLOR.WHITE, center_x = 150, center_y = 60)

    # Actions
    def highlight(self):
        '''Called when the button is hovered over. Changes the color of the box.'''
        Button.highlight(self)
        if self.click_allowed:
            self.box.surface = pygame.image.load('res/img/button_150px_gray.png').convert()

    def dehighlight(self):
        '''Called when the button is no longer hovered over. Changes the color of the box.'''
        Button.dehighlight(self)
        if self.click_allowed:
            self.box.surface = pygame.image.load('res/img/button_150px_red.png').convert()

    def allow_click(self):
        '''Allows the button to be clicked.'''
        self.click_allowed = True
        self.label.text = 'Go'

    def disallow_click(self):
        '''Disallows the button to be clicked.'''
        self.click_allowed = False
        self.label.text = 'Wait...'

    def on_click(self):
        '''Called when this button is clicked. Begins the conversion process.'''
        if self.click_allowed:
            self.app.warning_text.label.text = ''
            self.app.lock_inputs()
            self.get_playlist_info()

    # CONVERSION
    def get_playlist_info(self):
        '''Creates a thread that retrieves playlist info from the input playlist URL, and continues the conversion process when complete or
        terminates the process with an error.'''
        def get_playlist_info_then_download():
            try:
                playlist = get_playlist_info(url = self.app.playlist_entry_box.input.text)
                self.download_playlist(playlist = playlist)
            except PlaylistInfoException:
                self.app.warning_text.label.text = 'Error getting playlist info! Check the playlist URL.'
                self.app.unlock_inputs()
        # Get playlist info with a thread so that the main event loop isn't blocked.
        threading.Thread(target = get_playlist_info_then_download).start()

    def download_playlist(self, playlist):
        '''Creates a youtube-dl processes that download the audio of each video in a YouTube playlist, and continues the conversion process
        when complete or terminates the process with an error. The youtube-dl subprocesses will automatically close if the conversion process
        is canceled by the user by either closing the App window or pressing the back button.'''
        playlist_folder = os.path.join('downloads', playlist.name)
        processes = []
        # Start a youtube-dl subprocess for each video
        for video in playlist.videos:
            video_path = os.path.join(playlist_folder, video.name) + '.%(ext)s'
            process = start_download_video_audio_process(url = video.url, path = video_path)
            processes.append(process)
        # Add an update function that checks the processes' statuses periodically
        def check_download_status():
            for process in processes:
                if process.poll() == None: # At least one process is still executing
                    return
                elif process.poll() != 0: # At least one process terminated with an error
                    self.app.warning_text.label.text = 'Error downloading a video! Check the playlist.'
                    self.remove_update_function(function = check_download_status)
                    self.remove_cleanup_function(function = kill_processes)
                    self.app.unlock_inputs()
                    return
            # All processes have completed successfully
            self.remove_update_function(function = check_download_status)
            self.remove_cleanup_function(function = kill_processes)
            self.upload_podcast(playlist_folder = playlist_folder)
        self.add_update_function(function = check_download_status)
        # Add a cleanup function that terminates all subprocesses if the App window is closed
        def kill_processes():
            for process in processes:
                if not process.poll():
                    process.kill()
        self.add_cleanup_function(function = kill_processes)

    def upload_podcast(self, playlist_folder):
        '''Creates a thread that uploads the downloaded playlist to the VLC app through the input address, updating the warning
        if there is an error. If no address was provided, the conversion process is complete.'''
        def upload_podcast_then_finish():
            if not self.app.upload_entry_box.input.text:
                self.app.unlock_inputs()
            else:
                try:
                    upload_to_vlc(upload_url = self.app.upload_entry_box.input.text, playlist_folder = playlist_folder)
                except TimeoutException:
                    self.app.warning_text.label.text = 'Error upoading to VLC. Check the address and your internet.'
                    self.app.unlock_inputs()
        threading.Thread(target = upload_podcast_then_finish).start()

class WarningText(Element):
    '''An element that displays warning messages if the conversion process fails for some reason.'''
    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Element.on_app(self)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = '', x = 0, y = 310, color = COLOR.RED, center_x = 500)

    # DRAW
    def draw(self, area):
        '''Draws this element's drawables within the specified area onto the App's display.'''
        self.label.draw(area)

class BackButton(Button):
    '''A button that returns the user to the Splash "screen" when clicked.'''
    # APP
    def on_app(self):
        '''Called when this element is associated with an App. Initializes drawables.'''
        Button.on_app(self)
        self.box = Sprite(app = self.app, surface = pygame.image.load('res/img/button_75px_gray.png').convert(), x = 415, y = 310)
        self.label = Label(app = self.app, font = pygame.font.Font('res/font/Oswald-Regular.ttf', 16), text = 'Back', x = 415, y = 310, color = COLOR.WHITE, center_x = 75)

    # ACTION
    def on_click(self):
        '''Called when this button is clicked. Navigates to the Splash "screen" and cancels any in-progress conversion.'''
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