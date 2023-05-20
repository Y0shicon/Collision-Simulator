import sys
from math import atan, degrees, sqrt
from random import randint, uniform

import pygame
from pygame_widgets import *

from classes import *

from startScreen import mainScreen
from Simulation_v2 import simulation

__name__ = 'Collision Simulator'
__author__ = 'Yoshicon'


pygame.init()
screenWidth, screenHeight = 1280, 720
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Set the initial parameters')
clock = pygame.time.Clock()

retryVar = True
while retryVar:
    retryVar = simulation(win)
