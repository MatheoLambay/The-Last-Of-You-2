import pygame
from game.shop import shopMenu


class ShopPnj:
    def __init__(self,screen,link,x,y,map_x,map_y,name,scale=1):

        self.screen = screen
        self.name = name

        self.image = pygame.image.load(link).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        self.zone_image = pygame.image.load("img\game\zonesafe.png").convert_alpha()
        width = self.zone_image.get_width()
        height = self.zone_image.get_height()
        self.zone_image = pygame.transform.scale(self.zone_image, (int(width * scale), int(height * scale)))
        self.zone_rect = self.zone_image.get_rect()
        self.zone_rect.center = (x,y)

        self.rect.center = (x,y)
        self.x = x
        self.y = y 

        self.map_x = map_x
        self.map_y = map_y
     

    def draw(self):
        self.screen.blit(self.zone_image, self.zone_rect)
        self.screen.blit(self.image,self.rect)
        
    def openShop(self,manager,player):
        manager.push_menu(shopMenu(self.screen, player))