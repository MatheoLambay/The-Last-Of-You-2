import pygame
from button import Button

class mainMenu:
    def __init__(self):
        self.title_img = pygame.image.load("img\main_menu\menutitle.png").convert_alpha()
        self.exit_img = pygame.image.load("img\main_menu\exit_btn.png").convert_alpha()
        self.start_img = pygame.image.load("img\main_menu\start_btn.png").convert_alpha()
        self.background_img = pygame.image.load("img\main_menu\mbackground.png").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.start_button = Button(1920/2,300,self.start_img,0.8)
        self.exit_button = Button(60,1000,self.exit_img,0.8)

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
            

    def open(self,screen):
        screen.fill((255,255,255))
        titlerect = self.title_img.get_rect()
        titlerect.center = (1920/2,1080/10)
        backgroungrect = self.background_img.get_rect()
        backgroungrect.topleft = (0,0)
        screen.blit(self.background_img, backgroungrect)
        screen.blit(self.title_img, titlerect)
        

    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        
        if self.exit_button.draw(manager.screen):
            pygame.quit()
            quit()
        if self.start_button.draw(manager.screen):
            from settings_menu import settingsMenu
            self.fade(manager.screen,1920,1080)
            manager.push_menu(settingsMenu())