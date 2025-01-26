import pygame

class dropBullet:
    def __init__(self,screen,link,x,y,map_x,map_y,amount,scale=1):
        self.screen = screen

        self.image = pygame.image.load(link)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.amount = amount
        self.map_x = map_x
        self.map_y = map_y

    def give_to(self,cible):
        cible.weapon_bullet += self.amount
    
    def draw(self):
        self.screen.blit(self.image,self.rect)





class dropTuna:
    def __init__(self):
        pass