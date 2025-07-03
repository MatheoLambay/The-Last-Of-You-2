import pygame
import math
import random

class madmax(pygame.sprite.Sprite):
    def __init__(self,screen,zombies):
        super().__init__()
        self.screen = screen
        self.zombies = zombies

        self.max_life = 100
        self.life = self.max_life

        self.attack = 2
        self.velocity = 0.5
        self.angle = 0
        self.gold = 400

        self.last_angle = None
        self.x = 1920//2
        self.y = 1080//2

        self.items_life = 10

        self.last_poison_time = 0
        self.poison_interval = 1000
        self.last_attack_time = 0
        self.attack_interval = 1000

        wall1 = pygame.Rect(100,100,1920-200,10)
        wall2 = pygame.Rect(1920-100,100,10,1080-200)
        wall3 = pygame.Rect(100,100,10,1080-200)
        wall4 = pygame.Rect(100,1080-100,1920-190,10)
        self.walls = (wall1,wall2,wall3,wall4)

        self.original_image = pygame.image.load("img/game/boss/madmax.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(1920//2, 1080//2))
        self.hitbox = pygame.Rect(self.x-self.original_image.get_height()//2,self.y-self.original_image.get_width()//2,self.original_image.get_height(),self.original_image.get_width())

        self.poisons = []
        self.item_dropped = 0
    

    def point_at(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        
        if self.last_angle is None or abs(angle - self.last_angle) > 2:
            self.last_angle = angle
            adjusted_angle = angle - 90
            self.image = pygame.transform.rotate(self.original_image, -adjusted_angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def move_to(self, targetx, targety):
        direction = pygame.math.Vector2(targetx - self.x, targety - self.y)
        if direction.length_squared() != 0:
            direction = direction.normalize() * self.velocity
            self.x += direction.x
            self.y += direction.y
            self.rect.center = (self.x, self.y)
        self.hitbox = pygame.Rect(self.x-self.original_image.get_height()//2,self.y-self.original_image.get_width()//2,self.original_image.get_height(),self.original_image.get_width())

    def spawn(self):
        for z in self.zombies:
            z.kill()
        for w in self.walls:
            pygame.draw.rect(self.screen,"grey",w)

    def boss_management(self,player):
        font = pygame.font.Font('freesansbold.ttf', 30)
        name_text = font.render("MADMAX",True,(0,0,0))
        textRect = name_text.get_rect()
        textRect.topleft = (100,1080-80)
        ratio = self.life / self.max_life
        pygame.draw.rect(self.screen,"red",(textRect.bottomleft[0],textRect.bottomleft[1],(1920-200)*ratio,30))
        self.screen.blit(name_text, textRect)

        self.poison_spawn()
        self.poison_management(player)
        self.item_drop()


        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen,"blue",self.hitbox,width=1)
        
    def poison_spawn(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_poison_time >= self.poison_interval:
            if len(self.poisons) > 10:
                self.poisons.pop(0)

            self.poisons.append((pygame.image.load("img/game/boss/poison.png").convert_alpha(),self.x,self.y)) 
            self.last_poison_time = current_time
            

    def poison_management(self,cible):
        for p,x,y in self.poisons:
            rect = p.get_rect(center=(x,y))
            self.screen.blit(p,rect)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time >= self.attack_interval:
                if cible.hitbox.colliderect(rect):
                    cible.life -= self.attack
                self.last_attack_time = current_time

    def item_drop(self):
        if self.life < 50:
            if not self.item_dropped:
                self.item_dropped = 1
            else:
                img = pygame.image.load("img/game/boss/egg.png").convert_alpha()
                self.screen.blit(img, (500,500))
            
    def update(self,player):
        

        if self.life > 0:
            self.spawn()
            for w in self.walls:
                player.collision(w)

            if player.hitbox.colliderect(self.hitbox):
                print("detect")
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_interval:
                    player.life -= self.attack
                    self.last_attack_time = current_time
                
            self.point_at((player.x,player.y))
            self.move_to(player.x,player.y)
            # self.mad_max.poison_spawn(
            self.boss_management(player)
        elif self.life < 1:
            player.gold += self.gold
            self.kill()

        

  