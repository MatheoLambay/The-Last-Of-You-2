import pygame

class Player:
    def __init__(self,screen,link,x,y,life,attack,score=0):
        self.screen = screen

        self.image = pygame.image.load(link)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y     
        self.life = life
        self.attack = attack
        self.score = score
        self.velocity = 5  

    def Attack(self,cible):
        cible.life -= self.attack  
        
    def point_at(self, m_pos):
        pass
  
    def draw(self):
        self.screen.blit(self.image,self.rect)

   