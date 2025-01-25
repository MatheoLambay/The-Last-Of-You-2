import pygame
import math

class Player:
    def __init__(self,screen,link,x,y,life,attack,score=0):
        self.screen = screen

        self.original_image = pygame.image.load(link)
        self.original_image = pygame.transform.scale(self.original_image, (250 // 2, 250 // 2))

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.x = x
        self.y = y     
        self.life = life
        self.attack = attack
        self.score = score
        self.velocity = 2 
        self.angle = 0


    def Attack(self,cible):
        cible.life -= self.attack  
        
    def point_at(self, m_pos):
        
        # Calculate the angle to the mouse position
        dx, dy = m_pos[0] - self.rect.centerx, m_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))  # dy is positive because Pygame's y-axis increases downward
        
        # Adjust the angle if the default orientation is downward
        adjusted_angle = self.angle - 90  # Subtract 90 degrees if the sprite points down by default
        
        # Rotate the image
        rotated_image = pygame.transform.rotate(self.original_image, -adjusted_angle)  # Negative angle for Pygame's rotation direction
        
        # Update the rect to keep it centered
        self.image = rotated_image
        # self.image = pygame.transform.scale(self.image,(250/2,250/2))
        self.rect = self.image.get_rect(center=self.rect.center)

    
    def move(self,key,border):
        print(self.x)
        if key[pygame.K_z]:
            if self.y > 0:
                self.y -= 1 * self.velocity
            elif self.y == 0 and border["up"]:
                self.y = 1080
                return "u"
             
        if key[pygame.K_s]:
            if self.y < 1080:
                self.y += 1 * self.velocity
            elif self.y == 1080 and border["down"]:
                self.y = 0
                return "d"

        if key[pygame.K_d]:
            if self.x < 1920:
                self.x += 1 * self.velocity
            elif self.x == 1920 and border["right"]:
                self.x = 0
                return "r"
        
        if key[pygame.K_q]:
            if self.x > 0:
                self.x -= 1 * self.velocity
            elif self.x == 0 and border["left"]:
                self.x = 1920
                return "l"
            
        self.rect.center = (self.x,self.y)
        return None
    
            
    def draw(self):
        self.screen.blit(self.image,self.rect)

   