import pygame

class Pnj:
    def __init__(self,screen,link,x,y,map_x,map_y,name,attack,hitbox,scale=1):
        self.screen = screen
        self.name = name
        self.image = pygame.image.load(link).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y 
        self.map_x = map_x
        self.map_y = map_y
        self.attack = attack
        self.hitbox = hitbox
        self.weapon_bullet = 100
        self.range = 200

    def in_zone(self,cible):
        if cible.x > self.x - self.range and cible.x < self.x + self.range and cible.y > self.y - self.range and cible.y < self.y + self.range:
            return True
        return False

    def draw(self):
        if self.attack > 0:
            pygame.draw.circle(self.screen, "red", (self.x,self.y), self.range)
            pygame.draw.circle(self.screen, "white", (self.x,self.y), self.range-10)
            
        self.screen.blit(self.image,self.rect)