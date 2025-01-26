import pygame
import math

class Zombie:
    def __init__(self,screen,link,x,y,life,attack):
        self.screen = screen

        self.original_image = pygame.image.load(link)
        self.original_image = pygame.transform.scale(self.original_image, (90 // 1.5, 112 // 1.5))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.life = life
        self.attack = attack
        self.x = x
        self.y = y
        self.velocity = 0.5
        self.angle = 0
        


    def point_at(self,player_pos):
        
        # Calculate the angle to the mouse position
        dx, dy = player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))  # dy is positive because Pygame's y-axis increases downward
        
        # Adjust the angle if the default orientation is downward
        adjusted_angle = self.angle - 90  # Subtract 90 degrees if the sprite points down by default
        
        # Rotate the image
        rotated_image = pygame.transform.rotate(self.original_image, -adjusted_angle)  # Negative angle for Pygame's rotation direction
        
        # Update the rect to keep it centered
        self.image = rotated_image
        # self.image = pygame.transform.scale(self.image,(250/2,250/2))
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_to(self,targetx,targety):
        
        if targetx > self.x:
            self.x += 1 * self.velocity
        elif targetx < self.x:
            self.x -= 1 * self.velocity
        
        if targety > self.y:
           self.y += 1 * self.velocity
        elif targety < self.y:
            self.y -= 1 * self.velocity

        self.rect.center = (self.x,self.y)

    def draw(self):
        self.screen.blit(self.image,self.rect)