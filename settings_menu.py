import pygame
from button import Button

class settingsMenu:
    def __init__(self):
        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.background_img = pygame.image.load("img\settings_menu\sbackground.webp").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.back_button = Button(1000,200,self.back_img,0.8)

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
        # pygame.font.init()
        # title = pygame.font.Font('freesansbold.ttf', 32)
        # title_text = title.render("settings",True,(255, 0, 0))
        # textRect = title_text.get_rect()
        # textRect.center = (1920/2,50)
        # screen.blit(title_text, textRect)

    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        if self.back_button.draw(manager.screen):
            self.fade(manager.screen,1920,1080)
            manager.pop_menu()

