import pygame
from yagui import App, Element, Sprite
from gui.splash import Splash, HelpButton, StartButton
from gui.main import PlaylistEntryBox, UploadEntryBox, GoButton, WarningText, BackButton
from gui.help import HelpSplash, BackwardButton, ForwardButton

class YTPApp(App):
    '''App subclass for the YouTube to Podcast GUI. Made up of three "screens": the opening Splash, the Help slideshow,
    and the Main menu for the actual conversion process. The element classes of each "screen" can be found in their respective
    source code files.'''
    # INIT
    def __init__(self):
        App.__init__(self)
        # App setup
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

    # SPLASH
    def slide_splash(self, y):
        '''Slides all elements on the Splash "screen" vertically by the specified amount'''
        self.splash.image.y += y
        self.help_button.box.y += y
        self.help_button.label.y += y
        self.start_button.box.y += y
        self.start_button.label.y += y

    # HELP
    def slide_help(self, y):
        '''Slides all elements on the Help "screen" vertically by the specified amount'''
        self.help_splash.image.y += y
        self.backward_button.box.y += y
        self.backward_button.label.y += y
        self.forward_button.box.y += y
        self.forward_button.label.y += y

    # MAIN
    def slide_main(self, y):
        '''Slides all elements on the Main "screen" vertically by the specified amount'''
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

    def lock_inputs(self):
        '''Locks all inputs on the Main "screen" (while the conversion is ongoing)'''
        self.go_button.disallow_click()
        self.playlist_entry_box.disallow_input()
        self.upload_entry_box.disallow_input()

    def unlock_inputs(self):
        '''Unlocks all inputs on the Main "screen" (when the conversion is complete or stops prematurely)'''
        self.go_button.allow_click()
        self.playlist_entry_box.allow_input()
        self.upload_entry_box.allow_input()

class Background(Element):
    '''The background element for the app, drawn behind all other "screen" elements.'''
    # APP
    def on_app(self):
        '''Called when this element is associated with an app. Initializes drawables.'''
        Element.on_app(Element)
        surface = pygame.Surface((500, 300))
        surface.fill((255, 255, 255))
        self.image = Sprite(app = self.app, surface = surface, x = 0, y = 0)

    # DRAW
    def draw(self, area):
        '''Draws this element's drawables within the specified area onto the App's display.'''
        self.image.draw(area)