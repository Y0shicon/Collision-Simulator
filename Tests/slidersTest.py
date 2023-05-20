import pygame
from pygame_widgets import *

pygame.init()
win = pygame.display.set_mode((1200,700))
pygame.display.set_caption('Sliders')

class IncreasingSlider(object):
    def __init__(self, pos, width, height, win):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.slider = Slider(win, self.x, self.y, self.width, self.height, min = -10, max = 10, step =  1)
        self.textbox = TextBox(win, self.x, self.y + self.height + 20, self.width, self.height)

    def draw(self):
        self.textbox.draw()
        self.slider.draw()

controller = IncreasingSlider((150,150), 400, 100, win)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    controller.textbox.listen(events)
    controller.slider.listen(events)

    controller.textbox.setText(controller.slider.getValue())

    win.fill((255,255,255))
    controller.draw()
    pygame.display.update()


pygame.quit()