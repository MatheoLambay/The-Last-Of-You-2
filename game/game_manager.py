import pygame
from game.player import Player
from game.map import Map

class gameManager(Map):
    def __init__(self,screen):
        self.screen = screen
        self.background = pygame.image.load("img\game\map5.png").convert_alpha()
        self.player = Player(screen,"img\game\easter_egg.png",1920/2,1080/2,3,1)
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
        

    def open(self, screen):
        screen.fill((255,255,255))
        self.screen.blit(self.background,(0,0))

    def close(self):
        pass

    def update(self, event, manager):
        self.screen.fill((255,255,255))
        
        mouse_pos = pygame.mouse.get_pos()
        self.player.point_at(mouse_pos)

        map_position = self.player.move(pygame.key.get_pressed(),self.border)
        if map_position != None:
            self.background = self.map.switch_map(map_position)
            self.screen.blit(self.background,(0,0))

        self.border = self.map.map_border()


        self.screen.blit(self.background,(0,0))

        self.player.draw()