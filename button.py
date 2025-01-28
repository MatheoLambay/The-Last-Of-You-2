import pygame

#button class
class Button():
	def __init__(self,screen, x, y, image, scale=1, center_pos = "topleft"):
		width = image.get_width()
		height = image.get_height()

		self.screen = screen
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		if center_pos == "topleft":
			self.rect.topleft = (x,y)
		elif center_pos == "bottomright":
			self.rect.bottomright = (x,y)
		self.clicked = False
		

	def draw(self):
		self.screen.blit(self.image, (self.rect.x, self.rect.y))


	def detect(self):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
				
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action