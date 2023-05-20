import pygame
from random import randint, choice
from math import fabs

pygame.init()

width = 800
height = 600

win = pygame.display.set_mode((width,height))
pygame.display.set_caption('Collitions of Rectangles')

clock =  pygame.time.Clock()

class Rectangles(object):
    def __init__(self, pos, width, height):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.xVel = randint(-7, 7)
        self.yVel = randint(-7, 7)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def drawRect (self, win):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #self.rect.center = (self.x, self.y)
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        #left boundary and right boundary
        if self.x > 0 and self.x + self.width < width:
            self.x += self.xVel
        else:
            #Changing direction of velocity
            self.xVel *= -1
            self.x += self.xVel

        #top and bottom boundary
        if self.y > 0 and self.y + self.height < height:
            self.y += self.yVel
        else:
            self.yVel *= -1
            self.y += self.yVel

class textOnScreen(object):
    def __init__(self, text, pos, size, color):
        self.text = text
        self.pos = pos
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.size = size
        self.color = color
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.size)

    def draw(self, win, center = False):
        self.textsurface = self.myfont.render(self.text, True, self.color)
        if center:
            rect = self.textsurface.get_rect(center = (self.x, self.y))
            win.blit(self.textsurface, rect)
        else:
            win.blit(self.textsurface, (self.x, self.y))

def updateScreen():
    win.fill((255,255,255))

    rect1.drawRect(win)
    rect2.drawRect(win)

    rect1Speed.draw(win, center = True)
    rect2Speed.draw(win, center = True)

    pygame.display.update()

rect1 = Rectangles((100,100), 150, 85)
rect2 = Rectangles((100,300), 185, 90)
rect1Speed = textOnScreen('X Velocity -> ' + str(rect1.xVel) +'    Y Velocity -> ' + str(rect1.yVel), (width//2, 10), 20, rect1.color)
rect2Speed = textOnScreen('X Velocity -> ' + str(rect1.xVel) +'    Y Velocity -> ' + str(rect1.yVel), (width//2, 60), 20, rect2.color)

collitionTolerance = 10
run = True
while run:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

   
    if rect1.rect.colliderect(rect2) or rect2.rect.colliderect(rect1):
        #Checking for bottom - top collition
        if fabs(rect1.rect.bottom - rect2.rect.top) < collitionTolerance:
            #Head-On Collition
            if rect1.yVel * rect2.yVel < 0:
                print('Head On Collition')
                rect1.yVel *= -1
                rect2.yVel = fabs(rect2.yVel)
            else:
                print('Not head on collition')
                rect1.yVel = fabs(rect1.yVel + rect2.yVel//2) * -1 
                rect2.yVel = fabs(rect2.yVel - rect1.yVel//2)

        #Checking for top - bottom collition    
        elif fabs(rect1.rect.top - rect2.rect.bottom) < collitionTolerance:
            if rect1.yVel * rect2.yVel < 0:
                print('Head On Collition')
                rect1.yVel = fabs(rect1.yVel)
                rect2.yVel = fabs(rect2.yVel) * -1
            else:
                print('Not head on collition')
                rect1.yVel = fabs(rect1.yVel - rect2.yVel//2) * -1 
                rect2.yVel = fabs(rect2.yVel + rect1.yVel//2) 

        #Checking for left - right collition
        elif fabs(rect1.rect.left - rect2.rect.right) < collitionTolerance:
            if rect1.xVel * rect2.xVel < 0:
                print('Head On Collition')
                rect1.xVel = fabs(rect1.xVel)
                rect2.xVel = fabs(rect2.xVel) * -1
            else:
                print('Not head on collition')
                rect1.xVel = fabs(rect1.xVel + rect2.xVel//2)
                rect2.xVel = fabs(rect2.xVel - rect1.xVel//2) * -1

        #Checking for right - left collition
        elif fabs(rect1.rect.right - rect2.rect.left) < collitionTolerance:
            if rect1.xVel * rect2.xVel < 0:
                print('Head On Collition')
                rect1.xVel = fabs(rect1.xVel) * -1
                rect2.xVel = fabs(rect2.xVel) 
            else:
                print('Not head on collition')
                rect1.xVel = fabs(rect2.xVel - rect1.xVel//2) * -1
                rect2.xVel = fabs(rect2.xVel + rect1.xVel//2)

    rect1.move()
    rect2.move()

    rect1Speed.text = 'X Velocity -> ' + str(rect1.xVel) +'    Y Velocity -> ' + str(rect1.yVel)
    rect2Speed.text = 'X Velocity -> ' + str(rect2.xVel) +'    Y Velocity -> ' + str(rect2.yVel)


    updateScreen()

pygame.quit()