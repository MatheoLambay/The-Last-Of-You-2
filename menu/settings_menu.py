import pygame
from button import Button
from menu.tools.map_touch import Touch
import json
from copy import deepcopy

class settingsMenu:
    def __init__(self,screen):
        self.screen = screen

        with open('data\controls.json', 'r') as s:
            self.controls = json.load(s)

        self.controls_save = deepcopy(self.controls)

        self.title_img = pygame.image.load("img\settings_menu\menutitle.png").convert_alpha()
        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.save_img = pygame.image.load("img\settings_menu\save_btn.png").convert_alpha()
        self.yes_img = pygame.image.load("img\settings_menu\YES.png").convert_alpha()
        self.no_img = pygame.image.load("img/settings_menu/NO.png").convert_alpha()
        
        self.titlerect = self.title_img.get_rect()
        self.titlerect.topleft = (0,0)
        

        self.background_img = pygame.image.load("img\settings_menu\sbackground.webp").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))

        self.leave_img = pygame.image.load("img\settings_menu\leave_alert.png").convert_alpha()
        self.leave_rect = self.leave_img.get_rect()
        self.leave_rect.midbottom = (1920 // 2, 1080)
        
        self.back_button = Button(self.screen,20,900,self.back_img,0.8)
        self.save_button = Button(self.screen, self.back_button.rect.topright[0], self.back_button.rect.topright[1], self.save_img, 0.8)
        self.yes_btn = Button(self.screen, self.leave_rect.center[0]-130, self.leave_rect.center[1]+100, self.yes_img)
        self.no_btn = Button(self.screen, self.leave_rect.center[0]+100, self.leave_rect.center[1]+100, self.no_img)

        self.current_touch = None
        self.change_detected = False
        
        self.touch_list = []
        
        x = 200
        y = 400
        for i in self.controls.items():
            self.touch_list.append(Touch(self.screen, i,x,y))
            y+=60

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
        
        pass


    def close(self):
        pass

    def save_change(self):
        with open('data\controls.json', 'w') as s:
            json.dump(self.controls, s, indent=4)
        self.controls_save = deepcopy(self.controls)
        
    def leave_menu(self, manager):

        self.fade(manager.screen,1920,1080)
        manager.pop_menu()


    def update(self, key, manager):
        """Met à jour les interactions du menu."""
        self.screen.fill((0,0,0))

        self.screen.blit(self.title_img, self.titlerect)

        for i in self.touch_list:
            i.draw()
        
        if self.change_detected:
           
            self.screen.blit(self.leave_img, self.leave_rect)
            self.yes_btn.draw()
            self.no_btn.draw()

        self.save_button.draw()
        self.back_button.draw()
        
        # detecte quelle touch est en cours de selection
        for i in self.touch_list:
            if i.detect():
                self.current_touch = i
                break
        
        # met à jour l'affichage des touches
        for i in self.touch_list:
            if i == self.current_touch:
                i.draw_select_touch()
            else:
                i.draw_default_touch()


        if key is not None and pygame.key.name(key) == "escape" :
            self.current_touch.draw_default_touch()
            self.current_touch = None

        elif key is not None and self.current_touch is not None:
            if pygame.key.name(key) in self.controls.values():
                self.current_touch.draw_default_touch()
                self.current_touch = None
            else:      
                self.current_touch.set_new_touch(pygame.key.name(key))
                self.current_touch.draw_default_touch()
                self.controls[self.current_touch.touch[0]] = self.current_touch.touch[1]
                self.current_touch = None
        
    
        if self.save_button.detect():
            self.save_change()

        if self.yes_btn.detect():
            self.save_change()
            self.leave_menu(manager)

        if self.no_btn.detect():
            self.leave_menu(manager)

        if self.back_button.detect():
            if self.controls_save != self.controls:
                self.change_detected = True
            else:
                self.leave_menu(manager)
        


