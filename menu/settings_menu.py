import pygame
from button import Button

class settingsMenu:
    def __init__(self,screen):
        self.screen = screen
        self.title_img = pygame.image.load("img\settings_menu\menutitle.png").convert_alpha()
        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.background_img = pygame.image.load("img\settings_menu\sbackground.webp").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.back_button = Button(self.screen,20,900,self.back_img,0.8)

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

        titlerect = self.title_img.get_rect()
        titlerect.topleft = (0,1080/100)
        screen.blit(self.title_img, titlerect)
        
        self.back_button.draw()

    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        if self.back_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.pop_menu()

