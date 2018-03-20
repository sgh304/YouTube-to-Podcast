import pygame

def redraw(func):
    def with_redraw(self, *args, **kwargs):
        self.app.redraw_area(self.rect)
        func(self, *args, **kwargs)
        self.app.redraw_area(self.rect)
    return with_redraw

class Drawable:
    def __init__(self, app):
        self.app = app

    def __del__(self):
        self.app.redraw_area(self.rect)

    def force_redraw(self):
        self.app.redraw_area(self.rect)

    def draw(self, area):
        if not (self.rect.right < area.left) and not (self.rect.bottom < area.top) and not (self.rect.left > area.right) and not (self.rect.top > area.bottom):
            position = pygame.Rect(max(self.rect.left, area.left), max(self.rect.top, area.top), 0, 0)
            area = pygame.Rect(max(0, area.left - self.rect.left), max(0, area.top - self.rect.top), min(self.surface.get_width(), area.right - position.left), min(self.surface.get_height(), area.bottom - position.top))
            self.app.display_buffer.blit(self.surface, position, area)

class Sprite(Drawable):
    def __init__(self, app, surface, x, y):
        Drawable.__init__(self, app = app)
        self._surface = surface
        self._x = x
        self._y = y
        self.app.redraw_area(self.rect)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())

    @property
    def x(self):
        return self._x

    @x.setter
    @redraw
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    @redraw
    def y(self, y):
        self._y = y

    @property
    def surface(self):
        return self._surface

    @surface.setter
    @redraw
    def surface(self, surface):
        self._surface = surface

class Label(Drawable):
    def __init__(self, app, font, text, x, y, color = (0, 0, 0), center_x = None, center_y = None, limit_x = None):
        Drawable.__init__(self, app = app)
        self._font = font
        self._text = text
        self._x = x
        self._y = y
        self._color = color
        self._center_x = center_x
        self._center_y = center_y
        self._limit_x = limit_x
        self.make_surface()
        self.app.redraw_area(self.rect)

    @property
    def rect(self):
        return pygame.Rect(self.x + ((self.center_x or self.surface.get_width()) - self.surface.get_width()) / 2, self.y + ((self.center_y or self.surface.get_height()) - self.surface.get_height()) / 2, self.surface.get_width(), self.surface.get_height())

    @property
    def font(self):
        return self._font

    @font.setter
    @redraw
    def font(self, font):
        self._font = font
        self.make_surface()

    @property
    def text(self):
        return self._text

    @text.setter
    @redraw
    def text(self, text):
        self._text = text
        self.make_surface()

    @property
    def x(self):
        return self._x

    @x.setter
    @redraw
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    @redraw
    def y(self, y):
        self._y = y

    @property
    def color(self):
        return self._color

    @color.setter
    @redraw
    def color(self, color):
        self._color = color

    @property
    def center_x(self):
        return self._center_x

    @center_x.setter
    @redraw
    def center_x(self, center_x):
        self._center_x = center_x

    @property
    def center_y(self):
        return self._center_y

    @center_y.setter
    @redraw
    def center_y(self, center_y):
        self._center_y = center_y

    @property
    def limit_x(self):
        return self._limit_x

    @limit_x.setter
    @redraw
    def limit_x(self, limit_x):
        self._limit_x = limit_x

    def make_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        if self.limit_x and self.surface.get_width() > self.limit_x:
            self.surface = self.surface.subsurface(pygame.Rect(self.surface.get_width() - self.limit_x, 0, self.limit_x, self.surface.get_height()))