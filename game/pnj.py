import pygame

class SellerPnj:
    def __init__(self,screen,link,x,y,map_x,map_y,name,attack,scale=1):
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
        self.map_x = map_x
        self.map_y = map_y
        self.attack = attack

    def Attack(self):
        pass
    """icccicicicicicicicicicicicici"""

    def draw(self):
        self.screen.blit(self.image,self.rect)