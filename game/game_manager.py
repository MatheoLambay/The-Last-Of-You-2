import pygame
import random
from game.player import Player
from game.map import Map
from game.zombie import Zombie
from game.bullet import Bullet
from game.hud import Hud
from game.items import *


class gameManager(Map):
   
    def __init__(self,screen):
        self.screen = screen
        self.background = pygame.image.load("img\game\map5.png").convert_alpha()

        self.player = Player(screen,"img\game\easter_egg.png",1920/2,1080/2,3,1)

        self.player_bar = Hud(screen,self.player.x,self.player.y,100,10,self.player.life,self.player.weapon_bullet)

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
        self.items = []

        self.last_bullet_time = 0
        self.bullet_interval = 100 

        self.last_zombie_time = 0
        self.zombie_interval = 1000

        self.last_damage_time = 0
        self.damage_interval = 3000
        
    
       
        
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
                self.bullet.append(Bullet(self.screen,"img\game\ibullet.png", self.player.x, self.player.y, mouse_pos,0.8))
                self.player.weapon_bullet -= 1
                self.player_bar.ammo = self.player.weapon_bullet
                self.last_bullet_time = current_time    
        elif self.player.weapon_bullet == 0:
            print("no bullet") 


        """spawn zombie"""
        if current_time - self.last_zombie_time >= self.zombie_interval:
            if(random.randint(0,1)):
                if(random.randint(0,1)):
                    spawn_position_x = random.randint(0,1920)
                    spawn_position_y = 0
                else:
                    spawn_position_x = random.randint(0,1920)
                    spawn_position_y = 1080
            else:
                if(random.randint(0,1)):
                    spawn_position_x = 0
                    spawn_position_y = random.randint(0,1080)
                else:
                    spawn_position_x = 1920
                    spawn_position_y = random.randint(0,1080)

            self.zombies.append(Zombie(self.screen,"img\game\zombie\greendead_haut.png",spawn_position_x,spawn_position_y,3,1))
            self.last_zombie_time = current_time
            

        map_position = self.player.move(pygame.key.get_pressed(),self.border)
        self.player_bar.move(self.player.rect.bottomleft[0],self.player.rect.bottomleft[1])

        if map_position != None:
            self.background = self.map.switch_map(map_position)
            self.screen.blit(self.background,(0,0))
            for z in self.zombies:  
                if map_position == "u":
                    z.y += 1080
                elif map_position == "d":
                    z.y -= 1080
                elif map_position == "l":
                    z.x += 1920
                elif map_position == "r":
                    z.x -= 1920
        

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
                        self.player.Attack(z)
                        
                        if z.life < 1:
                            drop = random.randint(1,10)
                            if drop <= 3:
                                self.items.append(dropBullet(self.screen,"img\game\iammo.webp",z.x,z.y,self.map.case_x,self.map.case_y,10,0.1))
                            self.zombies.pop(self.zombies.index(z))

                        self.bullet.pop(self.bullet.index(b))
                        break
                                
        for i in self.items:
            if i.map_x == self.map.case_x and i.map_y == self.map.case_y:
                i.draw()
            if(i.rect.colliderect(self.player.rect)):
                self.items.pop(self.items.index(i))
                i.give_to(self.player)
                self.player_bar.ammo = self.player.weapon_bullet
            

        for z in self.zombies:
            if z.life > 0:
                z.point_at((self.player.x,self.player.y))
                z.move_to(self.player.x,self.player.y)
                if  0 <= z.x <= 1920 and 0 <= z.y <= 1080:
                    z.draw()
            if(self.player.x-10 <= z.x <= self.player.x+10 and self.player.y-10 <= z.y <= self.player.y+10)   : 
                current_time = pygame.time.get_ticks()
                if current_time - self.last_damage_time >= self.damage_interval:
                    z.Attack(self.player)
                    self.player_bar.hp = self.player.life
                    self.last_damage_time = current_time
                    if self.player.life < 1:
                        self.player.alive = 0 

        
    
        
        self.player_bar.draw()
        self.player.draw()
       