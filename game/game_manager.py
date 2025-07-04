import pygame
import random
import json
from game.player import Player
from game.map import Map
from game.zombie import Zombie
from game.bullet import Bullet
from game.hud import Hud
from game.turret import Turret
from game.items import dropItems
from game.ShopPnj import ShopPnj
from game.lvlup import LvLup
from game.BOSS.madmax import madmax
from button import Button



class gameManager(Map):
    
    def __init__(self,screen,player,texture_map):
        self.screen = screen

        with open("data\zombie.json", 'r') as f:
            self.zombies_pattern = json.load(f)

        with open('data\stat.json', 'r') as s:
            self.stat_player = json.load(s)
        
        with open('data\controls.json', 'r') as c:
            self.controls = json.load(c)

        self.interact = self.controls["interact"]
        self.items_1 = self.controls["item 1"]
        self.items_2 = self.controls["item 2"] 
        self.items_3 = self.controls["item 3"]
     
        
        #création du joueur et du hud
        self.player = Player(screen,player["link"],1920/2,1080/2,player["life"],player["attack"],player["velocity"],player["weapon_bullet_max"],player["attack_cooldown"],player["range_item"])
        self.player_bar = Hud(screen,self.player.x,self.player.y,100,10,self.player.life,self.player.weapon_bullet,self.player.weapon_bullet_max,self.player.xp,self.player.max_xp,self.player.gold,self.player.lvl)
        
        #création de la map
        self.map = Map(screen,texture_map)
        self.map.get_random_case()
        self.border = self.map.map_border()
        self.background = self.map.get_spawn_map()

        self.bullet = []
        self.zombies = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.items = []
        self.pnjs = []
        self.turrets = pygame.sprite.Group()

        self.combined_group = pygame.sprite.Group()
        self.combined_group.add(self.zombies)
        self.combined_group.add(self.boss)


        self.last_bullet_time = 0
        self.bullet_interval = self.player.attack_cooldown

        # intervalles pour le spawn de zombies
        self.last_zombie_time = 0
        self.zombie_interval = 1000

        # intervalles pour les dégâts du joueur
        # self.last_damage_time = 0
        # self.damage_interval = 1000

        # statistiques du joueur (temps)
        self.last_play_time = 0
        self.play_interval = 1000

        self.time_played = 0
        self.zombie_killed = {"greendead":0,"bluedead":0,"reddead":0,"yellowdead":0}
        
        self.market_button = 0
        self.player_in_safezone = 0
        self.death_animation_flag = 1

        pnj_spawn = self.map.get_random_case()
        self.pnjs.append(ShopPnj(self.screen,"img\game\Seller.png",random.randint(100,1820),random.randint(100,980),pnj_spawn[0],pnj_spawn[1],"seller"))

        self.mad_max = madmax(self.screen,self.zombies)
       

    def open(self, screen):
        screen.fill((255,255,255))
        self.screen.blit(self.background,(0,0))
        
        
    def close(self):
        pass

    def update(self, key, manager):

        if self.player.is_alive:
            
            self.screen.fill((255,255,255))
            self.screen.blit(self.background,(0,0))

            font = pygame.font.Font('freesansbold.ttf', 16)
            gold_text = font.render(str(len(self.zombies)),True,(255,215,0))
            goldRect = gold_text.get_rect()
            goldRect.topleft = (100,100)
            self.screen.blit(gold_text, goldRect)

            mouse_pos = pygame.mouse.get_pos()
            """orientation joueur"""
            self.player.point_at(mouse_pos)
            
            current_time = pygame.time.get_ticks()

            """time played"""
            if current_time - self.last_play_time >= self.play_interval:
                self.time_played +=1
                self.last_play_time = current_time
        
            """spawn bullet"""
            mouse_click = pygame.mouse.get_pressed()
            
            if mouse_click[0] and self.player.weapon_bullet > 0 and self.player.can_attack: 
                if current_time - self.last_bullet_time >= self.bullet_interval and self.player.can_attack:
                    self.new_bullet(mouse_pos,self.player)
                    self.last_bullet_time = current_time 
            elif mouse_click[2]:
                self.player.cac_attack = 1
         

            """spawn zombie"""
            if current_time - self.last_zombie_time >= self.zombie_interval and not(self.player_in_safezone):
                self.new_zombie()
                self.last_zombie_time = current_time 
                    
            """player move, hud"""
            map_position = self.player.move(self.border)
            self.player_bar.move(self.player.hitbox.bottomleft[0],self.player.hitbox.bottomleft[1])

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
                for b in self.boss:
                    if map_position == "u":
                        b.y += 1080
                    elif map_position == "d":
                        b.y -= 1080
                    elif map_position == "l":
                        b.x += 1920
                    elif map_position == "r":
                        b.x -= 1920

            
            """check map border"""
            self.border = self.map.map_border()

            """update turrets in list"""
            self.turrets_management()

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

            """player items management"""
            self.player_items_management()


            
            if self.player.score == 100:
                print("ici")
                self.boss.add(self.mad_max)
                self.player.score +=1
            self.boss_management()

            """player life"""
            self.player_management(manager)

            if not(self.player.player_in_market):  
                self.draw_update_player_hud()

        else:
            
            if self.death_animation_flag:
                self.fade_death()
                self.death_animation_flag = 0

    
            if self.end_btn.detect():
                from menu.resume_menu import resumeMenu
                manager.push_menu(resumeMenu(self.screen,self.zombie_killed,self.time_played,self.player.gold,self.player.current_upgrade,self.stat_player["total xp"]))
            

    def fade_death(self):

        self.death_img = pygame.image.load("img\game\gameover.png").convert_alpha()
        self.death_surface = pygame.Surface(self.death_img.get_size(), pygame.SRCALPHA)
        self.death_surface.blit(self.death_img, (0, 0))
        self.death_surface.set_alpha(0)
        self.death_surface_rect = self.death_surface.get_rect(center=(1920 // 2, 1080 // 2))

        for i in range(0, 255, 5):
            self.death_surface.set_alpha(i)
            self.screen.blit(self.death_surface, self.death_surface_rect)
            pygame.display.flip()
            pygame.time.delay(50)

        
        self.end_img = pygame.image.load("img\main_menu\start_btn_upper.png").convert_alpha()
        self.end_img_rect = self.end_img.get_rect()

        self.end_img_rect.centerx = self.death_surface_rect.centerx
        self.end_img_rect.top = self.death_surface_rect.bottom + 20  

        self.end_btn = Button(self.screen, self.end_img_rect.x, self.end_img_rect.y, self.end_img)
        self.end_btn.draw()

    def set_seller_position(self,p):
        pnj_spawn = self.map.get_random_case()
        p.map_x = pnj_spawn[0]
        p.map_y = pnj_spawn[1]
        p.x = random.randint(100,1820)
        p.y = random.randint(100,980)

    

    def draw_update_player_hud(self):
    
        self.player_bar.gold = self.player.gold
        self.player_bar.ammo = self.player.weapon_bullet
        self.player_bar.max_ammo = self.player.weapon_bullet_max
        self.player_bar.xp = self.player.xp
        self.player_bar.max_xp = self.player.max_xp
        self.player_bar.hp = self.player.life
        self.player_bar.max_hp = self.player.life_max
        self.player_bar.level = self.player.lvl
        
        self.player_bar.items = self.player.items
      
        
        self.player_bar.draw()
        self.player.draw()

    def new_zombie(self):
        # Choix de la position de spawn
        if random.randint(0, 1):
            spawn_position_x = random.randint(0, 1920)
            spawn_position_y = 0 if random.randint(0, 1) else 1080
        else:
            spawn_position_x = 0 if random.randint(0, 1) else 1920
            spawn_position_y = random.randint(0, 1080)

        # Construction de la liste des zombies valides
        zombies_pondérés = []
        poids_total = 0

        for key, zombie in self.zombies_pattern.items():
            if self.player.score >= zombie["min_score"]:
                force = zombie["life"]
                base_rate = zombie["rate"]
                # Formule pondérée (ajuste le 0.005 si nécessaire)
                poids = (1 / base_rate) * (1 + self.player.score * 0.005 * force)
                zombies_pondérés.append((key, zombie, poids))
                poids_total += poids

        # Sélection d’un zombie selon la pondération
        r = random.uniform(0, 1)
        cumul = 0
        zombie_choisi = None
        for key, zombie, poids in zombies_pondérés:
            ratio = poids / poids_total
            cumul += ratio
            if r < cumul:
                zombie_choisi = zombie
                break

        # Instanciation du zombie sélectionné
        if zombie_choisi:
            self.zombies.add(
                Zombie(
                    self.screen,
                    zombie_choisi["link"],
                    spawn_position_x,
                    spawn_position_y,
                    zombie_choisi["name"],
                    zombie_choisi["life"],
                    zombie_choisi["attack"],
                    zombie_choisi["gold"],
                    zombie_choisi["xp"],
                    zombie_choisi["velocity"],
                    zombie_choisi["scale"],
                )
            )


    def new_bullet(self,direction,player):
        if player.weapon_bullet > 0:
            self.bullet.append(Bullet(self.screen,"img\game\ibullet.png", player.x, player.y, direction,0.8))
            player.weapon_bullet -= 1 
        else:
            pass


    def bullets_management(self):

        for b in self.bullet:
            b.fire()
            if b.x > 1920 or b.x < 0 or b.y > 1080 or b.y < 0:
                self.bullet.pop(self.bullet.index(b))
            else:
                b.draw()

                for bo in self.boss:
                    if b.rect.colliderect(bo.rect):
                        self.player.Attack(bo)
                        self.bullet.pop(self.bullet.index(b))


                for z in self.zombies:
                    if( z.x - 20 <= b.x <= z.x + 20 and z.y - 20 <= b.y <= z.y + 20):
                        
                        self.player.Attack(z)
                        
                        self.bullet.pop(self.bullet.index(b))
                        break


    def items_management(self):
        for i in self.items:
            current_time = pygame.time.get_ticks()
            if i.map_x == self.map.case_x and i.map_y == self.map.case_y:
                i.draw()
            if(self.player.x-self.player.range_item <= i.x <= self.player.x+self.player.range_item and self.player.y-self.player.range_item <= i.y <= self.player.y+self.player.range_item):
                if i.name == "ammo" and self.player.weapon_bullet < self.player.weapon_bullet_max:
                    i.give_ammo_to(self.player)
                elif i.name == "heal" and self.player.life < self. player.life_max:
                    i.give_life_to(self.player)

                self.items.pop(self.items.index(i))
            elif(current_time - i.damage_interval >= i.last_damage_time):
                self.items.pop(self.items.index(i))


    def pnjs_management(self,manager):
        for p in self.pnjs:
            # Check if the pnj is on the current map
            if p.map_x == self.map.case_x and p.map_y == self.map.case_y:
                if self.player.player_in_market == 0:
                    p.draw()

                if p.name == "seller" or p.name == "safezone":
                    # detecte si le joueur est dans la zone de sécurité
                    if self.player.hitbox.colliderect(p.zone_rect):
                        self.player_in_safezone = 1
                        self.player.can_attack = 0                      
                        if pygame.key.get_pressed()[pygame.key.key_code(self.interact)] and self.market_button == 0:
                            self.player.player_in_market = 1
                            p.openShop(manager,self.player)
                            
                        
                    
                    
                """Gestion de collision avec le joueur"""
                self.player.collision(p)



    def player_items_management(self):
        
        if pygame.key.get_pressed()[pygame.key.key_code(self.items_1)] and self.player.items[0] != 0:
            if self.player.items[0]["name"] == "turret":
                self.place_turret(0)
        if pygame.key.get_pressed()[pygame.key.key_code(self.items_2)] and self.player.items[1] != 0:
            if self.player.items[1]["name"] == "turret":
                self.place_turret(1)
        if pygame.key.get_pressed()[pygame.key.key_code(self.items_3)] and self.player.items[2] != 0:
            if self.player.items[2]["name"] == "turret":
                self.place_turret(2)
            
    def place_turret(self,slot):
        self.turrets.add(Turret(self.screen,self.player.items[slot]["link"],self.player.x,self.player.y,self.map.case_x,self.map.case_y,self.player.items[slot]["damage"],self.player.items[slot]["weapon_bullet"], self.player.items[slot]["range"]))
        self.player.items[slot] = 0
        
    
    def turrets_management(self):
        for t in self.turrets:
            if t.map_x == self.map.case_x and t.map_y == self.map.case_y:
                if self.player.player_in_market == 0:
                    t.draw()
                    t.update(self.zombies, self.new_bullet)


    def zombies_management(self):
        self.zombies.update(self.player, self.player_in_safezone)
        for z in self.zombies:
            if z.life < 1:

                print("dead")
                self.stat_player["dead killed"] += 1
                self.stat_player["total gold"] += z.gold
                self.stat_player["total xp"] += z.xp
                self.stat_player[z.name] += 1
                self.zombie_killed[z.name] +=1
                self.player.get_level(z.xp)

                drop = random.randint(1,150)
                print(drop)
                if 1 <= drop <= 30:
                    self.items.append(dropItems(self.screen,"img\game\iammo.webp",z.x,z.y,self.map.case_x,self.map.case_y,40,"ammo",5000,0.1))
                
                elif 30 <= drop <= 35:
                    self.items.append(dropItems(self.screen,"img\game\heal.png",z.x,z.y,self.map.case_x,self.map.case_y,1,"heal",8000,0.1))
                z.drop_gold(self.player)
                z.kill()
                self.player.score += 10


    def boss_management(self):
        self.boss.update(self.player)

       
    def player_management(self,manager):
        
        if self.player.life < 1:
            with open("data/stat.json", 'w') as w:
                json.dump(self.stat_player, w,indent=4)
            self.player.is_alive = 0
        else:
            self.player.powers.update()
            if self.player.player_level_up:
                self.player_in_safezone = 1
                manager.push_menu(LvLup(self.screen,self.player))

            self.combined_group = pygame.sprite.Group()
            self.combined_group.add(self.zombies)
            self.combined_group.add(self.boss)
            self.player.cac_Attack(self.combined_group)