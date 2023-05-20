import pygame
from random import randint, choice, uniform
from math import sqrt, atan, degrees

pygame.init()
screenWidth, screenHeight = 1280, 720
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Collitions for spheres')

clock = pygame.time.Clock()

class displayVelocity(object):
    def __init__(self, xSpeed, ySpeed, mass, pos, size, color):
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.mass = mass
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.color = color
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.size)

    def draw(self, win, center = False):
        self.text = 'X Velocity -> ' + str(self.xSpeed) +'    Y Velocity -> ' + str(self.ySpeed) + '    Mass -> ' + "{:.2f}".format(self.mass/1000) + 'kg' 
        self.textsurface = self.myfont.render(self.text, True, self.color)
        if center:
            rect = self.textsurface.get_rect(center = (self.x, self.y))
            win.blit(self.textsurface, rect)
        else:
            win.blit(self.textsurface, (self.x, self.y))

    def speedUpdate(self, xSpeed, ySpeed):
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

class textOnScreen(object):

    def __init__(self, text, size, color, x, y):
        self.text = text
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.size)
        self.angle = 0

    def displayOnScreen(self, win, center = False, rotate = False):
        textsurface = self.myfont.render(self.text, True, self.color)
        if rotate:
            textsurface = pygame.transform.rotate(textsurface, self.angle)        
        if center:
            rect = textsurface.get_rect(center = (self.x, self.y))
            win.blit(textsurface,rect)
        else:
            win.blit(textsurface,(self.x, self.y))

class Circles(object):
    def __init__(self):
        self.x = randint(95, screenWidth - 95)
        self.y = randint(95, screenHeight - 95)
        self.radius = randint(45, 95)
        #Density = g/pixel
        self.density = uniform(0.01, 0.1)
        self.xVel = randint(-10, 10)
        self.yVel = randint(-10, 10)
        self.mass = self.density * 4/3 * 3.14 * (self.radius)**3
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        if self.x - self.radius > 0 and self.x + self.radius < screenWidth:
            self.x += self.xVel
        else:
            self.xVel *= -1
            self.x += self.xVel

        if self.y - self.radius > 0 and self.y + self.radius < screenHeight:
            self.y += self.yVel
        else:
            self.yVel *= -1
            self.y += self.yVel

def findAngle(obj1, obj2):
    y = obj2.y - obj1.y
    x = obj2.x - obj1.x

    if x != 0:
        return -1* degrees(atan(y/x))
    else:
        return 0

def findDistance(obj1, obj2):
    x1 = obj1.x
    x2 = obj2.x
    y1 = obj1.y
    y2 = obj2.y

    return sqrt((x1-x2)**2 + (y1-y2)**2)

def collision(obj1, obj2):
    m1 = obj1.mass/1000
    m2 = obj2.mass/1000
    u1x = obj1.xVel
    u2x = obj2.xVel
    u1y = obj1.yVel
    u2y = obj2.yVel

    obj1.xVel = int(((m1-m2)/(m1+m2))*u1x + (2*m2/(m1+m2))*u2x)
    obj2.xVel = int((2*m1/(m1+m2))*u1x + ((m2-m1)/(m1+m2))*u2x)

    obj1.yVel = int(((m1-m2)/(m1+m2))*u1y + (2*m2/(m1+m2))*u2y)
    obj2.yVel = int((2*m1/(m1+m2))*u1y + ((m2-m1)/(m1+m2))*u2y)

    while abs(findDistance(obj1, obj2) < (obj1.radius + obj2.radius)):
        if not obj1.xVel and not obj1.yVel and not obj2.xVel and not obj2.yVel:
            break
        obj1.move()
        obj2.move()
        updateWin()

def  updateWin():
    win.fill((255,255,255))

    #Displaying all circles
    for i in range(numObjects):
        objectsList[i].draw(win)

    #Displaying all velocity Displayers
    for i in range(numObjects):
        velocityDisplayList[i].draw(win, center = True)

    pygame.display.flip()

#Defining objects
#Density - Unit = g/pixel

numObjects = int(input('How many spheres?'))
objectsList = list()
for i in range(numObjects):
    objectsList.append(Circles())

print(objectsList)

velocityDisplayList = list()
for i in range(numObjects):
    velocityDisplayList.append(displayVelocity(objectsList[i].xVel, objectsList[i].yVel, objectsList[i].mass, (screenWidth//2, 10 + 50 *i), 20, objectsList[i].color))

print(velocityDisplayList)

run = True
fastForward = False
while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        clock.tick(240)
    elif keys[pygame.K_LEFT]:
        clock.tick(20)
    else:
        clock.tick((60))

    #Moving all circles
    for i in objectsList:
        i.move()

    #Displaying Velocities
    for i in range(numObjects):
        velocityDisplayList[i].speedUpdate(objectsList[i].xVel, objectsList[i].yVel)

    #Checking for collision between all circles
    for i in range(numObjects):
        for j in range(i + 1, numObjects):
            if abs(findDistance(objectsList[i], objectsList[j])) < objectsList[i].radius + objectsList[j].radius:
                collision(objectsList[i], objectsList[j])

    updateWin()

pygame.quit()