import pygame
from random import randint, choice
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
    def __init__(self, pos, density):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.radius = randint(45, 95)
        #Density = g/pixel
        self.density = density
        self.xVel = randint(-5, 5)
        self.yVel = randint(-5, 5)
        self.mass = density * 4/3 * 3.14 * (self.radius)**3
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

    while abs(findDistance(circle1, circle2) < (circle1.radius + circle2.radius)):
        if not obj1.xVel and not obj1.yVel and not obj2.xVel and not obj2.yVel:
            break
        obj1.move()
        obj2.move()
        updateWin()

def  updateWin():
    win.fill((255,255,255))

    circle1.draw(win)
    circle2.draw(win)

    rect1DisplayVel.draw(win, center = True)
    rect2DisplayVel.draw(win, center = True)
    
    if keys[pygame.K_q]:
        pygame.draw.line(win, (0,0,0), (circle1.x, circle1.y), (circle2.x, circle2.y), 3)
        displayDistance.displayOnScreen(win, center = True, rotate = True)

    pygame.display.flip()

#Defining objects
#Density - Unit = g/pixel
circle1 = Circles((150,150), 0.04)
circle2 = Circles((650,450), 0.01)

rect1DisplayVel = displayVelocity(circle1.xVel, circle1.yVel, circle1.mass, (screenWidth//2, 10), 20, circle1.color)
rect2DisplayVel = displayVelocity(circle2.xVel, circle2.yVel, circle2.mass, (screenWidth//2, 60), 20, circle2.color)

displayDistance = textOnScreen('Distance : ' + "{:.2f}".format(findDistance(circle1, circle2)), 20, (0,0,0), (circle1.x + circle2.x)/2, (circle1.y + circle2.y)/2 - 20)

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

    circle1.move()
    circle2.move()

    rect1DisplayVel.speedUpdate(circle1.xVel, circle1.yVel)
    rect2DisplayVel.speedUpdate(circle2.xVel, circle2.yVel)

    if abs(findDistance(circle1, circle2) < (circle1.radius + circle2.radius)):
        collision(circle1, circle2)

    #if all boxes have 0 velocity then program closes after 5 seconds
    if not circle1.xVel and not circle1.yVel and not circle2.xVel and not circle2.yVel:
        pygame.time.delay(5000)
        break

    displayDistance.text = 'Distance : ' + "{:.2f}".format(findDistance(circle1, circle2))
    displayDistance.x = (circle1.x + circle2.x)/2
    displayDistance.y = (circle1.y + circle2.y)/2 - 20
    displayDistance.angle = findAngle(circle1, circle2)

    updateWin()

pygame.quit()