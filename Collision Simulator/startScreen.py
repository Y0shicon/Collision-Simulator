import sys
from math import atan, degrees, sqrt
from random import randint, uniform

import pygame
from pygame_widgets import *

from classes import *

pygame.init()
screenWidth, screenHeight = 1280, 720
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Set the initial parameters')
clock = pygame.time.Clock()

def mainScreen(startWin):

    def checkShowData():
        for i in range(len(sphereList)):
            if sphereList[i].showInfo:
                return True, i
        
        return False, False


    def checkCollisionMouse():
        for i in sphereList:
            if i.rectHitbox.collidepoint(pygame.mouse.get_pos()):
                return True, i

        return False, False

    def output():
        global nSpheres
        # Get text in the textbox
        nSpheres = round((float(textbox.getText()))) if textbox.getText() != '' else 0
        print('No. of sphere -', nSpheres)

    def EOutput():
        global e
        e = float(coefficientOfRestitution.getText())
        print('e -', e)


    def closeInfo(sphere):
        for i in sphereList:
            if i != sphere:
                i.showInfo = False

    def startSim():
        global run
        run = False
        pygame.time.delay(500)

    def showGrid():
        global showGridBool
        showGridBool = not(showGridBool)

    def showArrow():
        global showArrowBool
        showArrowBool = not(showArrowBool)

    def clearSphereList():
        global sphereList, nSpheres, textbox
        sphereList = []
        nSpheres = 0
        textbox = TextBox(startWin, screenWidth - 90, screenHeight - 80, 60, 50, fontSize=40,
                      borderColour=(255, 0, 0), textColour=(0, 200, 0),
                      onSubmit=output, radius=10, borderThickness=5)
        textbox.setText('')

    def updateWin(): 

        startWin.fill((64,224,208))

        #Collision Window - Section
        pygame.draw.rect(startWin, (255,255,255), collisionRect, border_radius=10)
        pygame.draw.rect(startWin, (0,0,0), collisionRect, 5, border_radius=10)

        #Showing the grid
        if showGridBool:
            for i in range(collisionRect.left + 15, collisionRect.right - 15, 20):
                pygame.draw.line(startWin, (120,120,120), (i,collisionRect.top), (i, collisionRect.bottom))
            for i in range(collisionRect.top + 15, collisionRect.bottom - 15, 20):
                pygame.draw.line(startWin, (120,120,120), (collisionRect.left, i), (collisionRect.right, i))
            #Darker Lines for references
            for i in range(collisionRect.left + 15, collisionRect.right - 15, 100):
                pygame.draw.line(startWin, (90,90,90), (i,collisionRect.top), (i, collisionRect.bottom), width=2)
            for i in range(collisionRect.top + 15, collisionRect.bottom - 15, 100):
                pygame.draw.line(startWin, (90,90,90), (collisionRect.left, i), (collisionRect.right, i), width = 2)

        #Showing all arrows if button pressed
        if showArrowBool:
            for sphere in sphereList:
                sphere.showProjectileArrow(win)

        #Showing Axis
        startWin.blit(axisImg, (-5,205))

        #Displaying all the widgets
        textForTextbox.draw(startWin, center=True)
        textbox.draw()
        coefficientOfRestitution.draw()
        coefficientOfRestitutionText.draw(startWin, center=True)
        startButton.draw()
        showGridButton.draw()
        showArrowButton.draw()
        clearButton.draw()

        # Displaying all spheres
        for sphere in sphereList[::-1]:
            sphere.draw(startWin)

        #Showing editable parameters for the clicked sphere
        if checkShowData()[0]:
            pygame.draw.rect(startWin, (230, 140, 31),
                            (20, 20, screenWidth - 140, 151), border_radius=25)
            sphereList[checkShowData()[1]].showData(startWin)

            coefficientOfRestitution.draw()

        pygame.display.update()


    global textForTextbox, textbox, e

    #No of spheres
    textForTextbox = textOnScreen(
        'Enter the number of Spheres', 23, (255, 0, 0), screenWidth - 270, screenHeight - 50)
    textbox = TextBox(startWin, screenWidth - 90, screenHeight - 80, 60, 50, fontSize=40,
                      borderColour=(255, 0, 0), textColour=(0, 200, 0),
                      onSubmit=output, radius=10, borderThickness=5)
    textbox.setText('')

    #Coefficient of restitution
    coefficientOfRestitutionText = textOnScreen('Coefficient of Restitution', 23, (0,255,0), screenWidth - 250, screenHeight - 100)
    coefficientOfRestitution = TextBox(startWin, screenWidth - 85, screenHeight - 140, 50, 50, fontSize=35,
                    borderColour=(255, 0, 0), textColour=(0, 200, 0),
                    onSubmit=EOutput, radius=10, borderThickness=5)                    
    e = 1
    coefficientOfRestitution.setText(str(e))
    
    axisImg = pygame.image.load(r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\cartesianPlane.png')
    axisImg = pygame.transform.scale(axisImg, (320,180))

    #ALL BUTTONS
    startButton = Button(startWin, screenWidth - 100, 15, 90, 40, onClick = startSim, text = 'START')
    clearButton = Button(startWin, screenWidth - 100, 60, 90, 40, onClick = clearSphereList, text = 'Clear')
    showGridButton = Button(startWin, screenWidth - 100, 105, 90, 40, onClick = showGrid, text = 'Show Grid')
    showArrowButton = Button(startWin, screenWidth -100, 150, 90, 45, onClick = showArrow, text = 'Show Arrow')

    collisionRect = pygame.Rect(10, 200,  screenWidth - 20, 500)
    
    global showArrowBool, showGridBool, indragging, sphereList,  nSpheres, run

    nSpheres = 0
    showGridBool = False
    showArrowBool = False
    indragging = False

    sphereList = list()

    run = True    
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if checkCollisionMouse()[0]:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            '''if event.type == pygame.MOUSEBUTTONDOWN:
                if checkCollisionMouse()[0]:
                    for sphere in sphereList:
                        sphere.showInfo = False'''

        # Dragging the spheres using mouse
        if checkCollisionMouse()[0] or indragging:
            if pygame.mouse.get_pressed()[0]:
                indragging = True

                #Checking for borders
                if checkCollisionMouse()[1] != False:
                    objectInDrag = checkCollisionMouse()[1]
                objectInDrag.showInfo = True                   
                
                # -----> Turns the showInfo parameter of all spheres to False except the given <------
                closeInfo(objectInDrag)

                #Checking for borders
                if objectInDrag.rectHitbox.left > collisionRect.left and objectInDrag.rectHitbox.right < collisionRect.right:
                    objectInDrag.x = pygame.mouse.get_pos()[0]
                elif objectInDrag.rectHitbox.left <= collisionRect.left:
                    objectInDrag.x = collisionRect.left + objectInDrag.radius + 10
                elif objectInDrag.rectHitbox.right >= collisionRect.right:
                    objectInDrag.x = collisionRect.right - objectInDrag.radius - 10
                
                if objectInDrag.rectHitbox.top > collisionRect.top and objectInDrag.rectHitbox.bottom < collisionRect.bottom:
                    objectInDrag.y = pygame.mouse.get_pos()[1]
                elif objectInDrag.rectHitbox.top < collisionRect.top:
                    objectInDrag.y = collisionRect.top + objectInDrag.radius + 10
                elif objectInDrag.rectHitbox.bottom >= collisionRect.bottom:
                    objectInDrag.y = collisionRect.bottom - objectInDrag.radius - 10
            
            else:
                indragging = False
                objectInDrag = None


        if nSpheres > len(sphereList):
            for i in range(nSpheres - len(sphereList)):
                sphereList.append(
                    Spheres(collisionRect.center, startWin))

        #! All sliders, Start Button and textboxes updating
        for i in sphereList:
            if i.showInfo:
                i.xVelSlider.listen(events)
                i.yVelSlider.listen(events)
                i.radiusSlider.listen(events)
                i.densitySlider.listen(events)
                break
        textbox.listen(events)
        coefficientOfRestitution.listen(events)
        startButton.listen(events)
        showGridButton.listen(events)
        showArrowButton.listen(events)
        clearButton.listen(events)

        updateWin()

        clock.tick(240)

    else:
        return sphereList, e

if __name__ == '__main__':
    mainScreen(win)