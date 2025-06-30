import pygame
from button import Button

class presentationMenu:
    def __init__(self,screen):
        self.screen = screen
        self.title_img = pygame.image.load("img\main_menu\menutitle.png").convert_alpha()
        self.start_img = pygame.image.load("img\main_menu\start_btn.png").convert_alpha()
        self.background_img = pygame.image.load("img\main_menu\presentation.png").convert_alpha()
       
        self.start_button = Button(self.screen,1920//2,1080//2,self.start_img)
       
       
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
        
        backgroungrect = self.background_img.get_rect()
        backgroungrect.topleft = (0,0)
        screen.blit(self.background_img, backgroungrect)
        titlerect = self.title_img.get_rect()
        titlerect.center = (1920/2,1080/10)
        screen.blit(self.title_img, titlerect)

        self.start_button.draw()
       
            

    def close(self):
        pass

    def update(self, event, manager):
     
        if self.start_button.detect():
            self.fade(self.screen,1920,1080)
            from menu.main_menu import mainMenu
            manager.push_menu(mainMenu(self.screen))
        