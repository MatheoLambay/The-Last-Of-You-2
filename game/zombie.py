import pygame

class Zombie:
    def __init__(self,life,attack,x,y):
        self.life = life
        self.attack = attack
        self.x = x
        self.y = y

    def Attack(self,cible):
        cible.life -= self.attack

