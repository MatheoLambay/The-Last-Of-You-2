import pygame
import json
from button import Button

class statMenu:
    def __init__(self,screen):
        self.screen = screen
        self.stat_img = pygame.image.load("img\main_menu\stat_btn.png").convert_alpha()
        self.statrect = self.stat_img.get_rect()
        self.statrect.topleft = (0,0)

        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.back_button = Button(self.screen,20,900,self.back_img,0.8)

        self.last_stat = self.statrect.bottomleft

        with open('data\stat.json','r') as f:
            self.data = json.load(f)
            print(self.data)

    def fade(self,screen,SCREENWIDTH, SCREENHEIGHT): 
        fade = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        fade.fill((0,0,0))
        opacity = 0
        for r in range(0, 30):
            opacity += 1
            fade.set_alpha(opacity)
            screen.blit(fade, (0,0))
            pygame.display.update() 
        for r in range(0, 30):
            opacity -= 1
            fade.set_alpha(opacity)
            screen.blit(fade, (0,0))
            pygame.display.update()

    def open(self, screen):
        screen.fill((0,0,0))

        screen.blit(self.stat_img, self.statrect)
       
        for i,j in self.data.items():
            data_font = pygame.font.Font('The Last Of Us Rough.ttf', 30)
            text = "%s : %i"%(i,j)
            data_text = data_font.render(text,True,(255,255,255))
            textRect = data_text.get_rect()
            textRect.topleft = (self.last_stat[0],self.last_stat[1])
            self.last_stat = textRect.bottomleft
            self.screen.blit(data_text, textRect)
        
        
        self.back_button.draw()
        


    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        if self.back_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.pop_menu()