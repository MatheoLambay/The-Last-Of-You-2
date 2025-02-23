import pygame
from button import Button
from game.game_manager import gameManager


class selectModeMenu:
    def __init__(self,screen):
        self.screen = screen
        self.wanted1 = pygame.image.load("img\select_mode_menu\wanted1.png").convert_alpha()
        self.wanted2 = pygame.image.load("img\select_mode_menu\wanted2.png").convert_alpha() 
        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.background_img = pygame.image.load("img\select_mode_menu\sbackground.png").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.back_button = Button(screen,20,900,self.back_img,0.8)
        self.classic_button = Button(screen,50,50,self.wanted1)

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

        self.back_button.draw()
        self.classic_button.draw()

    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        if self.back_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.pop_menu()
        
        if self.classic_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.push_menu(gameManager(self.screen))