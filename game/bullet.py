import pygame
import math

class Bullet:
    def __init__(self,screen,link,x,y,m_pos,scale=1):
        self.screen = screen
        self.original_image = pygame.image.load(link)
        width = self.original_image.get_width()
        height = self.original_image.get_height()

        self.original_image = pygame.transform.scale(self.original_image, (int(width * scale), int(height * scale)))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.angle = 0

        self.x = x
        self.y = y
        self.m_pos = m_pos

        # Calcul de la direction initiale
        dx = self.m_pos[0] - self.x
        dy = self.m_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            self.direction_x = dx / distance
            self.direction_y = dy / distance
        else:
            self.direction_x, self.direction_y = 0, 0  # Éviter division par zéro

        self.point_at()
        

    def point_at(self):
        # Calculate the angle to the mouse position
        dx, dy = self.m_pos[0] - self.rect.centerx, self.m_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))  # dy is positive because Pygame's y-axis increases downward
        
        # Adjust the angle if the default orientation is downward
        adjusted_angle = self.angle - 90  # Subtract 90 degrees if the sprite points down by default
        
        # Rotate the image
        rotated_image = pygame.transform.rotate(self.original_image, -adjusted_angle)  # Negative angle for Pygame's rotation direction
        
        # Update the rect to keep it centered
        self.image = rotated_image
        # self.image = pygame.transform.scale(self.image,(250/2,250/2))
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire(self):
       # Ajustement de la vitesse
        speed = 5  # Ajuster selon les besoins
        self.x += self.direction_x * speed
        self.y += self.direction_y * speed

        # Mise à jour de la position
        self.rect.center = (self.x, self.y)

        # # Si le sprite dépasse les limites de l'écran, gérer le comportement
        # screen_width, screen_height = self.screen.get_size()
        # if (self.x < 0 or self.x > screen_width or 
        #     self.y < 0 or self.y > screen_height):
        #     pass  # Supprimez ou réinitialisez le sprite ici si nécessaire

    def draw(self):
        self.screen.blit(self.image,self.rect)