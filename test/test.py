import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Création d'une surface "bras" fictive (100x40), rouge, pointant vers la gauche
arm_img = pygame.Surface((100, 40), pygame.SRCALPHA)
pygame.draw.rect(arm_img, (255, 0, 0), (0, 0, 100, 40))
# Repère le point midright (pivot) en vert
pygame.draw.circle(arm_img, (0, 255, 0), (arm_img.get_width()-1, arm_img.get_height()//2), 5)

# Point fixe où le bras doit être accroché
pivot_pos = pygame.Vector2(400, 300)

def rotate_around_midright(image, pivot_pos, target_pos):
    # Calcul du vecteur direction vers la souris
    direction = pygame.Vector2(target_pos) - pivot_pos
    # Angle entre la direction et la direction gauche (-1, 0)
    angle = direction.angle_to(pygame.Vector2(-1, 0))

    # Rotation de l'image
    rotated_image = pygame.transform.rotate(image, angle)

    # Offset entre centre et midright dans l'image d'origine
    orig_rect = image.get_rect()
    pivot_offset = pygame.Vector2(orig_rect.width, orig_rect.height / 2)

    # Rotation de l'offset
    rotated_offset = pivot_offset.rotate(-angle)

    # Calcul du nouveau topleft pour que midright = pivot_pos
    new_topleft = pivot_pos - rotated_offset

    # Rect de l'image pivotée
    rotated_rect = rotated_image.get_rect(topleft=new_topleft)

    return rotated_image, rotated_rect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_pos = pygame.mouse.get_pos()

    screen.fill((30, 30, 30))

    # Affiche le pivot fixe en vert
    pygame.draw.circle(screen, (0, 255, 0), (int(pivot_pos.x), int(pivot_pos.y)), 5)

    # Rotation du bras autour du pivot
    rotated_arm, arm_rect = rotate_around_midright(arm_img, pivot_pos, mouse_pos)
    screen.blit(rotated_arm, arm_rect)

    pygame.display.flip()
    clock.tick(60)
