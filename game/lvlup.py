import pygame
import random
import json
from button import Button


class LvLup:
    def __init__(self,screen,player):
        self.screen = screen
        self.player = player

        self.background_img = pygame.image.load("img\game\shopbackgorund.jpg").convert_alpha()
        self.bg_rect = self.background_img.get_rect()
        self.bg_rect.center = (1920/2,1080/2)
        
        self.all_powers = [Mine(screen),Speed(),Life(),Ammo()]
        self.selected_powers = []
        self.finals_powers = []

    def open(self, screen):
        nbr = random.randint(10,100)
        for p in self.all_powers:
            if p.drop >= nbr:
                self.selected_powers.append(p)

        x = self.bg_rect.topleft[0] + 50
        y = self.bg_rect.topleft[1] + 30
        for i in range(3):
            self.finals_powers.append((Button(self.screen,x,y,pygame.image.load("img/game/lvlup_menu/affiche.png")),random.choices(self.selected_powers)))
            x+=300
        self.screen.blit(self.background_img, self.bg_rect)
        
        x = self.bg_rect.topleft[0] + 50
        y = self.bg_rect.topleft[1] + 30
        data_font = pygame.font.Font('The Last Of Us Rough.ttf', 40)
        for i in self.finals_powers:
            
            i[0].draw()
            gold_text = data_font.render(i[1][0].name, True, (255,255,255))
            goldRect = gold_text.get_rect(topleft = (x+10,y+10))
            self.screen.blit(gold_text, goldRect)
            x+=300

            
    def close(self):
        pass
        
    def update(self, event, manager):
        """Met à jour les interactions du menu et affiche tout."""
        for i in self.finals_powers:
            if i[0].detect():
                if i[1][0].type == "stat":
                    if hasattr(self.player, i[1][0].name):
                        current = getattr(self.player, i[1][0].name)
                        setattr(self.player, i[1][0].name, current + i[1][0].amount)
                    else:
                        print(f"L'attribut {i[1][0].name} n'existe pas sur le joueur.")

                elif i[1][0].type == "power":
                    if hasattr(self.player, 'powers'):
                        for i in self.player.powers:
                            self.player.powers.add(i[1][0])
                self.player.player_level_up = 0
                manager.pop_menu()  
                print("just pop")           

      


class Mine:
    def __init__(self,screen):
        self.name = "Mine"
        self.type = "power"
        self.attack = 2
        self.drop = 20

    def update():
        pass  

class TP:
    def __init__(self,screen):
        self.name = "TP"
        self.type = "power"
        self.attack = 10
        self.drop = 10

    def update():
        pass  



class Speed:
    def __init__(self):
        self.name = "velocity"
        self.type = "stat"
        self.amount = 0.1
        self.drop = 80

class Life:
    def __init__(self):
        self.name = "life_max"
        self.type = "stat"
        self.amount = 1
        self.drop = 80

class Ammo:
    def __init__(self):
        self.name = "weapon_bullet_max"
        self.type = "stat"
        self.amount = 10
        self.drop = 80 
    
class RangeItem:
    def __init__(self):
        self.name = "range_item"
        self.type = "stat"
        self.amount = 10
        self.drop = 80

   



