import pygame
import math

class Player:
    def __init__(self,screen,link,x,y,life,attack,velocity,weapon_bullet_max,attack_cooldown,range_item):
       
        self.screen = screen

        self.original_image = pygame.image.load(link)
        self.original_image = pygame.transform.scale(self.original_image, (250 // 2, 250 // 2))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.angle = 0

        self.x = x
        self.y = y     
        self.life_max = life
        self.life = self.life_max

        self.attack = attack
        self.velocity = velocity
        self.weapon_bullet_max = weapon_bullet_max
        self.weapon_bullet = self.weapon_bullet_max
        self.attack_cooldown = attack_cooldown
        self.alive = 1
        self.direction = None
        self.can_attack = 1
        self.gold = 0
        self.score = 0

        self.lvl = 1
        self.xp = 0
        self.max_xp = self.get_next_lvl_xp()

        self.items = [0,0,0]

        self.player_in_market = 0 
        self.player_just_bought = 0
        self.range_item = range_item
        self.current_upgrade = {}

    def get_level(self,new_xp):
        self.xp += new_xp
        if self.xp >= self.max_xp:
            self.lvl += 1
            self.xp = 0
            self.max_xp = self.get_next_lvl_xp()

    def get_next_lvl_xp(self):
        return int(1000 * (1.1**self.lvl - 1.1**(self.lvl-1)))

    def point_at(self, m_pos):
        if self.alive:
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
        
        if self.alive:
            if key[pygame.K_z]:
                self.direction = "u"
                if self.y > 0:
                    self.y -= 1 * self.velocity
                elif self.y <= 0 and border["up"]:
                    self.y = 1080
                    return "u"
                    
            if key[pygame.K_s]:
                self.direction = "d"
                if self.y < 1080:
                    self.y += 1 * self.velocity
                elif self.y >= 1080 and border["down"]:
                    self.y = 0
                    return "d"

            if key[pygame.K_d]:
                self.direction = "r"
                if self.x < 1920:
                    self.x += 1 * self.velocity
                elif self.x >= 1920 and border["right"]:
                    self.x = 0
                    return "r"
            
            if key[pygame.K_q]:
                self.direction = "l"
                if self.x > 0:
                    self.x -= 1 * self.velocity
                elif self.x <= 0 and border["left"]:
                    self.x = 1920
                    return "l"
            
            self.rect.center = (self.x,self.y)
            return None
     
    def Attack(self,cible):
        if self.alive:
            cible.life -= self.attack

    
    def draw(self):
        self.screen.blit(self.image,self.rect)

