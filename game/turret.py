import pygame
import math

class Turret(pygame.sprite.Sprite):
    def __init__(self,screen,link,x,y,map_x,map_y,attack,weapon_bullet,range,scale=2):
        super().__init__()
        self.screen = screen
       
        
        self.original_image = pygame.image.load(link).convert_alpha()
        width = self.original_image.get_width()
        height = self.original_image.get_height()

        self.original_image = pygame.transform.scale(self.original_image, (int(width * scale), int(height * scale)))
        self.image = self.original_image.copy()  # <- IMPORTANT : copie nette

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x = x
        self.y = y 
        self.map_x = map_x
        self.map_y = map_y

        self.angle = 0
        self.last_angle = None

        self.attack = attack
        self.weapon_bullet = weapon_bullet
        self.range = range

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
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        angle = math.degrees(math.atan2(-dy, dx))  # -dy car pygame Y va vers le bas

        if self.last_angle is None or abs(angle - self.last_angle) > 1:
            self.last_angle = angle

            adjusted_angle = angle + 90  # Ajuste selon orientation sprite

            rotated_image = pygame.transform.rotate(self.original_image, adjusted_angle)

            self.image = rotated_image
            self.rect = self.image.get_rect(center=(self.x, self.y))


    def update(self, zombies, new_bullet_func):
        if self.weapon_bullet <= 0:
            self.kill()
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_time < self.bullet_interval:
            return  # attendre le cooldown

        # Trouver le zombie le plus proche dans le range
        closest_zombie = None
        closest_dist = float('inf')

        for z in zombies:
            if z.life <= 0:
                continue

            dx = z.x - self.x
            dy = z.y - self.y
            dist = math.hypot(dx, dy)

            if dist < self.range and dist < closest_dist:
                closest_zombie = z
                closest_dist = dist

        if closest_zombie:
            # Vise et tire
            self.point_at((closest_zombie.x, closest_zombie.y))
            new_bullet_func((closest_zombie.x, closest_zombie.y), self)
            self.last_bullet_time = current_time



    def draw(self):
        pygame.draw.circle(self.screen, "red", (self.x,self.y), self.range, width=1)
        # pygame.draw.circle(self.screen, "white", (self.x,self.y), self.range-10)
        self.screen.blit(self.image,self.rect)

