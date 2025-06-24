import pygame

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
        

    def collision(self,player):
        if player.rect.colliderect(self.rect):
            overlap_x = min(player.rect.right - self.rect.left, self.rect.right - player.rect.left)
            overlap_y = min(player.rect.bottom - self.rect.top, self.rect.bottom - player.rect.top)

            if overlap_x < overlap_y:  # Collision dominante sur l'axe horizontal
                if player.rect.centerx < self.rect.centerx:
                    player.x = self.rect.left - player.rect.width / 2
                else:
                    player.x = self.rect.right + player.rect.width / 2
            elif overlap_x > overlap_y:  # Collision dominante sur l'axe vertical
                if player.rect.centery < self.rect.centery:
                    player.y = self.rect.top - player.rect.height / 2
                else:
                    player.y = self.rect.bottom + player.rect.height / 2

            player.rect.center = (player.x, player.y)