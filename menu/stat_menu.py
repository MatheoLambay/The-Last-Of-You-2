import pygame
import json
from button import Button

class statMenu:
    def __init__(self,screen):
        self.screen = screen
        self.stat_img = pygame.image.load("img\main_menu\stat_btn.png").convert_alpha()
        self.statrect = self.stat_img.get_rect()
        self.statrect.topleft = (0,0)

        self.background_img = pygame.image.load("img/stat_menu/bg.png").convert_alpha()
        self.background_img_rect = self.background_img.get_rect(topleft=(0,0))

        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.back_button = Button(self.screen,20,900,self.back_img,0.8)

        self.last_stat = self.statrect.bottomleft

        with open('data\stat.json','r') as f:
            self.data = json.load(f)
            print(self.data)

        self.xp = self.data["total xp"]
        self.lvl = 1
        self.max_xp = self.get_next_lvl_xp()

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

    def get_level(self):
        if self.xp >= self.max_xp:
            self.lvl += 1
            self.xp -= self.max_xp
            self.max_xp = self.get_next_lvl_xp()
            
    def get_next_lvl_xp(self):
        return int(1000 * (1.9**self.lvl - 1.9**(self.lvl-1)))

    def open(self, screen):
        screen.fill((0,0,0))
        self.screen.blit(self.background_img, self.background_img_rect)
        screen.blit(self.stat_img, self.statrect)
       
        for i,j in self.data.items():
            data_font = pygame.font.Font('The Last Of Us Rough.ttf', 30)
            text = "%s : %i"%(i,j)
            data_text = data_font.render(text,True,(255,255,255))
            textRect = data_text.get_rect()
            textRect.topleft = (self.last_stat[0],self.last_stat[1])
            self.last_stat = textRect.bottomleft
            self.screen.blit(data_text, textRect)
        
        self.get_level()
        font = pygame.font.Font('freesansbold.ttf', 30)
        name_text = font.render("LEVEL "+str(self.lvl),True,(255,255,255))
        textRect = name_text.get_rect()
        textRect.topleft = (100,1080-300)
        ratio = self.xp / self.max_xp
        pygame.draw.rect(self.screen,"white",(textRect.bottomleft[0],textRect.bottomleft[1],(1920-200),40),width=5)
        pygame.draw.rect(self.screen,"yellow",(textRect.bottomleft[0]+5,textRect.bottomleft[1]+5,(1920-200)*ratio,30))
        self.screen.blit(name_text, textRect)
       
        self.back_button.draw()




    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        if self.back_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.pop_menu()