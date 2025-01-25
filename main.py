import pygame
from menu_manager import menuManager
from menu.main_menu import mainMenu


pygame.init()

menu_manager = menuManager()
menu_manager.push_menu(mainMenu(menu_manager.screen))


run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	current_menu = menu_manager.get_current_menu()
	if current_menu:
		current_menu.update(event,menu_manager)
		
	
	pygame.display.update()

pygame.quit()