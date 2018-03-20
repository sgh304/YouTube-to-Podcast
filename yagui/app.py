import sys, pygame
from yagui.util import get_smallest_rect

class App:
    def __init__(self):
        pygame.init()
        # State
        self.running = False
        self.clock = pygame.time.Clock()
        # Display
        self.display_buffer = pygame.Surface((500, 300))
        self.display = pygame.display.set_mode((500, 300))
        self.redraw_areas = []
        # Elements
        self.elements = []

    # Main Loop
    def start(self):
        self.running = True
        while self.running:
            self.process_events()
            self.update_elements()
            self.redraw_display()
            self.clock.tick(60)
        for element in self.elements:
            element.cleanup()

    def process_events(self):
        for event in pygame.event.get():
            # Window events
            if event.type == pygame.QUIT:
                self.running = False
            # Action events
            elif event.type == pygame.KEYDOWN:
                for element in self.elements:
                    element.key_down(key = event.key)
            elif event.type == pygame.KEYUP:
                for element in self.elements:
                    element.key_up(key = event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for element in self.elements:
                    element.mouse_down(button = event.button, pos = event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                for element in self.elements:
                    element.mouse_up(button = event.button, pos = event.pos)
            elif event.type == pygame.MOUSEMOTION:
                for element in self.elements:
                    element.mouse_move(pos = event.pos)

    def update_elements(self):
        for element in self.elements:
            element.update()

    def redraw_display(self):
        if self.redraw_areas:
            redraw_area = get_smallest_rect(self.redraw_areas)
            for element in self.elements:
                element.draw(redraw_area)
            pygame.transform.scale(self.display_buffer, (self.display.get_width(), self.display.get_height()), self.display)
            pygame.display.update()
            self.redraw_areas = []

    # Display
    def redraw_area(self, area):
        self.redraw_areas.append(area)

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, icon_path):
        pygame.display.set_icon(pygame.image.load(icon_path))

    # Elements
    def add_element(self, element):
        element.set_app(app = self)
        self.elements.append(element)
        return element

    def remove_element(self, element):
        self.elements.remove(element)