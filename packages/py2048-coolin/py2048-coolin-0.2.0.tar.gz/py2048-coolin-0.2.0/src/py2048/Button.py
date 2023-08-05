import pygame as pyg

class Button(object):
    ALL_CLICKS = 0
    FIRST_CLICK = 1
    RELEASE = 2

    def __init__(self, rect, normal_color, hover_color, when_active):
        self.rect = rect

        self.normal_color =  normal_color
        self.hover_color = hover_color
        self.current_color = normal_color
        self.active_on = when_active
        self.waiting = False

    def check_hover(self):
        if self.rect.collidepoint(pyg.mouse.get_pos()):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.normal_color

    def check_click(self):
        if self.check_hover() and pyg.mouse.get_pressed()[0]:
            if self.active_on == Button.ALL_CLICKS:
                return True
            elif self.active_on == Button.FIRST_CLICK and not self.waiting:
                self.waiting = True
                return True
            elif self.active_on == Button.RELEASE:
                self.waiting = True
                return False
        elif self.waiting: #Mouse not hovering and not pressed but waiting flag is set
            waiting = False
            if self.active_on == Button.RELEASE:
                return True

    def draw(self):
        return pyg.draw.rect(pyg.display.get_surface(), self.current_color, self.rect)
