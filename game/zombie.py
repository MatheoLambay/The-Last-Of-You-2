import pygame
import math

class Zombie(pygame.sprite.Sprite):
    def __init__(self, screen, link, x, y, name, life, attack, gold, xp, velocity, scale=1):
        super().__init__()
        self.screen = screen

        self.original_image = pygame.image.load(link).convert_alpha()
        width = self.original_image.get_width()
        height = self.original_image.get_height()
        self.original_image = pygame.transform.scale(self.original_image, (int(width * scale), int(height * scale)))

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.name = name
        self.life = life
        self.attack = attack
        self.x = x
        self.y = y
        self.velocity = velocity
        self.angle = 0
        self.last_angle = None

        self.xp = xp
        self.gold = gold

    def point_at(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        
        if self.last_angle is None or abs(angle - self.last_angle) > 2:
            self.last_angle = angle
            adjusted_angle = angle - 90
            self.image = pygame.transform.rotate(self.original_image, -adjusted_angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def move_to(self, targetx, targety):
        direction = pygame.math.Vector2(targetx - self.x, targety - self.y)
        if direction.length_squared() != 0:
            direction = direction.normalize() * self.velocity
            self.x += direction.x
            self.y += direction.y
            self.rect.center = (self.x, self.y)

    def Attack(self, cible):
        cible.life -= self.attack

    def drop_gold(self, cible):
        cible.gold += self.gold

    def update(self, player, player_in_safezone):
        
        if self.life > 0:
            if not player_in_safezone:
                self.point_at((player.x, player.y))
                self.move_to(player.x, player.y)
        else:
            self.kill()

    def draw(self):
        if self.screen.get_rect().colliderect(self.rect):
            self.screen.blit(self.image, self.rect)
