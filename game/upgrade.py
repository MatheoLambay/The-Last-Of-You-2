import pygame

class upgrade:
    def __init__(self,name,amount,price):
        
        self.name = name
        self.amount = amount
        self.price = price

    def apply(self,cible):
        
        if self.name == "increase max ammo":
            cible.weapon_bullet_max += self.amount
        elif self.name == "increase life max":
            cible.life_max += self.amount
        elif self.name == "increase damage":
            cible.attack += self.amount
        elif self.name == "increase velocity":
            cible.velocity += self.amount
        
        
        
