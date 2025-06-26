from button import Button
import pygame

class selectPlayer(Button):
    def __init__(self,screen , player,x, y):
        background_img = pygame.image.load("img\select_mode_menu\wanted1.png").convert_alpha()
        super().__init__(screen, x, y, background_img)
        self.player = player
        self.screen = screen
        

    """Dessine le bouton et affiche les informations du joueur."""
    def draw_affich(self):
        
        self.draw()
        player_img = pygame.image.load(self.player["link"]).convert_alpha()
        player_img_rect = player_img.get_rect(center=(self.rect.centerx, self.rect.centery))


        font = pygame.font.Font("The Last Of Us Rough.ttf", 40)
        name_text = font.render(self.player["name"], True, (0,0,0))
        name_text_rect = name_text.get_rect(center=(player_img_rect.centerx, player_img_rect.bottom + 20))


        self.screen.blit(player_img, player_img_rect)
        self.screen.blit(name_text, name_text_rect)
      
   
       
            
    def get_top_right(self):
        """Retourne la position en haut à gauche de l'image de fond."""
        return self.rect.topright

    