import pygame
import random
import json

from game.player import Player
from game.map import Map
from game.zombie import Zombie
from game.bullet import Bullet
from game.hud import Hud
from game.pnj import SellerPnj
from game.items import *



class gameManager(Map):
   
    def __init__(self,screen):
        self.screen = screen

        with open("game/zombie.json", 'r') as f:
            self.zombies_pattern = json.load(f)

        with open('menu/stat.json', 'r') as s:
            self.stat_player = json.load(s)
        

        self.background = pygame.image.load("img\game\map5.png").convert_alpha()

        self.death_img = pygame.image.load("img\game\gameover.png").convert_alpha()
        self.deat_rect = self.death_img.get_rect().center =(1920/2,1080/2) 

        self.player = Player(screen,"img\game\easter_egg.png",1920/2,1080/2,3,1)

        self.player_bar = Hud(screen,self.player.x,self.player.y,100,10,self.player.life,self.player.weapon_bullet,self.player.weapon_bullet_max,self.player.gold)

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
        self.pnjs = []

        self.last_bullet_time = 0
        self.bullet_interval = 100 

        self.last_zombie_time = 0
        self.zombie_interval = 1000

        self.last_damage_time = 0
        self.damage_interval = 2000

        self.market_button = 0
        self.player_in_safezone = 0

        self.pnjs.append(SellerPnj(self.screen,"img\game\zonesafe.png",1920/2,1080/2,0,1,"market",999,0))
        self.pnjs.append(SellerPnj(self.screen,"img\game\pnj.png ",1920/2,1080/2,0,1,"vendeur",0,1))
        
    
    def open(self, screen):
        screen.fill((255,255,255))
        self.screen.blit(self.background,(0,0))
        
        
    def close(self):
        pass

    def update(self, event, manager):
        if self.player.alive:

            self.screen.fill((255,255,255))
            self.screen.blit(self.background,(0,0))

            mouse_pos = pygame.mouse.get_pos()
            """orientation joueur"""
            self.player.point_at(mouse_pos)
            
            current_time = pygame.time.get_ticks()
        
            """spawn bullet"""
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] and self.player.weapon_bullet > 0 and self.player.can_attack: 
                if current_time - self.last_bullet_time >= self.bullet_interval and self.player.can_attack:
                    self.new_bullet(mouse_pos)
                    self.last_bullet_time = current_time 

            """spawn zombie"""
            if current_time - self.last_zombie_time >= self.zombie_interval and not(self.player_in_safezone):
                self.zombie_spawn()
                self.last_zombie_time = current_time 
                    
            """player move, hud"""
            map_position = self.player.move(pygame.key.get_pressed(),self.border)
            self.player_bar.move(self.player.rect.bottomleft[0],self.player.rect.bottomleft[1])

            """detect map change"""
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
            
            """check map border"""
            self.border = self.map.map_border()

            """update bullets in list"""
            self.bullets_management()
            """update items in list"""
            self.items_management()

            self.player.can_attack = 1
            self.player_in_safezone = 0
            """update pnj interaction"""
            self.pnjs_management(manager)
            """udpate zombies in list"""
            self.zombies_management()
            
            if not(self.player.player_in_market):  
                self.draw_update_player_hud()
            
        else:
            self.screen.blit(self.death_img,self.deat_rect)
            print('mort')
            with open("menu\stat.json", 'w') as w:
                json.dump(self.stat_player,w)


    def draw_update_player_hud(self):
    
        self.player_bar.gold = self.player.gold
        self.player_bar.ammo = self.player.weapon_bullet
        self.player_bar.max_ammo = self.player.weapon_bullet_max
        self.player_bar.hp = self.player.life
        self.player_bar.max_hp = self.player.life_max
        
        self.player_bar.draw()
        self.player.draw()


    def zombie_spawn(self):
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


        spawn_percent = random.randint(0,100)
        new_zombies_pattern = list(self.zombies_pattern.keys())
    
        zombie_not_selected = 1

        while zombie_not_selected:
            
            random_zombie = random.choice(new_zombies_pattern)

            if self.zombies_pattern[random_zombie]["rate"] >= spawn_percent and self.zombies_pattern[random_zombie]["min_score"] <= self.player.score: 
                link = self.zombies_pattern[random_zombie]["link"]
                life = self.zombies_pattern[random_zombie]["life"]
                attack = self.zombies_pattern[random_zombie]["attack"]
                gold = self.zombies_pattern[random_zombie]["gold"]
                velocity = self.zombies_pattern[random_zombie]["velocity"]
                scale = self.zombies_pattern[random_zombie]["scale"]
                self.zombies.append(Zombie(self.screen,link,spawn_position_x,spawn_position_y,life,attack,gold,velocity,scale))
                zombie_not_selected = 0

            else:
                new_zombies_pattern.pop(new_zombies_pattern.index(random_zombie))


    def new_bullet(self,mouse_pos):
        if self.player.weapon_bullet > 0:
            self.bullet.append(Bullet(self.screen,"img\game\ibullet.png", self.player.x, self.player.y, mouse_pos,0.8))
            self.player.weapon_bullet -= 1 
        else:
            pass


    def bullets_management(self):
        for b in self.bullet:
            b.fire()
            if b.x > 1920 or b.x < 0 or b.y > 1080 or b.y < 0:
                self.bullet.pop(self.bullet.index(b))
            else:
                b.draw()
                for z in self.zombies:
                    if( z.x - 20 <= b.x <= z.x + 20 and z.y - 20 <= b.y <= z.y + 20):
                        
                        self.player.Attack(z)
                        
                        if z.life < 1:
                            """zombie drop"""
                            z.drop_gold(self.player)
                            self.stat_player["dead killed"] += 1
                            self.stat_player["total gold"] += z.gold
                            
                            self.player.score += 1
                            
                            drop = random.randint(1,100)
                            if 1 <= drop <= 30:
                                self.items.append(dropItems(self.screen,"img\game\iammo.webp",z.x,z.y,self.map.case_x,self.map.case_y,40,"ammo",5000,0.1))
                            
                            elif 30 <= drop <= 35:
                                self.items.append(dropItems(self.screen,"img\game\heal.png",z.x,z.y,self.map.case_x,self.map.case_y,1,"heal",8000,0.1))
                        
                        self.bullet.pop(self.bullet.index(b))
                        break


    def items_management(self):
        for i in self.items:
            current_time = pygame.time.get_ticks()
            if i.map_x == self.map.case_x and i.map_y == self.map.case_y:
                i.draw()
            if(self.player.x-20 <= i.x <= self.player.x+20 and self.player.y-20 <= i.y <= self.player.y+20):
                if i.name == "ammo" and self.player.weapon_bullet < self.player.weapon_bullet_max:
                    i.give_ammo_to(self.player)
                elif i.name == "heal" and self.player.life < self. player.life_max:
                    i.give_life_to(self.player)

                self.items.pop(self.items.index(i))
            elif(current_time - i.damage_interval >= i.last_damage_time):
                self.items.pop(self.items.index(i))


    def pnjs_management(self,manager):
        for p in self.pnjs:
            if p.map_x == self.map.case_x and p.map_y == self.map.case_y:
                if self.player.player_in_market == 0:
                    p.draw()

                keyboard = pygame.key.get_pressed()
                if p.rect.colliderect(self.player.rect):
                    self.player_in_safezone = 1
                    self.player.can_attack = 0
                    key = keyboard[pygame.K_e]
                    if key and self.market_button == 0:
                        self.player.player_in_market = 1
                        from game.shop import shopMenu
                        manager.push_menu(shopMenu(self.screen,self.player))
                        
                        print("pnj détecté")
                    self.market_button = key
                    
                """Gestion de collision avec le joueur"""
                if self.player.rect.colliderect(p.rect) and p.hitbox:
                    overlap_x = min(self.player.rect.right - p.rect.left, p.rect.right - self.player.rect.left)
                    overlap_y = min(self.player.rect.bottom - p.rect.top, p.rect.bottom - self.player.rect.top)

                    if overlap_x < overlap_y:  # Collision dominante sur l'axe horizontal
                        if self.player.rect.centerx < p.rect.centerx:
                            self.player.x = p.rect.left - self.player.rect.width / 2
                        else:
                            self.player.x = p.rect.right + self.player.rect.width / 2
                    elif overlap_x > overlap_y:  # Collision dominante sur l'axe vertical
                        if self.player.rect.centery < p.rect.centery:
                            self.player.y = p.rect.top - self.player.rect.height / 2
                        else:
                            self.player.y = p.rect.bottom + self.player.rect.height / 2

                    self.player.rect.center = (self.player.x, self.player.y)
    

    def zombies_management(self):
        for z in self.zombies:
            if z.life > 0:
                if not(self.player_in_safezone):
                    z.point_at((self.player.x,self.player.y))
                    z.move_to(self.player.x,self.player.y)
                if  0 <= z.x <= 1920 and 0 <= z.y <= 1080:
                    z.draw()
            else:
                self.zombies.pop(self.zombies.index(z))

            if(self.player.x-20 <= z.x <= self.player.x+20 and self.player.y-20 <= z.y <= self.player.y+20)   : 
                current_time = pygame.time.get_ticks()
                if current_time - self.last_damage_time >= self.damage_interval:
                    z.Attack(self.player)
                    
                    self.last_damage_time = current_time
                    if self.player.life < 1:
                        """joueur mort"""
                        self.player.alive = 0  