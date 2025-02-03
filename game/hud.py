import pygame

class Hud:
    def __init__(self,screen,x,y,w,h,max_hp,ammo,max_ammo,xp,max_xp,gold):
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

    def move(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        

        ammo_font = pygame.font.Font('freesansbold.ttf', 16)
        text = "%i/%i"%(self.ammo,self.max_ammo)
        ammo_text = ammo_font.render(text,True,(0,0,0))
        textRect = ammo_text.get_rect()
        textRect.topleft = (self.x,self.y)

        ratio = self.hp / self.max_hp
        life = pygame.draw.rect(self.screen,"red",(textRect.bottomleft[0],textRect.bottomleft[1],self.w,self.h))
        pygame.draw.rect(self.screen,"green",(textRect.bottomleft[0],textRect.bottomleft[1],self.w*ratio,self.h))

        ratio = self.xp / self.max_xp

        level = pygame.draw.rect(self.screen,"black",(life.bottomleft[0],life.bottomleft[1],self.w,self.h))
        pygame.draw.rect(self.screen,"yellow",(life.bottomleft[0],life.bottomleft[1],self.w*ratio,self.h))


        gold = pygame.font.Font('freesansbold.ttf', 16)
        gold_text = gold.render(str(self.gold),True,(255,215,0))
        goldRect = gold_text.get_rect()
        goldRect.topright = (level.bottomright[0],level.bottomright[1])

        self.screen.blit(ammo_text, textRect)
        self.screen.blit(gold_text, goldRect)



