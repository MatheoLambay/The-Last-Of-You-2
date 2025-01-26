import pygame

class HealthBar:
    def __init__(self,screen,x,y,w,h,max_hp):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def move(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(self.screen,"red",(self.x,self.y,self.w,self.h))
        pygame.draw.rect(self.screen,"green",(self.x,self.y,self.w*ratio,self.h))