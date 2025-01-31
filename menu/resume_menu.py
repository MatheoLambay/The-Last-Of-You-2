import pygame
from button import Button

class resumeMenu:
    def __init__(self,screen,total_killed,total_time,total_gold,upgrade):
        self.screen = screen
        self.title_img = pygame.image.load("img/resume_menu/resume.png").convert_alpha()
        self.title_rect = self.title_img.get_rect()

        
        self.background_img = pygame.image.load("img/resume_menu/background.webp").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.background_rect = self.background_img.get_rect()

        self.menu_img = pygame.image.load("img/resume_menu/menu.png").convert_alpha()
        self.menu_button = Button(self.screen,20,900,self.menu_img,0.8)

        self.divers_img = pygame.image.load("img/resume_menu/divers.png").convert_alpha()
        self.divers_rect = self.divers_img.get_rect()

        self.upgrade_img = pygame.image.load("img/resume_menu/upgrade.png").convert_alpha()
        self.upgrade_rect = self.upgrade_img.get_rect()

        self.stat = {"total killed":total_killed,"total time":total_time,"total gold":total_gold}
        self.upgrade = upgrade

        self.last_stat = self.divers_rect
        self.last_upgrade = self.upgrade_rect
        
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
       
        self.background_rect.topleft = (0,0)
        screen.blit(self.background_img, self.background_rect)

        self.title_rect.center = (1920/2,100)
        screen.blit(self.title_img, self.title_rect)

        self.divers_rect.topright = (self.title_rect.bottomleft[0],self.title_rect.bottomleft[1])
        screen.blit(self.divers_img, self.divers_rect)

        self.upgrade_rect.topleft = (self.title_rect.bottomright[0],self.title_rect.bottomright[1])
        screen.blit(self.upgrade_img, self.upgrade_rect)

        
        data_font = pygame.font.Font('freesansbold.ttf', 32)

        for i,j in self.stat.items():
            text = "%s : %i"%(i,j)
            data_text = data_font.render(text,True,(255,255,255))
            textRect = data_text.get_rect()
            textRect.topleft = (self.last_stat.bottomleft[0],self.last_stat.bottomleft[1])
            self.screen.blit(data_text, textRect)
            self.last_stat = textRect
            
        for i in self.upgrade:
            data_text = data_font.render(str(i),True,(255,255,255))
            textRect = data_text.get_rect()
            textRect.topleft = (self.last_upgrade.bottomleft[0],self.last_upgrade.bottomleft[1])
            self.screen.blit(data_text, textRect)
            self.last_upgrade = textRect
        
        self.menu_button.draw()

    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        if self.menu_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.go_home()
