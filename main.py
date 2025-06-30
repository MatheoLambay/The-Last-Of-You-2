import pygame
from menu_manager import menuManager
from menu.presentation_menu import presentationMenu

pygame.init()
pygame.font.init()
menu_manager = menuManager()
menu_manager.push_menu(presentationMenu(menu_manager.screen))

run = True
while run:
	key = None
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.KEYDOWN:
			key = event.key
		

	current_menu = menu_manager.get_current_menu()
	if current_menu:
		current_menu.update(key,menu_manager)

	pygame.display.update()

pygame.quit()