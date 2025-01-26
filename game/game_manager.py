import pygame
from game.player import Player
from game.map import Map
from game.zombie import Zombie
from game.bullet import Bullet

class gameManager(Map):
   
    def __init__(self,screen):
        self.screen = screen
        self.background = pygame.image.load("img\game\map5.png").convert_alpha()

        self.player = Player(screen,"img\game\easter_egg.png",1920/2,1080/2,3,1)
        #self.zombie = Zombie(screen,"img\game\zombie\greendead_haut.png",100,100,3,1)
        # self.bullet = Bullet(self.screen,"img\game\imgbullet.png",self.player.x,self.player.y,(100,100))

        self.map1 = pygame.image.load("img\game\map1.png").convert_alpha()
        self.map2 = pygame.image.load("img\game\map2.png").convert_alpha()
        self.map3 = pygame.image.load("img\game\map3.png").convert_alpha()
        self.map4 = pygame.image.load("img\game\map4.png").convert_alpha()
        self.map5 = pygame.image.load("img\game\map5.png").convert_alpha()
        self.map6 = pygame.image.load("img\game\map6.png").convert_alpha()
        self.map7 = pygame.image.load("img\game\map7.png").convert_alpha()
        self.map8 = pygame.image.load("img\game\map8.png").convert_alpha()
        self.map9 = pygame.image.load("img\game\map9.png").convert_alpha()

        self.map = Map(screen,(((self.map1),(self.map2),(self.map3)),((self.map4),(self.map5),(self.map6)),((self.map7),(self.map8),(self.map9))))
        self.border = self.map.map_border()

        self.bullet = []
        self.zombies = []

        self.last_bullet_time = 0
        self.bullet_interval = 100 

        self.last_zombie_time = 0
        self.zombie_interval = 1000
        
       
        
    def open(self, screen):
        screen.fill((255,255,255))
        self.screen.blit(self.background,(0,0))
        
        
    def close(self):
        self.bullet = []

    def update(self, event, manager):
        

        self.screen.fill((255,255,255))
        
    
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
       
        self.player.point_at(mouse_pos)
        

        current_time = pygame.time.get_ticks()
        if mouse_click[0] and self.player.weapon_bullet > 0: 
            if current_time - self.last_bullet_time >= self.bullet_interval:
                self.bullet.append(Bullet(self.screen,"img\game\imgbullet.png", self.player.x, self.player.y, mouse_pos))
                self.player.weapon_bullet -= 1
                self.last_bullet_time = current_time    
        elif self.player.weapon_bullet == 0:
            pass  

        if current_time - self.last_zombie_time >= self.zombie_interval:
            self.zombies.append(Zombie(self.screen,"img\game\zombie\greendead_haut.png",100,100,3,1))
            self.last_zombie_time = current_time

        map_position = self.player.move(pygame.key.get_pressed(),self.border)
        if map_position != None:
            self.background = self.map.switch_map(map_position)
            self.screen.blit(self.background,(0,0))
            if map_position == "u":
                for z in self.zombies:
                    z.y += 1080
        """iciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"""
        

        self.border = self.map.map_border()


        self.screen.blit(self.background,(0,0))

        for b in self.bullet:
            b.fire()
            if b.x > 1920 or b.x < 0 or b.y > 1080 or b.y < 0:
                self.bullet.pop(self.bullet.index(b))
            else:
                b.draw()
                for z in self.zombies:
                    if(b.rect.colliderect(z.rect)):
                        self.bullet.pop(self.bullet.index(b))
                        self.player.Attack(z)
                        if z.life < 1:
                            self.zombies.pop(self.zombies.index(z))

        for z in self.zombies:
            if z.life > 0:
                z.point_at((self.player.x,self.player.y))
                z.move_to(self.player.x,self.player.y)
                z.draw()

        
        self.player.draw()
       
        