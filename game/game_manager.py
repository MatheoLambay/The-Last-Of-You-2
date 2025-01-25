import pygame
from game.player import Player

class gameManager:
    def __init__(self,screen):
        self.screen = screen
        self.player = Player(screen,"img\game\easter_egg.png",1920/2,1080/2,3,1)

    def open(self, screen):
        screen.fill((255,255,255))
        # self.player.place()

    def close(self):
        pass

    def update(self, event, manager):

        self.player.draw()

        if event.type == pygame.MOUSEMOTION:
            self.player.point_at(event.pos)
            
        
        