import pygame
import math

class zombieSettings:
    def __init__(self,screen,body,arm,x,y):
        self.screen = screen

        self.zombie_body_img = pygame.image.load(body).convert_alpha()
        self.zombie_arm_img = pygame.image.load(arm).convert_alpha()
        self.x = x
        self.y = y
        

        self.zombie_body_img_rect = self.zombie_body_img.get_rect(midbottom=(self.x,self.y))
        self.zombie_arm_img_rect = self.zombie_arm_img.get_rect(center=(self.zombie_body_img_rect.center[0]-70,self.zombie_body_img_rect.center[1]+40))

        self.image = self.zombie_arm_img.copy()

        self.angle = 0

    
    
       
    def point_at(self, m_pos):
        if m_pos[0] < 1920//2-200:
            # Calculate the angle to the mouse position
            dx, dy = m_pos[0] - self.zombie_arm_img_rect.centerx, m_pos[1] - self.zombie_arm_img_rect.centery
            self.angle = math.degrees(math.atan2(dy, dx))  # dy is positive because Pygame's y-axis increases downward

            # Adjust the angle if the default orientation is downward
            adjusted_angle = self.angle - 180  # Subtract 180 degrees if the sprite points down by default

            # Rotate the image
            rotated_image = pygame.transform.rotate(self.zombie_arm_img, -adjusted_angle)  # Negative angle for Pygame's rotation direction

            # Update the rect to keep it centered
            self.image = rotated_image
            # self.image = pygame.transform.scale(self.image,(250/2,250/2))
            self.zombie_arm_img_rect = self.image.get_rect(center=self.zombie_arm_img_rect.center)

    def draw(self):
        self.screen.blit(self.image, self.zombie_arm_img_rect)
        self.screen.blit(self.zombie_body_img, self.zombie_body_img_rect)