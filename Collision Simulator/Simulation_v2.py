import sys
from math import atan, degrees, sqrt, cos, sin
from random import randint, uniform
from sympy import solve, symbols
import numpy as np

import pygame
from pygame_widgets import *

from classes import *

from startScreen import mainScreen

pygame.init()
screenWidth, screenHeight = 1280, 720
win = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()


def simulation(win):

    sphereList, coefficientOfRestitution = mainScreen(win)
    pygame.display.set_caption('Simulation')

    def findDistance(obj1, obj2):
        x1 = obj1.x
        x2 = obj2.x
        y1 = obj1.y
        y2 = obj2.y

        return sqrt((x1-x2)**2 + (y1-y2)**2)

    def checkHeadOn(obj1, obj2):

        print('Object 1 angle :', obj1.angle, '\nObject 2 angle :', obj2.angle)
        y = abs(obj1.y - obj2.y)
        x = abs(obj1.x - obj2.x)

        commonNormalAngle = degrees(atan(y/x)) if x != 0 else 90
        print('Common Normal Angle :', commonNormalAngle)
        if abs(obj1.angle - obj2.angle) < 7 and (abs(commonNormalAngle - obj1.angle) < 7 or abs(commonNormalAngle - obj2.angle) < 7):
            print('Head On Collision')
            return True
        print('Oblique Collision')
        return False

    def collision(obj1, obj2, neg = 1):
        m1 = obj1.mass/1000
        m2 = obj2.mass/1000
        u1x = obj1.xVel * neg
        u2x = obj2.xVel * neg
        u1y = obj1.yVel * neg
        u2y = obj2.yVel * neg
        e = coefficientOfRestitution

        u1 = pygame.math.Vector2(u1x, u1y)
        u2 = pygame.math.Vector2(u2x, u2y)
        x1 = pygame.math.Vector2(obj1.x, obj1.y)
        x2 = pygame.math.Vector2(obj2.x, obj2.y)

        v1 = u1 - 2*m2/(m1+m2) * ((u1 - u2).dot(x1-x2)) / \
            ((x1-x2).length())**2 * (x1-x2)
        v2 = u2 - 2*m1/(m1+m2) * ((u2 - u1).dot(x2-x1)) / \
            ((x2-x1).length())**2 * (x2-x1) 

        obj1.xVel = v1.x * neg
        obj1.yVel = v1.y * neg

        obj2.xVel = v2.x * neg
        obj2.yVel = v2.y * neg

        while abs(findDistance(obj1, obj2) < (obj1.radius + obj2.radius)):
            if not obj1.xVel and not obj1.yVel and not obj2.xVel and not obj2.yVel:
                break
            obj1.move(collisionRect, neg)
            obj2.move(collisionRect, neg)
            updateWin()

    def stop():
        global run, restartVar
        run = False
        restartVar = False

    def restart():
        global run, restartVar
        run = False
        restartVar = True

    def showGrid():
        global showGridBool
        showGridBool = not(showGridBool)

    def showArrow():
        global showArrowBool
        showArrowBool = not(showArrowBool)

    def movement(neg = 1):
        # Moving all spheres
        for sphere in sphereList:
            sphere.move(collisionRect, neg)

        infoDisplayer.speedUpdate()

        # Checking for collision between all circles
        for i in range(numObjects):
            for j in range(i + 1, numObjects):
                if abs(findDistance(sphereList[i], sphereList[j])) < sphereList[i].radius + sphereList[j].radius:
                    collision(sphereList[i], sphereList[j], neg)

    def updateWin():
        win.fill((64, 224, 208))

        # Collision Window - Surface
        pygame.draw.rect(win, (255, 255, 255), collisionRect, border_radius=10)
        pygame.draw.rect(win, (0, 0, 0), collisionRect, 5, border_radius=10)

        # Showing the grid
        if showGridBool:
            for i in range(collisionRect.left + 15, collisionRect.right - 15, 20):
                pygame.draw.line(
                    win, (120, 120, 120), (i, collisionRect.top), (i, collisionRect.bottom))
            for i in range(collisionRect.top + 15, collisionRect.bottom - 15, 20):
                pygame.draw.line(
                    win, (120, 120, 120), (collisionRect.left, i), (collisionRect.right, i))
            # Darker Lines for references
            for i in range(collisionRect.left + 15, collisionRect.right - 15, 100):
                pygame.draw.line(
                    win, (90, 90, 90), (i, collisionRect.top), (i, collisionRect.bottom), width=2)
            for i in range(collisionRect.top + 15, collisionRect.bottom - 15, 100):
                pygame.draw.line(
                    win, (90, 90, 90), (collisionRect.left, i), (collisionRect.right, i), width=2)

        # Showing all arrows if button pressed
        if showArrowBool:
            for sphere in sphereList:
                sphere.showProjectileArrow(win)

        # Showing the simulator controllers
        if paused:
            playButton.draw()
        else:
            pauseButton.draw()
        rewindButton.draw()
        forwardButton.draw()

        # Displaying the axis
        win.blit(axisImg, (-5, 205))

        # Displaying the buttons
        stopButton.draw()
        restartButton.draw()
        showArrowButton.draw()
        showGridButton.draw()

        # Displaying all circles
        for i in range(numObjects):
            sphereList[i].draw(win)

        # Displaying all velocity Displayers
        pygame.draw.rect(win, (255, 255, 255), infoBoxRect, border_radius=10)
        pygame.draw.rect(win, (0, 0, 0), infoBoxRect, 5, border_radius=10)
        infoBoxText.draw(win, center=True)
        infoDisplayer.draw()

        pygame.display.update()

    numObjects = len(sphereList)
    infoBoxRect = pygame.Rect(10, 15, screenWidth - 220, 175)
    infoBoxText = textOnScreen('Info for all spheres', 40, (231, 53, 142),
                               infoBoxRect.left + infoBoxRect.width // 2, infoBoxRect.top + 25, font='lintxt')
    infoDisplayer = mDisplayInfoInSim(sphereList, win)

    collisionRect = pygame.Rect(10, 200,  screenWidth - 20, 500)

    axisImg = pygame.image.load(
        r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\cartesianPlane.png')
    axisImg = pygame.transform.scale(axisImg, (320, 180))

    stopButton = Button(win, screenWidth - 100, 30, 90,
                        40, onClick=stop, text='STOP')
    restartButton = Button(win, screenWidth - 200, 30,
                           90, 40, onClick=restart, text='RESTART')
    showGridButton = Button(win, screenWidth - 100, 75,
                            90, 40, onClick=showGrid, text='Show Grid')
    showArrowButton = Button(win, screenWidth - 200,
                             75, 90, 40, onClick=showArrow, text='Show Arrow')

    #! Defining the controller buttons in form of images and scaling them down to '50 x 50' images
    # ?To pause the simulation
    pauseButton = clickableImage(r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\pause.png',
                                    win, (collisionRect.centerx, collisionRect.top + 35), (50,50))
    # ?To resume the simulation
    playButton = clickableImage(r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\play.png',
                                 win, (collisionRect.centerx, collisionRect.top + 35), (50,50))

    # ?Forward and backward buttons
    rewindButton = clickableImage(r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\rewind.png',
                                  win, (collisionRect.centerx - 90, collisionRect.top + 35), (70,50),
                                  onClickImgPath = r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\rewindPressed.png')
    forwardButton = clickableImage(r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\forward.png',
                                  win, (collisionRect.centerx + 90, collisionRect.top + 35), (70,50),
                                  onClickImgPath =  r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\forwardPressed.png')

    global run, restartVar, showArrowBool, showGridBool, paused

    showArrowBool = False
    showGridBool = False
    restartVar = True
    paused = False
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                # ? Checking for hovering over controller buttons
                if pauseButton.rect.collidepoint(event.pos) or rewindButton.rect.collidepoint(event.pos) or forwardButton.rect.collidepoint(event.pos):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                #! Describing functions for each controller button
                #? Pause Button
                if pauseButton.rect.collidepoint(event.pos):
                    paused = not paused
                #? Forward Button
                elif forwardButton.rect.collidepoint(event.pos):
                    movement()
                    forwardButton.clicked()
                    
                #? Rewind Button
                #todo FIX REWIND BUTTON - DONE
                elif rewindButton.rect.collidepoint(event.pos):
                    movement(neg = -1)
                    rewindButton.clicked()
                    
            if event.type == pygame.MOUSEBUTTONUP:
                #! Changing the images back to the original ones
                #? Pause Button
                if pauseButton.rect.collidepoint(event.pos):
                    pauseButton.clicked()
                    
                #? Forward Button
                elif forwardButton.rect.collidepoint(event.pos):
                    forwardButton.clicked()
                    
                #? Rewind Button
                #todo FIX REWIND BUTTON - DONE
                elif rewindButton.rect.collidepoint(event.pos):
                    rewindButton.clicked()
                        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            clock.tick(150)
        elif keys[pygame.K_LEFT]:
            clock.tick(20)
        else:
            clock.tick((60))
            
        if not paused:
            movement()

        stopButton.listen(events)
        restartButton.listen(events)
        showArrowButton.listen(events)
        showGridButton.listen(events)

        updateWin()
        
    else:
        
        print(restartVar)
        return restartVar


if __name__ == '__main__':
    simulation(win)
