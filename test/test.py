import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Code de la touche")

font = pygame.font.SysFont(None, 30)

def afficher_texte(texte):
    screen.fill((30, 30, 30))
    rendu = font.render(texte, True, (255, 255, 255))
    screen.blit(rendu, (20, 80))
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            afficher_texte(f"Touche: {event.unicode} | Code: {event.key}")
