import pygame

class upgrade:
    def __init__(self,name,amount):
        
        self.name = name
        self.amount = amount

    def apply(self,cible):
        print(self.name)
        if self.name == "increase max ammo":
            cible.weapon_bullet_max += self.amount
        elif self.name == "increase life max":
            cible.life_max += self.amount
        
        
