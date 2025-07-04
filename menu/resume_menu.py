import pygame
from button import Button
import json

class resumeMenu:
    def __init__(self,screen,zombie_killed,total_time,total_gold,upgrade,xp):
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

        self.stat = {"total time":total_time,"total gold":total_gold}
        self.total_killed = 0

        for i,j in zombie_killed.items():
            self.stat[i] = j
            self.total_killed += j
        self.stat["total killed"] = self.total_killed
        self.upgrade = upgrade

        self.xp = xp
        print("xp: " + str(self.xp))
        self.lvl = 1
        self.max_xp = self.get_next_lvl_xp()
        
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

        
        data_font = pygame.font.Font('The Last Of Us Rough.ttf', 32)

        for i,j in self.stat.items():
            text = "%s : %i"%(i,j)
            data_text = data_font.render(text,True,(255,255,255))
            textRect = data_text.get_rect()
            textRect.topleft = (self.last_stat.bottomleft[0],self.last_stat.bottomleft[1])
            self.screen.blit(data_text, textRect)
            self.last_stat = textRect
            
        for i,j in self.upgrade.items():
            text = "%s : %ix"%(i,j)
            data_text = data_font.render(text,True,(255,255,255))
            textRect = data_text.get_rect()
            textRect.topleft = (self.last_upgrade.bottomleft[0],self.last_upgrade.bottomleft[1])
            self.screen.blit(data_text, textRect)
            self.last_upgrade = textRect

        self.menu_button.draw()

    def get_level(self):
        if self.xp >= self.max_xp:
            self.lvl += 1
            self.xp -= self.max_xp
            self.max_xp = self.get_next_lvl_xp()
            
    def get_next_lvl_xp(self):
        return int(1000 * (1.9**self.lvl - 1.9**(self.lvl-1)))
        
    
    def close(self):
        pass

    def update(self, event, manager):
        """Met à jour les interactions du menu."""
        # self.screen.fill((255,255,255))
       
        # self.background_rect.topleft = (0,0)
        # self.screen.blit(self.background_img, self.background_rect)

        # self.title_rect.center = (1920/2,100)
        # self.screen.blit(self.title_img, self.title_rect)

        # self.divers_rect.topright = (self.title_rect.bottomleft[0],self.title_rect.bottomleft[1])
        # self.screen.blit(self.divers_img, self.divers_rect)

        # self.upgrade_rect.topleft = (self.title_rect.bottomright[0],self.title_rect.bottomright[1])
        # self.screen.blit(self.upgrade_img, self.upgrade_rect)

        self.get_level()

        font = pygame.font.Font('freesansbold.ttf', 30)
        name_text = font.render("LEVEL "+str(self.lvl),True,(255,255,255))
        textRect = name_text.get_rect()
        textRect.topleft = (100,1080-300)
        ratio = self.xp / self.max_xp
        pygame.draw.rect(self.screen,"white",(textRect.bottomleft[0],textRect.bottomleft[1],(1920-200),40),width=5)
        pygame.draw.rect(self.screen,"yellow",(textRect.bottomleft[0]+5,textRect.bottomleft[1]+5,(1920-200)*ratio,30))
        self.screen.blit(name_text, textRect)
        
        
        if self.menu_button.detect():
            self.fade(manager.screen,1920,1080)
            manager.go_home()
