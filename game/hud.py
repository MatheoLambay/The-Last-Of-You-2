import pygame

class Hud:
    def __init__(self,screen,x,y,w,h,max_hp,ammo,max_ammo,gold):
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

    def move(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        ratio = self.hp / self.max_hp

        ammo_font = pygame.font.Font('freesansbold.ttf', 16)
        text = "%i/%i"%(self.ammo,self.max_ammo)
        ammo_text = ammo_font.render(text,True,(0,0,0))
        textRect = ammo_text.get_rect()
        textRect.topleft = (self.x,self.y)
        
        life = pygame.draw.rect(self.screen,"red",(textRect.bottomleft[0],textRect.bottomleft[1],self.w,self.h))
        pygame.draw.rect(self.screen,"green",(textRect.bottomleft[0],textRect.bottomleft[1],self.w*ratio,self.h))

        gold = pygame.font.Font('freesansbold.ttf', 16)
        gold_text = gold.render(str(self.gold),True,(255,215,0))
        goldRect = gold_text.get_rect()
        goldRect.topright = (life.bottomright[0],life.bottomright[1])

        self.screen.blit(ammo_text, textRect)
        self.screen.blit(gold_text, goldRect)



