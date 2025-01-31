import pygame
from button import Button

class mainMenu:
    def __init__(self,screen):
        self.screen = screen
        self.title_img = pygame.image.load("img\main_menu\menutitle.png").convert_alpha()
        self.exit_img = pygame.image.load("img\main_menu\exit_btn.png").convert_alpha()
        self.start_img = pygame.image.load("img\main_menu\start_btn.png").convert_alpha()
        self.settings_img = pygame.image.load("img\main_menu\settings_btn.png").convert_alpha()
        self.background_img = pygame.image.load("img\main_menu\mbackground.png").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.stat_img = pygame.image.load("img\main_menu\stat_btn.png").convert_alpha()
        self.codex_img = pygame.image.load("img\main_menu\codex_btn.png").convert_alpha()

        self.start_button = Button(self.screen,1920/100,200,self.start_img)
        self.stat_button = Button(self.screen,1920/100,350,self.stat_img)
        self.settings_button = Button(self.screen,1920/100,500,self.settings_img)
        self.codex_button = Button(self.screen,1920/100,650,self.codex_img)

        self.exit_button = Button(self.screen,20,900,self.exit_img,0.8)
        

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
        self.settings_button.draw()
        self.stat_button.draw()
        self.codex_button.draw()
        self.exit_button.draw()

            

    def close(self):
        pass

    def update(self, event, manager):
        if self.exit_button.detect():
            pygame.quit()
            quit()
            
        if self.settings_button.detect():
            from menu.settings_menu import settingsMenu
            self.fade(manager.screen,1920,1080)
            manager.push_menu(settingsMenu(self.screen))

        if self.stat_button.detect():
            from menu.stat_menu import statMenu
            self.fade(manager.screen,1920,1080)
            manager.push_menu(statMenu(self.screen))

        if self.codex_button.detect():
            pass

        if self.start_button.detect():
            self.fade(manager.screen,1920,1080)
            from menu.select_menu import selectModeMenu
            manager.push_menu(selectModeMenu(self.screen))
        