import pygame

class Map:
    def __init__(self,screen,map):
        self.screen = screen
        
        self.case_x = 1
        self.case_y = 1
        self.max_case_x = 2
        self.max_case_y = 2
        self.min_case_x = 0
        self.min_case_y = 0
        self.map = map
        self.border = {"up":0,"down":0,"left":0,"right":0}
        
        
    def switch_map(self,direction):
        
        if direction == "u" and self.case_y > self.min_case_y:
            self.case_y -= 1
        elif direction == "d" and self.case_y < self.max_case_y:
            self.case_y += 1
        elif direction == "l" and self.case_x > self.min_case_x :
            self.case_x -= 1
        elif direction == "r" and self.case_x < self.max_case_x:
            self.case_x += 1
        return self.map[self.case_y][self.case_x]
    
    def map_border(self):
        if self.case_x == self.max_case_x:
            self.border["right"] = 0
        else:
            self.border["right"] = 1

        if self.case_x == self.min_case_x:
            self.border["left"] = 0
        else:
            self.border["left"] = 1

        if self.case_y == self.max_case_y:
            self.border["down"] = 0
        else:
            self.border["down"] = 1

        if self.case_y == self.min_case_y:
            self.border["up"] = 0
        else: 
            self.border["up"] = 1
        
        return self.border