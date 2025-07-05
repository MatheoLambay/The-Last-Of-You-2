
class upgrade:
    def __init__(self,name,description,amount,price,stat=None):
        
        self.name = name
        self.description = description
        self.amount = amount
        self.price = price
        self.stat = stat
      

    def apply(self,player):
        # Vérifie si le joueur a l'attribut à upgrader
        if hasattr(player, self.name):
            current = getattr(player, self.name)
            if current + self.amount > getattr(player,self.name+"_max"):
                setattr(player, self.name, getattr(player,self.name+"_max"))
            else:
                setattr(player, self.name, current + self.amount)
        else:
            print(f"L'attribut {self.name} n'existe pas sur le joueur.")

    def additem(self,player,damage=None,weapon_bullet=None):
        if hasattr(player, 'items'):
            for i in player.items:
                if i == 0:
                    player.items[player.items.index(i)] = {"name":self.name,"damage":self.stat[0],"weapon_bullet":self.stat[1],"range":self.stat[2],"link":self.stat[3]}
                    return 1
            return 0
        
        
        
