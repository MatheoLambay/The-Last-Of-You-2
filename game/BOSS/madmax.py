import pygame
import math
class madmax:
    def __init__(self,screen,zombies):
        self.screen = screen
        self.zombies = zombies

        self.max_life = 100
        self.life = self.max_life


        self.attack = 2
        self.velocity = 0.5
        self.angle = 0
        self.last_angle = None
        self.x = 1920//2
        self.y = 1080//2 

        self.last_poison_time = 0
        self.poison_interval = 1000

        wall1 = pygame.Rect(100,100,1920-200,10)
        wall2 = pygame.Rect(1920-100,100,10,1080-200)
        wall3 = pygame.Rect(100,100,10,1080-200)
        wall4 = pygame.Rect(100,1080-100,1920-190,10)
        self.walls = (wall1,wall2,wall3,wall4)

        self.original_image = pygame.image.load("img/game/boss/madmax.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(1920//2, 1080//2))

        self.poisons = []
        # self.poison_image = pygame.image.load("img/game/boss/poison.png").convert_alpha()
        # self.poison_image_rect = self.poison_image.get_rect(center=(self.x,self.y))

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

    def apparition(self):
        for z in self.zombies:
            z.life = 0
        for w in self.walls:
            pygame.draw.rect(self.screen,"grey",w)

    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        name_text = font.render("MADMAX",True,(0,0,0))
        textRect = name_text.get_rect()
        textRect.topleft = (100,1080-80)

        ratio = self.life / self.max_life
        pygame.draw.rect(self.screen,"red",(textRect.bottomleft[0],textRect.bottomleft[1],(1920-200)*ratio,30))
        self.screen.blit(name_text, textRect)

        for p,x,y in self.poisons:
            rect = p.get_rect(center=(x,y))
            self.screen.blit(p,rect)

        self.screen.blit(self.image, self.rect)
        
    def poison_attack(self):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_poison_time >= self.poison_interval:
            self.poisons.append((pygame.image.load("img/game/boss/poison.png").convert_alpha(),self.x,self.y))
        
            self.last_poison_time = current_time