import pygame
import math

class Turret(pygame.sprite.Sprite):
    def __init__(self,screen,link,x,y,map_x,map_y,attack,scale=1):
        super().__init__()
        self.screen = screen
       
        
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

        self.angle = 0
        self.last_angle = None

        self.attack = attack
        self.weapon_bullet = 10
        self.range = 200

        self.last_bullet_time = 0
        self.bullet_interval = 1000 

    def detect(self,cible):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_time >= self.bullet_interval:
            if cible.x > self.x - self.range and cible.x < self.x + self.range and cible.y > self.y - self.range and cible.y < self.y + self.range:
                self.last_bullet_time = current_time 
                return True
        return False
    
    def point_at(self, pos):
        dx = pos[0] - self.rect.centerx
        dy = pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        
        if self.last_angle is None or abs(angle - self.last_angle) > 2:
            self.last_angle = angle
            adjusted_angle = angle - 90
            self.image = pygame.transform.rotate(self.image, -adjusted_angle)
            self.rect = self.image.get_rect(center=self.rect.center)


    def update(self, cible):
        
        if self.weapon_bullet > 0:
            pass
            # self.point_at((cible.x, cible.y))
        else:
            self.kill()


    def draw(self):
        pygame.draw.circle(self.screen, "red", (self.x,self.y), self.range)
        pygame.draw.circle(self.screen, "white", (self.x,self.y), self.range-10)
        self.screen.blit(self.image,self.rect)

