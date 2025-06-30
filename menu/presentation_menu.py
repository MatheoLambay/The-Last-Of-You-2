import pygame


class presentationMenu:
    def __init__(self,screen):
        self.screen = screen
        self.title_img = pygame.image.load("img\main_menu\menutitle.png").convert_alpha()
        self.part2_img = pygame.image.load("img\main_menu\part2.png").convert_alpha()
        self.background_img = pygame.image.load("img\main_menu\presentation.png").convert_alpha()

        self.titlerect = self.title_img.get_rect(center = (1920//2,1080/10))
        self.part2_rect= self.part2_img.get_rect(topleft=self.titlerect.bottomleft)

        data_font = pygame.font.Font('The Last Of Us Rough.ttf', 80)
        self.data_text = data_font.render("Press any key",True,(255,255,255))
        

        self.text_surface = pygame.Surface(self.data_text.get_size(), pygame.SRCALPHA)
        self.text_surface.blit(self.data_text, (0, 0))
        self.text_surface_rect = self.text_surface.get_rect(midbottom=(1920//2,1000))

        self.text_alpha = 255
        self.text_apparition = 0
        
        
    def fade(self,screen,SCREENWIDTH, SCREENHEIGHT): 
        fade = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        fade.fill((0,0,0))
        opacity = 0
        for r in range(0, 100):
            opacity += 1
            fade.set_alpha(opacity)
            screen.blit(fade, (0,0))
            pygame.display.update() 
        for r in range(0, 100):
            opacity -= 1
            fade.set_alpha(opacity)
            screen.blit(fade, (0,0))
            pygame.display.update()
            

    def open(self,screen):
        screen.fill((255,255,255))
        
    def text_animation(self):
        
        fade_speed = 0.5  # change alpha by 5 per frame
        min_alpha = 0  # minimum alpha for visibility

        if self.text_apparition == 0:
            self.text_alpha -= fade_speed
            if self.text_alpha <= min_alpha:
                self.text_alpha = min_alpha
                self.text_apparition = 1
        else:
            self.text_alpha += fade_speed
            if self.text_alpha >= 255:
                self.text_alpha = 255
                self.text_apparition = 0

        # Clear the surface before blitting new text
        self.text_surface.fill((0, 0, 0, 0))
        self.data_text.set_alpha(self.text_alpha)
        self.text_surface.blit(self.data_text, (0, 0))
        self.screen.blit(self.text_surface, self.text_surface_rect)
          

    def close(self):
        pass

    def update(self, key, manager):
        backgroungrect = self.background_img.get_rect()
        backgroungrect.topleft = (0,0)
        self.screen.blit(self.background_img, backgroungrect)

        
        self.screen.blit(self.title_img, self.titlerect)
        self.screen.blit(self.part2_img, self.part2_rect)
        self.text_animation()

        if key is not None:
            # Smooth zoom effect on background for 2 seconds
            duration = 500  # milliseconds
            start_time = pygame.time.get_ticks()
            initial_scale = 1.0
            final_scale = 2  # Zoom to 120%
            clock = pygame.time.Clock()
            running = True
            while running:
                now = pygame.time.get_ticks()
                elapsed = now - start_time
                if elapsed >= duration:
                    scale = final_scale
                    running = False
                else:
                    t = elapsed / duration
                    scale = initial_scale + (final_scale - initial_scale) * t

                bg_width = int(self.background_img.get_width() * scale)
                bg_height = int(self.background_img.get_height() * scale)
                bg_zoom = pygame.transform.smoothscale(self.background_img, (bg_width, bg_height))
                rect = bg_zoom.get_rect(center=(1920 // 2, 1080 // 2))
                self.screen.fill((0, 0, 0))
                self.screen.blit(bg_zoom, rect)
                pygame.display.update()
                clock.tick(60)

            self.fade(self.screen,1920,1080)
            from menu.main_menu import mainMenu
            manager.push_menu(mainMenu(self.screen))
        