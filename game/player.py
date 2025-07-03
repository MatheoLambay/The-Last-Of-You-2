import pygame
import math
import json

class Player(pygame.sprite.Sprite):
    def __init__(self,screen,link,x,y,life,attack,velocity,weapon_bullet_max,attack_cooldown,range_item):
       
        self.screen = screen
        self.x = x
        self.y = y     
        self.life_max = life
        self.life = self.life_max

        self.attack = attack
        self.velocity = velocity
        self.weapon_bullet_max = weapon_bullet_max
        self.weapon_bullet = self.weapon_bullet_max
        self.attack_cooldown = attack_cooldown

        with open('data\controls.json', 'r') as c:
            self.controls = json.load(c)

        self.up = self.controls["up"]
        self.down = self.controls["down"]
        self.left = self.controls["left"]
        self.right = self.controls["right"]

        self.original_image = pygame.image.load(link)
        self.original_image = pygame.transform.scale(self.original_image, (250 // 2, 250 // 2))
        self.image = self.original_image

        #interval et animation càc joueur
        self.frame_index = 0
        self.last_frame_time = 0
        self.frame_interval = 50
        self.cac_attack = 0
        self.cac_touched = []
        
        # self.hitbox = pygame.draw.rect(self.screen,"red",(self.x-self.original_image.get_height()//2,self.y-self.original_image.get_width()//2,self.original_image.get_height(),self.original_image.get_width()),10)
        self.hitbox = pygame.Rect(self.x-self.original_image.get_height()//2,self.y-self.original_image.get_width()//2,self.original_image.get_height(),self.original_image.get_width())
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.angle = 0
        self.adjusted_angle = 0

        self.is_alive = 1
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
        return int(1000 * (1.5**self.lvl - 1.5**(self.lvl-1)))

    def point_at(self, m_pos):
        if self.alive:
            # Calculate the angle to the mouse position
            dx, dy = m_pos[0] - self.rect.centerx, m_pos[1] - self.rect.centery
            self.angle = math.degrees(math.atan2(dy, dx))  # dy is positive because Pygame's y-axis increases downward
            
            # Adjust the angle if the default orientation is downward
            self.adjusted_angle = self.angle - 90  # Subtract 90 degrees if the sprite points down by default
            
            # Rotate the image
            rotated_image = pygame.transform.rotate(self.original_image, -self.adjusted_angle)  # Negative angle for Pygame's rotation direction
            
            # Update the rect to keep it centered
            self.image = rotated_image
            # self.image = pygame.transform.scale(self.image,(250/2,250/2))
            self.rect = self.image.get_rect(center=self.rect.center)

    
    def move(self,border):
        
        if self.alive:
            if pygame.key.get_pressed()[pygame.key.key_code(self.up)]:
                self.direction = "u"
                if self.y > 0:
                    self.y -= 1 * self.velocity
                elif self.y <= 0 and border["up"]:
                    self.y = 1080
                    return "u"
                    
            if pygame.key.get_pressed()[pygame.key.key_code(self.down)]:
                self.direction = "d"
                if self.y < 1080:
                    self.y += 1 * self.velocity
                elif self.y >= 1080 and border["down"]:
                    self.y = 0
                    return "d"

            if pygame.key.get_pressed()[pygame.key.key_code(self.right)]:
                self.direction = "r"
                if self.x < 1920:
                    self.x += 1 * self.velocity
                elif self.x >= 1920 and border["right"]:
                    self.x = 0
                    return "r"
            
            if pygame.key.get_pressed()[pygame.key.key_code(self.left)]:
                self.direction = "l"
                if self.x > 0:
                    self.x -= 1 * self.velocity
                elif self.x <= 0 and border["left"]:
                    self.x = 1920
                    return "l"
            
            self.rect.center = (self.x,self.y)
            self.hitbox = pygame.Rect(self.x-self.original_image.get_height()//2,self.y-self.original_image.get_width()//2,self.original_image.get_height(),self.original_image.get_width())
            return None
     
    def collision(self, rect2):
        # Gère le cas où rect2 est un pygame.Rect directement
        target_rect = rect2.rect if hasattr(rect2, 'rect') else rect2

        if self.hitbox.colliderect(target_rect):
            overlap_x = min(self.hitbox.right - target_rect.left, target_rect.right - self.hitbox.left)
            overlap_y = min(self.hitbox.bottom - target_rect.top, target_rect.bottom - self.hitbox.top)

            if overlap_x < overlap_y:  # Collision dominante sur l'axe horizontal
                if self.hitbox.centerx < target_rect.centerx:
                    self.x = target_rect.left - self.hitbox.width / 2
                else:
                    self.x = target_rect.right + self.hitbox.width / 2
            else:  # Collision dominante sur l'axe vertical
                if self.hitbox.centery < target_rect.centery:
                    self.y = target_rect.top - self.hitbox.height / 2
                else:
                    self.y = target_rect.bottom + self.hitbox.height / 2

            # Mettre à jour la hitbox après repositionnement
            self.hitbox = pygame.Rect(
                self.x - self.original_image.get_height() // 2,
                self.y - self.original_image.get_width() // 2,
                self.original_image.get_height(),
                self.original_image.get_width()
            )

    def cac_Attack(self,combined_group):
        if self.cac_attack:
            cac_pattern = [
                pygame.image.load("img/game/player/frame_1.png").convert_alpha(),
                pygame.image.load("img/game/player/frame_2.png").convert_alpha(),
                pygame.image.load("img/game/player/frame_3.png").convert_alpha(),
                pygame.image.load("img/game/player/frame_4.png").convert_alpha(),
                pygame.image.load("img/game/player/frame_5.png").convert_alpha(),
                pygame.image.load("img/game/player/frame_6.png").convert_alpha(),
                pygame.image.load("img/game/player/frame_7.png").convert_alpha()
            ]
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_interval:
                if self.frame_index < len(cac_pattern)-1:
                    self.frame_index +=1
                self.last_frame_time = current_time

            spawn_pos = None
            offset = 80  
            angle_rad = math.radians(self.angle)  
            dir_vector = pygame.Vector2(math.cos(angle_rad), math.sin(angle_rad))
            spawn_pos = pygame.Vector2(self.x, self.y) + dir_vector * offset
            
            rotated_image = pygame.transform.rotate(cac_pattern[self.frame_index], -self.adjusted_angle)
            rect = rotated_image.get_rect(center=spawn_pos)

            self.screen.blit(rotated_image, rect)  

            if self.frame_index >= len(cac_pattern)-1:
                self.cac_touched = []
                self.frame_index = 0
                self.cac_attack = 0

            attack_sprite = pygame.sprite.Sprite()
            attack_sprite.rect = rect
            attack_sprite.image = pygame.Surface(rect.size, pygame.SRCALPHA)  # image obligatoire pour les collisions

            touched_enemies = pygame.sprite.spritecollide(attack_sprite, combined_group, dokill=False)
            
            if self.frame_index == 1:
                for i in touched_enemies:
                    if i not in self.cac_touched:
                        i.life -= 1
                        self.cac_touched.append(i)

                
                



    def Attack(self,cible):
        if self.alive:
            cible.life -= self.attack

    def draw(self):
        self.screen.blit(self.image,self.rect)
        pygame.draw.rect(self.screen,"red",self.hitbox,width=1)

    