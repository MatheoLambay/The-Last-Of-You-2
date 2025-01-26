import pygame

class Hud:
    def __init__(self,screen,x,y,w,h,max_hp,ammo):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.ammo = ammo 

    def move(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        ratio = self.hp / self.max_hp

        pygame.font.init()
        title = pygame.font.Font('freesansbold.ttf', 32)
        title_text = title.render(str(self.ammo),True,(0,0,0))
        textRect = title_text.get_rect()
        textRect.topleft = (self.x,self.y)
        
        pygame.draw.rect(self.screen,"red",(textRect.bottomleft[0],textRect.bottomleft[1],self.w,self.h))
        pygame.draw.rect(self.screen,"green",(textRect.bottomleft[0],textRect.bottomleft[1],self.w*ratio,self.h))
        self.screen.blit(title_text, textRect)

