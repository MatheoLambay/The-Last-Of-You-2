import pygame
import json
from button import Button

class codexMenu:
    def __init__(self,screen):
        self.screen = screen
        self.codex_img = pygame.image.load("img\codex_menu\codex.png").convert_alpha()
        self.codex_rect = self.codex_img.get_rect()
        self.codex_rect.center = (1920/2,100)

        self.background_img = pygame.image.load("img\settings_menu\sbackground.webp").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))

        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.back_button = Button(self.screen,20,900,self.back_img,0.8)

        self.left_img = pygame.image.load("img\codex_menu\gauche.png").convert_alpha()
        self.right_img = pygame.image.load("img\codex_menu\droite.png").convert_alpha()

        
        self.right_btn = None
        self.left_btn = None
        
        self.button_pressed = False

        with open("data\codex.json", 'r') as f:
            self.zombies = json.load(f)

        """liste nom zombie"""
        self.zombies_list = list(self.zombies)
        
        """list key zombie"""
        self.info_key = list(self.zombies[self.zombies_list[0]].keys())

        self.current_index = 0
        self.last_index = None
       
        

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
        
        
    

    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        

        if self.current_index != self.last_index:

            
            self.screen.fill((0,0,0))
            self.screen.blit(self.codex_img, self.codex_rect)

            data_font = pygame.font.Font('The Last Of Us Rough.ttf', 30)

            image = pygame.image.load(self.zombies[self.zombies_list[self.current_index]]["link"]).convert_alpha()
            image = pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2)))
            image_rect = image.get_rect()
            image_rect.center = (self.codex_rect.centerx,self.codex_rect.centery+image.get_height()/2+self.codex_img.get_height()/2)
            self.screen.blit(image,image_rect)
            space = 0
            

            for i in self.info_key:
                
                text = "%s : %s"%(i,self.zombies[self.zombies_list[self.current_index]][i])
                data_text = data_font.render(text,True,(255,255,255))
                textRect = data_text.get_rect()
                textRect.topleft = (image_rect.topright[0]+10,image_rect.topright[1]+space)
                self.screen.blit(data_text, textRect)
                space += image.get_height()/8
            self.last_index = self.current_index

            
            self.right_btn = Button(self.screen,image_rect.bottomright[0],image_rect.bottomright[1],self.right_img,0.3,"topright")
            self.left_btn = Button(self.screen,image_rect.bottomleft[0],image_rect.bottomleft[1],self.left_img,0.3)

            self.back_button.draw()

            if self.zombies_list.index(self.zombies_list[self.current_index]) == 0:
                self.right_btn.draw()

            elif self.zombies_list.index(self.zombies_list[self.current_index]) == len(self.zombies_list)-1:
                self.left_btn.draw()

            else: 
                self.left_btn.draw()
                self.right_btn.draw()
            

            
        if self.back_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.pop_menu()
        elif self.right_btn.detect() and not(self.button_pressed):
            self.fade(manager.screen,1920,1080)
            self.current_index +=1
            self.button_pressed = True

        elif self.left_btn.detect() and not(self.button_pressed):
            self.fade(manager.screen,1920,1080)
            self.current_index -=1
            self.button_pressed = True

        else:
            self.button_pressed = False


    # data_font = pygame.font.Font('The Last Of Us Rough.ttf', 30)
    #         text = "%s : %i"%(i,j)
    #         data_text = data_font.render(text,True,(255,255,255))
    #         textRect = data_text.get_rect()
    #         textRect.topleft = (self.last_stat[0],self.last_stat[1])
    #         self.last_stat = textRect.bottomleft
    #         self.screen.blit(data_text, textRect)
