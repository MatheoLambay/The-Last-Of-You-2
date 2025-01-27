import pygame

class dropItems:
    def __init__(self,screen,link,x,y,map_x,map_y,amount,name,interval,scale=1):
        self.screen = screen
        self.name = name
        self.image = pygame.image.load(link)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y 
        self.amount = amount
        self.map_x = map_x
        self.map_y = map_y

        self.last_damage_time = pygame.time.get_ticks()
        self.damage_interval = interval

    def give_ammo_to(self,cible):
        cible.weapon_bullet += self.amount
        if cible.weapon_bullet > cible.weapon_bullet_max:
            cible.weapon_bullet = cible.weapon_bullet_max
        
    def give_life_to(self,cible):
        cible.life += self.amount
    
    def draw(self):
        self.screen.blit(self.image,self.rect)

