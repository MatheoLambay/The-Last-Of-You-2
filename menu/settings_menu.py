import pygame
from button import Button
from menu.tools.map_touch import Touch
import json
from copy import deepcopy
from menu.tools.zombie_settings import zombieSettings

class settingsMenu:
    def __init__(self,screen):
        self.screen = screen

        with open('data\controls.json', 'r') as s:
            self.controls = json.load(s)
        self.controls_save = deepcopy(self.controls)

        with open('data\default_controls.json','r') as d:
            self.default_controls = json.load(d)

        self.title_img = pygame.image.load("img\settings_menu\menutitle.png").convert_alpha()
        self.titlerect = self.title_img.get_rect()
        self.titlerect.topleft = (0,0)

        self.background_img = pygame.image.load("img/settings_menu/bg.png").convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (1920, 1080))
        self.background_img_rect = self.background_img.get_rect(topleft=(0,0))

        self.back_img = pygame.image.load("img\settings_menu\goback_btn.png").convert_alpha()
        self.save_img = pygame.image.load("img\settings_menu\save_btn.png").convert_alpha()
        self.reset_img = pygame.image.load("img/settings_menu/reset_btn.png").convert_alpha()
        self.yes_img = pygame.image.load("img\settings_menu\YES.png").convert_alpha()
        self.no_img = pygame.image.load("img/settings_menu/NO.png").convert_alpha()
        self.cancel_img = pygame.image.load("img/settings_menu/cancel.png").convert_alpha()
        

        self.zombie = zombieSettings(self.screen,"img/settings_menu/zombie_body.png","img/settings_menu/zombie_arm.png",1920//2,1080)
        self.target_zombie_hide = self.zombie.zombie_body_img_rect.y + 1000
        self.target_zombie_show = self.zombie.zombie_body_img_rect.y

        self.leave_zombie_img = pygame.image.load("img\settings_menu\leave_alert.png").convert_alpha()
        self.leave_zombie_rect = self.leave_zombie_img.get_rect()
        self.leave_zombie_rect.midtop = (1920//2, 1080)

        self.target_leave_show = self.leave_zombie_rect.y - 600
        self.target_leave_hide = self.leave_zombie_rect.y 

        self.speed = 20
        
        self.back_button = Button(self.screen,20,900,self.back_img,0.8)
        self.save_button = Button(self.screen, self.back_button.rect.topright[0]+50, self.back_button.rect.topright[1], self.save_img, 0.8)
        self.reset_button = Button(self.screen, self.save_button.rect.topright[0]+50, self.save_button.rect.topright[1], self.reset_img, 0.8)

        self.yes_btn = Button(self.screen, self.leave_zombie_rect.center[0]-130, self.leave_zombie_rect.center[1]+100, self.yes_img)
        self.no_btn = Button(self.screen, self.leave_zombie_rect.center[0]+100, self.leave_zombie_rect.center[1]+100, self.no_img)
        self.cancel_btn = Button(self.screen, self.leave_zombie_rect.center[0]-40, self.leave_zombie_rect.center[1]+100, self.cancel_img)


        self.target_yes = (self.leave_zombie_rect.center[0]-130, self.leave_zombie_rect.center[1]+100)
        self.target_no = (self.leave_zombie_rect.center[0]+100, self.leave_zombie_rect.center[1]+100)
        self.target_cancel = (self.leave_zombie_rect.center[0], self.leave_zombie_rect.center[1]+100)

        self.current_touch = None
        self.change_detected = False
        
        self.touch_list = []
        
        x = 120
        y = self.titlerect.bottomleft[1]+20
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

    def reset_change(self):
        self.controls = deepcopy(self.default_controls)
        
        for i in range(len(self.touch_list)): 
           self.touch_list[i].touch[1] = list(self.controls.values())[i]
        
    def hide_zombie_point(self):
        if self.zombie.zombie_body_img_rect.y < self.target_zombie_hide:
            self.zombie.zombie_body_img_rect.y += self.speed
            self.zombie.zombie_arm_img_rect.y += self.speed
            if self.zombie.zombie_body_img_rect.y > self.target_zombie_hide:
                self.zombie.zombie_body_img_rect.y = self.target_zombie_hide 
                self.zombie.zombie_arm_img_rect.y = self.target_zombie_hide 
            return 0
        return 1

    def hide_zombie_leave(self):
        if self.leave_zombie_rect.y < self.target_leave_hide:
            self.leave_zombie_rect.y += self.speed
            self.yes_btn.rect[1] += self.speed
            self.no_btn.rect[1] += self.speed
            self.cancel_btn.rect[1] += self.speed
            if self.leave_zombie_rect.y > self.target_leave_hide:
                self.leave_zombie_rect.y = self.target_leave_hide  
                self.yes_btn.rect.center = self.target_yes
                self.no_btn.rect.center = self.target_no
                self.cancel_btn.rect.center = self.target_cancel
            return 0
        return 1

    def show_zombie_point(self):
         if self.zombie.zombie_body_img_rect.y > self.target_zombie_show:
            self.zombie.zombie_body_img_rect.y -= self.speed
            self.zombie.zombie_arm_img_rect.y -= self.speed
            if self.zombie.zombie_body_img_rect.y < self.target_zombie_show:
                self.zombie.zombie_body_img_rect.y = self.target_zombie_show 
                self.zombie.zombie_arm_img_rect.y = self.target_zombie_show

    def show_zombie_leave(self):
        if self.leave_zombie_rect.y > self.target_leave_show:
            self.leave_zombie_rect.y -= self.speed
            self.yes_btn.rect[1] -= self.speed
            self.no_btn.rect[1] -= self.speed
            self.cancel_btn.rect[1] -= self.speed
            if self.leave_zombie_rect.y < self.target_leave_show:
                self.leave_zombie_rect.y = self.target_leave_show  # Pour ne pas dépasser
                self.yes_btn.rect.center = self.target_yes
                self.no_btn.rect.center = self.target_no
                self.cancel_btn.rect.center = self.target_cancel
    
    def update(self, key, manager):
        """Met à jour les interactions du menu."""
        self.screen.fill((0,0,0))
        self.screen.blit(self.background_img, self.background_img_rect)
        self.screen.blit(self.title_img, self.titlerect)
        self.zombie.draw()
        self.zombie.point_at(pygame.mouse.get_pos())
        
        for i in self.touch_list:
            i.draw()
        
        if self.change_detected:
            #en bas zombie avec bras
            if(self.hide_zombie_point()):
                self.show_zombie_leave()

            self.screen.blit(self.leave_zombie_img, self.leave_zombie_rect)
            self.yes_btn.draw()
            self.no_btn.draw()
            self.cancel_btn.draw()

        else:
            if(self.hide_zombie_leave()):
                self.show_zombie_point()
            
            self.screen.blit(self.leave_zombie_img, self.leave_zombie_rect)
            self.yes_btn.draw()
            self.no_btn.draw()
            self.cancel_btn.draw()
            self.save_button.draw()
            self.reset_button.draw()

        
        self.back_button.draw()
        
        
        # detecte quelle touche est en cours de selection
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

        if self.save_button.detect() and not self.change_detected:
            self.save_change()
            for touch in self.touch_list:
                touch.color = "black"

        if self.yes_btn.detect():
            self.save_change()
            self.leave_menu(manager)

        if self.cancel_btn.detect():
            self.change_detected = False

        if self.no_btn.detect():
            self.leave_menu(manager)

        if self.reset_button.detect() and not self.change_detected:
            self.reset_change()
            for touch in self.touch_list:
                touch.color = "black"
            
        if self.back_button.detect():
            if self.controls_save != self.controls:
                self.change_detected = True
                for touch in self.touch_list:
                    if touch.touch[1] not in list(self.controls_save.values()):
                        touch.color = "red"
             
            else:
                self.leave_menu(manager)