import pygame
import json
import random
from button import Button
from game.upgrade import upgrade


class shopMenu:
    def __init__(self,screen,player):
        self.screen = screen
        self.player = player

        

        self.background_img = pygame.image.load("img\game\shopbackgorund.jpg").convert_alpha()
        self.bg_rect = self.background_img.get_rect()
        self.bg_rect.center = (1920/2,1080/2)

        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png")
        self.back_button = Button(self.screen,self.bg_rect.bottomright[0],self.bg_rect.bottomright[1],self.back_img,0.8,"bottomright")
        

        self.random_upgrade = []
        self.current_upgrade = []

        with open('game/upgrade.json','r') as f:
            self.data = json.load(f)
       
        self.selectUpgrade()
        
        

    def selectUpgrade(self):
        space = 0
        for i in range(4):
            self.random_upgrade.append(random.choice(list(self.data)))
        
        """création des boutons et des images"""
        for i in self.random_upgrade:
            image = pygame.image.load(self.data[i]["link"]).convert_alpha()
            button = Button(self.screen,self.bg_rect.topleft[0]+space,self.bg_rect.topleft[1],image,0.1)
            space += 200
            up = upgrade(self.data[i]["description"],self.data[i]["amont"],self.data[i]["price"])
            self.current_upgrade.append((button,up))
        
        
    def open(self, screen):
        
    
        screen.blit(self.background_img, self.bg_rect)  

        self.back_button.draw()
        for i in self.current_upgrade:
            i[0].draw()

            text = pygame.font.Font('freesansbold.ttf', 20)

            desc_text = text.render(str(i[1].name),True,(255,215,0))
            descRect = desc_text.get_rect()
            descRect.topleft = (i[0].rect.bottomleft[0],i[0].rect.bottomleft[1])

            price_text = text.render(str(i[1].price),True,(255,0,0))
            priceRect = price_text.get_rect()
            priceRect.topleft = (descRect.bottomleft[0],descRect.bottomleft[1])

            self.screen.blit(price_text, priceRect)
            self.screen.blit(desc_text, descRect)


    def close(self):
        pass


    def update(self, event, manager):
         
        

        """Met à jour les interactions du menu."""
        if self.back_button.detect():
           
            manager.pop_menu()

        for i in self.current_upgrade:
            if i[0].detect():
                if self.player.gold >= i[1].price:
                    i[1].apply(self.player)
                else:
                    print('no money')
            
            