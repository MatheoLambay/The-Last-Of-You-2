import pygame

class Touch:
    def __init__(self,screen, touch, x=0, y=0):
        self.screen = screen
        self.touch = touch
        self.x = x
        self.y = y
        self.frame_size = 50
        self.frame_rect = (self.x+(self.frame_size/2), self.y+(self.frame_size/2))
       
    def draw(self):
        
        pygame.draw.rect(self.screen,"white", (self.x,self.y, self.frame_size,self.frame_size))
        pygame.draw.rect(self.screen,"green", (self.x+2,self.y+2, self.frame_size-4,self.frame_size-4))
        
        font = pygame.font.Font("The Last Of Us Rough.ttf", 40)

        self.touch_name = font.render(self.touch[0], True, (255,255,255))
        self.touch_name_rect = self.touch_name.get_rect(topright=(self.x-20,self.y))

        self.touch_text = font.render(self.touch[1], True, (0,0,0))
        self.touch_text_rect = self.touch_text.get_rect(center=(self.frame_rect[0], self.frame_rect[1]))
        
        self.screen.blit(self.touch_name, self.touch_name_rect)
        self.screen.blit(self.touch_text, self.touch_text_rect)

    def detect(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x <= mouse_x <= self.x + self.frame_size and self.y <= mouse_y <= self.y + self.frame_size:
            if pygame.mouse.get_pressed()[0]:
                return True
        return False
    

    