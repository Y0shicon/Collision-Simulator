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
pygame.display.set_caption('Simulation')
clock = pygame.time.Clock()


def simulation(win):

    sphereList, coefficientOfRestitution = mainScreen(win)

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

    def collision(obj1, obj2):
        m1 = obj1.mass/1000
        m2 = obj2.mass/1000
        u1x = obj1.xVel
        u2x = obj2.xVel
        u1y = obj1.yVel
        u2y = obj2.yVel
        e = coefficientOfRestitution

        # =========================================> Eqn Solver method <==============================================

        ''' m1u1 + m2u2 = m1v1 + m2v2 ==> m1u2 + m2u2 -> Constant
            m1/2 * u1**2 + m2/2 * u2**2 = m1/2 *v1**2 + m2
                                            
        v1x, v2x, v1y, v2y = symbols('v1x v2x v1y v2y')
        eqn1 = [m1*v1x + m2*v2x - m1*u1x - m2*u2x, m1/2*v1x**2 + m2/2*v2x**2 - m1/2*u1x**2 - m2/2*u2x**2]
        eqn2 = [m1*v1y + m2*v2y - m1*u1y - m2*u2y, m1/2*v1y**2 + m2/2*v2y**2 - m1/2*u1y**2 - m2/2*u2y**2]



        obj1.xVel, obj2.xVel = int(solve(eqn1)[1][v1x]), int(solve(eqn1)[1][v2x])
        obj1.yVel, obj2.yVel = int(solve(eqn2)[1][v1y]), int(solve(eqn2)[1][v2y])

        print(obj1.xVel, obj1.yVel, obj2.xVel, obj2.yVel)'''

        # =========================================> Direct Method <===============================================

        if checkHeadOn(obj1, obj2):
            obj1.xVel = int(((m1-e*m2)/(m1+m2))*u1x + ((1+e)*m2/(m1+m2))*u2x)
            obj2.xVel = int(((1+e)*m1/(m1+m2))*u1x + ((m2-e*m1)/(m1+m2))*u2x)

            obj1.yVel = int(((m1-e*m2)/(m1+m2))*u1y + ((1+e)*m2/(m1+m2))*u2y)
            obj2.yVel = int(((1+e)*m1/(m1+m2))*u1y + ((m2-e*m1)/(m1+m2))*u2y)

        else:
            y = abs(obj1.y - obj2.y)
            x = abs(obj1.x - obj2.x)
            commonNormalAngle = atan(y/x) if x != 0 else 90
            u1cn = u1x * cos(commonNormalAngle) + u1y * sin(commonNormalAngle)
            u2cn = u2x * cos(commonNormalAngle) + u2y * sin(commonNormalAngle)
            u1ct = v1ct = u1y * cos(commonNormalAngle) + \
                u1x * sin(commonNormalAngle)
            u2ct = v2ct = u2y * cos(commonNormalAngle) + \
                u2x * sin(commonNormalAngle)

            a = np.array([[m1, m2], [-1, 1]])
            b = np.array([m1*u1cn + m2*u2cn, e*(u2cn - u1cn)])

            v2cn, v1cn = np.linalg.solve(a, b)

            print(
                'm1 - ', m1,
                '\nm2 - ',  m2,
                '\nu1x - ', u1x,
                '\nu2x - ', u2x,
                '\nu1y - ', u1y,
                '\nu2y - ', u2y,
                '\ntheta -', degrees(commonNormalAngle),
                '\nu1cn -', u1cn,
                '\nu2cn - ', u2cn,
                '\nu1ct = v1ct - ', u1ct,
                '\nu2ct = v2ct - ', u2ct,
                '\nv1cn - ', v1cn,
                '\nv2cn - ', v2cn
            )

            #v1cn, v2cn = round(v1cn), round(v2cn)

            obj1.xVel = v1cn * cos(commonNormalAngle) + v1ct * sin(commonNormalAngle)

            obj1.yVel = v1ct * cos(commonNormalAngle) + v1cn * sin(commonNormalAngle)

            obj2.xVel = v2cn * cos(commonNormalAngle) + v2ct * sin(commonNormalAngle)

            obj2.yVel = v2ct * cos(commonNormalAngle) + v2cn * sin(commonNormalAngle)

            '----------------> Configuring the directions <---------------------'
            
            ''' Dividing the circle to 4 quarters -
            1) 1st quarter = 45 - 135 ==> Top Collision
            2) 2nd quarter = 135 - 225 ==> Left Collision
            3) 3rd quarter = 225 - 315 ==> Bottom Collision
            4) 4th quarter = 315 - 45 ==> Right Collision
            Extra - 1) At 45 ==> Top and Right Collision
                    2) At 135 ==> Top and Left Collision
                    3) At 225 ==> Bottom and Left Collision
                    4) At 315 ==> Bottom and Right Collision'''

            #To check which quarter is the collision taking place in, we check the common normal angle
            
            y = obj1.y - obj2.y
            x = obj1.x - obj2.x
            theta = degrees(atan(y/x)) if x != 0 else 90
            theta = theta if theta >= 0 else 360 + theta
            print('Theta(non absolute) - ', theta)

            #Both Top and Bottom collision have same results
            if 45 < theta < 135 or 225 < theta < 315:
                
                if u1x > 0:
                    obj1.xVel = abs(obj1.xVel)

                elif abs(u1x) < 0:
                    if u2x > 0:
                        obj1.xVel = abs(obj1.xVel)
                    
                    elif u2x == 0:
                        if obj1.x > obj2.x:
                            obj1.xVel = abs(obj1.xVel)
                            obj2.xVel = abs(obj2.xVel) * -1
                        else:
                            obj1.xVel = abs(obj1.xVel) * -1
                            obj2.xVel = abs(obj2.xVel) 

                    else:
                        obj1.xVel = abs(obj1.xVel) * -1
                else:
                    obj1.xVel = abs(obj1.xVel) * -1

                if u2x > 0:
                    obj2.xVel = abs(obj2.xVel)

                elif u2x == 0:
                    if u1x > 0:
                        obj2.xVel = abs(obj2.xVel)
                    
                    elif abs(u1x) < 0:
                        if obj1.x > obj2.x:
                            obj1.xVel = abs(obj1.xVel)
                            obj2.xVel = abs(obj2.xVel) * -1
                        else:
                            obj1.xVel = abs(obj1.xVel) * -1
                            obj2.xVel = abs(obj2.xVel) 

                    else:
                        obj2.xVel = abs(obj2.xVel) * -1
                else:
                    obj2.xVel = abs(obj2.xVel) * -1

                #Changing y - directions
                if u1y > 0.7 :
                    obj1.yVel = abs(obj1.yVel) * -1

                elif abs(u1y) < 0.7 :
                    if u2y > 0.7 :
                        obj1.yVel = abs(obj1.yVel) 
                    
                    elif abs(u2y) < 0.7 :
                        if obj1.y > obj2.y:
                            obj1.yVel = abs(obj1.yVel)
                            obj2.yVel = abs(obj2.yVel) * -1
                        else:
                            obj1.yVel = abs(obj1.yVel) * -1
                            obj2.yVel = abs(obj2.yVel) 

                    else:
                        obj1.yVel = abs(obj1.yVel) * -1
                else:
                    obj1.yVel = abs(obj1.yVel)

                if u2y > 0.7 :
                    obj2.yVel = abs(obj2.yVel) * -1

                elif abs(u2y) < 0.7 :
                    if u1y > 0.7 :
                        obj2.yVel = abs(obj2.yVel) 
                    
                    elif abs(u1y) < 0.7 :
                        if obj1.y > obj2.y:
                            obj1.yVel = abs(obj1.yVel)
                            obj2.yVel = abs(obj2.yVel) * -1
                        else:
                            obj1.yVel = abs(obj1.yVel) * -1
                            obj2.yVel = abs(obj2.yVel) 

                    else:
                        obj2.yVel = abs(obj2.yVel) * -1
                else:
                    obj2.yVel = abs(obj2.yVel)

            #Both Left and Right collision have same results
            if 135 < theta < 225 or 315 < theta < 360 or 0 < theta < 45:
                
                if u1x > 0.7:
                    obj1.xVel = abs(obj1.xVel) * -1

                elif abs(u1x) < 0.7:
                    if u2x > 0.7:
                        obj1.xVel = abs(obj1.xVel)
                    
                    elif u2x == 0.7:
                        if obj1.x > obj2.x:
                            obj1.xVel = abs(obj1.xVel)
                            obj2.xVel = abs(obj2.xVel) * -1
                        else:
                            obj1.xVel = abs(obj1.xVel) * -1
                            obj2.xVel = abs(obj2.xVel) 

                    else:
                        obj1.xVel = abs(obj1.xVel) * -1
                else:
                    obj1.xVel = abs(obj1.xVel)

                if u2x > 0.7:
                    obj2.xVel = abs(obj2.xVel) * -1

                elif u2x == 0.7:
                    if u1x > 0.7:
                        obj2.xVel = abs(obj2.xVel)
                    
                    elif abs(u1x) < 0.7:
                        if obj1.x > obj2.x:
                            obj1.xVel = abs(obj1.xVel)
                            obj2.xVel = abs(obj2.xVel) * -1
                        else:
                            obj1.xVel = abs(obj1.xVel) * -1
                            obj2.xVel = abs(obj2.xVel) 

                    else:
                        obj2.xVel = abs(obj2.xVel) * -1
                else:
                    obj2.xVel = abs(obj2.xVel)

                if u1y > 0:
                    obj1.yVel = abs(obj1.yVel) 

                elif u1y == 0:
                    if u2y > 0:
                        obj1.yVel = abs(obj1.yVel) 
                    
                    elif u2y == 0:
                        if obj1.y > obj2.y:
                            obj1.yVel = abs(obj1.yVel)
                            obj2.yVel = abs(obj2.yVel) * -1
                        else:
                            obj1.yVel = abs(obj1.yVel) * -1
                            obj2.yVel = abs(obj2.yVel) 

                    else:
                        obj1.yVel = abs(obj1.yVel) * -1
                else:
                    obj1.yVel = abs(obj1.yVel) * -1

                if u2y > 0:
                    obj2.yVel = abs(obj2.yVel)

                elif u2y == 0:
                    if u1y > 0:
                        obj2.yVel = abs(obj2.yVel) 
                    
                    elif u1y == 0:
                        if obj1.y > obj2.y:
                            obj1.yVel = abs(obj1.yVel)
                            obj2.yVel = abs(obj2.yVel) * -1
                        else:
                            obj1.yVel = abs(obj1.yVel) * -1
                            obj2.yVel = abs(obj2.yVel) 

                    else:
                        obj2.yVel = abs(obj2.yVel) * -1
                else:
                    obj2.yVel = abs(obj2.yVel) * -1


            print(
                #'v1cn rounded - ', v1cn,
                #'\nv2cn rounded - ', v2cn,
                '\nSphere 1 x Vel - ', obj1.xVel,
                '\nSphere 1 y Vel - ', obj1.yVel,
                '\nSphere 2 x Vel - ', obj2.xVel,
                '\nSphere 2 y Vel - ', obj2.yVel
            )

        while abs(findDistance(obj1, obj2) < (obj1.radius + obj2.radius)):
            if not obj1.xVel and not obj1.yVel and not obj2.xVel and not obj2.yVel:
                break
            obj1.move(collisionRect)
            obj2.move(collisionRect)
            updateWin()

    def stop():
        global run, restartVar
        run = False
        restartVar = False

    def restart():
        global run, restartVar
        run = False
        restartVar = True

    def updateWin():
        win.fill((64,224,208))

        pygame.draw.rect(win, (255,255,255), collisionRect, border_radius=10)
        pygame.draw.rect(win, (0,0,0), collisionRect, 5, border_radius=10)

        # Displaying the axis
        win.blit(axisImg, (-5, 205))

        # Displaying the buttons
        stopButton.draw()
        restartButton.draw()

        # Displaying all circles
        for i in range(numObjects):
            sphereList[i].draw(win)

        # Displaying all velocity Displayers
        for i in range(numObjects):
            velocityDisplayList[i].draw(win, center=True)

        pygame.display.update()

    global run, restartVar

    restartVar = True
    numObjects = len(sphereList)
    velocityDisplayList = list()
    i = 0
    for sphere in sphereList:
        velocityDisplayList.append(displayVelocity(
            sphere.xVel, sphere.yVel, sphere.mass, (screenWidth//2 - 100, 10 + 50 * i), 20, sphere.color))
        i += 1

    collisionRect = pygame.Rect(10, 200,  screenWidth - 20, 500)
    axisImg = pygame.image.load(
        r'D:\More Python Projects\Games\Collitions Experiment\Collision Simulator\Images\cartesianPlane.png')
    axisImg = pygame.transform.scale(axisImg, (320, 180))
    stopButton = Button(win, screenWidth - 100, 10, 90,
                        40, onClick=stop, text='STOP')
    restartButton = Button(win, screenWidth - 200, 10,
                           90, 40, onClick=restart, text='RESTART')
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            clock.tick(240)
        elif keys[pygame.K_LEFT]:
            clock.tick(20)
        else:
            clock.tick((60))

        # Moving all spheres
        for sphere in sphereList:
            sphere.move(collisionRect)

        # Displaying velocities
        for i in range(numObjects):
            velocityDisplayList[i].speedUpdate(
                sphereList[i].xVel, sphereList[i].yVel)

        # Checking for collision between all circles
        for i in range(numObjects):
            for j in range(i + 1, numObjects):
                if abs(findDistance(sphereList[i], sphereList[j])) < sphereList[i].radius + sphereList[j].radius:
                    collision(sphereList[i], sphereList[j])

        stopButton.listen(events)
        restartButton.listen(events)

        updateWin()
    else:
        print(restartVar)
        return restartVar

if __name__ == '__main__':
    simulation(win)