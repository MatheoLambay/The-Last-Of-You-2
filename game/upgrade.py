import pygame

class upgrade:
    def __init__(self,name,description,amount,price):
        
        self.name = name
        self.description = description
        self.amount = amount
        self.price = price

    def apply(self,player):
        # Vérifie si le joueur a l'attribut à upgrader
        if hasattr(player, self.name):
            current = getattr(player, self.name)
            setattr(player, self.name, current + self.amount)
        else:
            print(f"L'attribut {self.name} n'existe pas sur le joueur.")

    def additem(self,player):
        if hasattr(player, 'items'):
            for i in player.items:
                if i == 0:
                    player.items[player.items.index(i)] = self.name
                    return
        
        
        
