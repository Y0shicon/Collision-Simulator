import pygame
from pygame_widgets import *
import sys

pygame.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('The Button')

def clicked():
    print('Clicked')

button1 = Button(win, 640, 360, 100, 40, onClick = clicked)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

    win.fill((0,0,0))
    button1.listen(events)
    button1.draw()
    pygame.display.update()