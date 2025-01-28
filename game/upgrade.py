import pygame

class upgrade:
    def __init__(self,name,description,amount,price):
        
        self.name = name
        self.description = description
        self.amount = amount
        self.price = price

    def apply(self,cible):
        
        if self.name == "max_ammo":
            cible.weapon_bullet_max += self.amount
        elif self.name == "max_life":
            cible.life_max += self.amount
        elif self.name == "increase_damage":
            cible.attack += self.amount
        elif self.name == "increase_velocity":
            cible.velocity += self.amount
        
        
        
