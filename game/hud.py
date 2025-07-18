import pygame

class Hud:
    def __init__(self,screen,x,y,w,h,max_hp,ammo,max_ammo,xp,max_xp,gold,level):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.ammo = ammo 
        self.max_ammo = max_ammo
        self.gold = gold
        self.xp = xp
        self.max_xp = max_xp
        self.level = level
        self.items = [0,0,0]

    def move(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = "%i/%i"%(self.ammo,self.max_ammo)
        ammo_text = font.render(text,True,(0,0,0))
        textRect = ammo_text.get_rect()
        textRect.topleft = (self.x,self.y)

        ratio = self.hp / self.max_hp
        life = pygame.draw.rect(self.screen,"red",(textRect.bottomleft[0],textRect.bottomleft[1],self.w,self.h))
        pygame.draw.rect(self.screen,"green",(textRect.bottomleft[0],textRect.bottomleft[1],self.w*ratio,self.h))

        ratio = self.xp / self.max_xp

        level = pygame.draw.rect(self.screen,"black",(life.bottomleft[0],life.bottomleft[1],self.w,self.h))
        pygame.draw.rect(self.screen,"yellow",(life.bottomleft[0],life.bottomleft[1],self.w*ratio,self.h))

        lvl_text = font.render(str(self.level),True,(0,0,0))
        lvlRect = lvl_text.get_rect()
        lvlRect.topleft = (level.topleft[0],level.topleft[1])


        gold_text = font.render(str(self.gold),True,(255,215,0))
        goldRect = gold_text.get_rect()
        goldRect.topright = (level.bottomright[0],level.bottomright[1])

        last_rect =  [life.topright[0],textRect.bottomright[1]]

        for i in self.items:
    
            slot = pygame.draw.rect(self.screen,"grey", (last_rect[0],last_rect[1], 30,30))
            if i != 0:
                item_frame = pygame.draw.rect(self.screen,"green", (last_rect[0]+4,last_rect[1]+4, 21,21))

                self.original_image = pygame.image.load(i["link"]).convert_alpha()
                width = self.original_image.get_width()
                height = self.original_image.get_height()
                self.original_image = pygame.transform.scale(self.original_image, (int(width * 0.5), int(height * 0.5)))
                self.original_image_rect = self.original_image.get_rect()
                self.original_image_rect.center = (item_frame.centerx, item_frame.centery)
                self.screen.blit(self.original_image, self.original_image_rect)


            else:
                pygame.draw.rect(self.screen,"red", (last_rect[0]+4,last_rect[1]+4, 21,21))
            last_rect = slot.topright
        
        
            
        
        self.screen.blit(lvl_text, lvlRect)
        self.screen.blit(ammo_text, textRect)
        self.screen.blit(gold_text, goldRect)



