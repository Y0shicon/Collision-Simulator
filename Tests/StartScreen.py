import pygame
from math import atan, degrees, sqrt
from random import randint, uniform
import sys
from classes import *


def startScreen():
    pygame.init()
    screenWidth, screenHeight = 800, 600
    startWin = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('Set the initial parameters')
    clock = pygame.time.Clock()

    def updateWin():
        startWin.fill((135, 206, 235))

        nSpheresText.draw(startWin)

        # Displaying all spheres
        for sphere in sphereList[::-1]:
            sphere.draw(startWin)

        if showInfo:
            pygame.draw.rect(startWin, (230, 140, 31),
                             (screenWidth - 100, 200, 101, 150), 2)

        pygame.display.update()

    def checkCollisionMouse():
        for i in sphereList:
            if i.rectHitbox.collidepoint(pygame.mouse.get_pos()):
                return True, i
        else:
            return False, False

    nSpheresText = mTextBox('0', (screenWidth//2, 40), (150, 250, 100))

    showInfo = False
    run = True
    sphereList = list()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if nSpheresText.rect.collidepoint(event.pos):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_IBEAM)

                elif checkCollisionMouse()[0]:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if nSpheresText.rect.collidepoint(event.pos):
                    nSpheresText.activateTyping = True
                    nSpheresText.text = ''
                else:
                    nSpheresText.activateTyping = False

            if event.type == pygame.KEYDOWN and nSpheresText.activateTyping:
                if event.key == pygame.K_BACKSPACE:
                    nSpheresText.text = nSpheresText.text[: -1]
                elif event.key == pygame.K_RETURN:
                    nSpheresText.activateTyping == False
                    nSpheresText.num = int(nSpheresText.text)

                elif event.unicode.isnumeric():
                    nSpheresText.text += event.unicode

        # Dragging the spheres using mouse
        if checkCollisionMouse()[1]:
            if pygame.mouse.get_pressed()[0]:
                showInfo = True
                'checkCollisionMouse()[1].show(startWin)'
                checkCollisionMouse()[1].x = pygame.mouse.get_pos()[0]
                checkCollisionMouse()[1].y = pygame.mouse.get_pos()[1]

        if nSpheresText.num > 0:
            for i in range(nSpheresText.num - len(sphereList)):
                if i < 0:
                    break
                    print('Broke')
                sphereList.append(
                    Spheres((screenWidth//2, screenHeight//2), startWin))

        updateWin()

        clock.tick(60)


startScreen()
