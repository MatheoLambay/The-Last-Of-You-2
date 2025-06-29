import pygame
from button import Button

class Pin(Button):
    def __init__(self,screen,x,y,map_cases):
        pin = pygame.image.load("img\select_mode_menu\pin.png").convert_alpha()
        super().__init__(screen, x, y, pin)
        self.screen = screen
        self.x = x
        self.y = y
        self.maps_cases = map_cases
        