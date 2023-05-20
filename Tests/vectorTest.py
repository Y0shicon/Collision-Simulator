import pygame
import sys

from classes import Spheres

pygame.init()

win = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Vectors')


v1 = pygame.math.Vector2(3,4)
v2 = pygame.math.Vector2(3,6)

print(v1.distance_to(v2))

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
    