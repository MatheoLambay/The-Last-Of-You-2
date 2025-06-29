import pygame
from button import Button
from game.game_manager import gameManager
from menu.tools.map_ping import Pin
import json


class selectMapMenu:
    def __init__(self,screen,player):
        self.screen = screen
        self.player = player

        with open('data\players.json', 'r') as p:
            self.players_stats = json.load(p)

        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.background_img = pygame.image.load("img\select_mode_menu\map.png").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.back_button = Button(screen,20,900,self.back_img,0.8)


        self.pin1 = Pin(self.screen,200,200,(("img\game\map1.png","img\game\map2.png"),("img\game\map3.png","img\game\map4.png")))
        self.pin2 = Pin(self.screen,300,300,(("img\game\map1.png",),("img\game\map2.png",),("img\game\map3.png",),("img\game\map4.png",)))
        self.pins = (self.pin1,self.pin2)
        

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
        screen.fill((255,255,255))
        backgroungrect = self.background_img.get_rect()
        backgroungrect.topleft = (0,0)
        screen.blit(self.background_img, backgroungrect)
        for i in self.pins:
            i.draw()
        self.back_button.draw()

        
    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        if self.back_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.pop_menu()
        
        for i in self.pins:
            if i.detect():
                self.fade(manager.screen,1920,1080)
                manager.push_menu(gameManager(self.screen,self.player,i.maps_cases))

       