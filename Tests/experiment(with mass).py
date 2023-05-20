import pygame
from random import randint, choice

pygame.init()
screenWidth, screenHeight = 800, 600
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Collitions for rectangles')

clock = pygame.time.Clock()

class textOnScreen(object):
    def __init__(self, xSpeed, ySpeed, mass, pos, size, color):
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.mass = mass
        self.pos = pos
        self.x = int(pos[0])
        self.y = int(pos[1])
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

class Rectangle(object):
    def __init__(self, pos, density):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.width = randint(70,  150)
        self.height = randint(20, 80)
        #Density = g/pixel
        self.density = density
        self.xVel = randint(-5,5)
        self.yVel = randint(-5, 5)
        self.mass = density * self.width * self.height
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.rect =  pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.rect =  pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        if self.x > 0 and self.x + self.width < screenWidth:
            self.x += self.xVel
        else:
            self.xVel *= -1
            self.x += self.xVel

        if self.y > 0 and self.y + self.height < screenHeight:
            self.y += self.yVel
        else:
            self.yVel *= -1
            self.y += self.yVel

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

    while obj1.rect.colliderect(obj2.rect):
        if not obj1.xVel and not obj1.yVel and not obj2.xVel and not obj2.yVel:
            break
        obj1.move()
        obj2.move()
        updateWin()

def  updateWin():
    win.fill((255,255,255))

    rect1.draw(win)
    rect2.draw(win)

    rect1DisplayVel.draw(win, center = True)
    rect2DisplayVel.draw(win, center = True)
    
    pygame.display.flip()

#Defining objects
#Density - Unit = g/pixel
rect1 = Rectangle((50,50), 1.8)
rect2 = Rectangle((320,120), 2)

rect1DisplayVel = textOnScreen(rect1.xVel, rect1.yVel, rect1.mass, (screenWidth//2, 10), 20, rect1.color)
rect2DisplayVel = textOnScreen(rect2.xVel, rect2.yVel, rect2.mass, (screenWidth//2, 60), 20, rect2.color)

run = True
fastForward = False
while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        clock.tick(240)
    else:
        clock.tick((60))

    #if all boxes have 0 velocity then program closes after 5 seconds
    if not rect1.xVel and not rect1.yVel and not rect2.xVel and not rect2.yVel:
        pygame.time.delay(5000)
        run = False

    rect1.move()
    rect2.move()

    rect1DisplayVel.speedUpdate(rect1.xVel, rect1.yVel)
    rect2DisplayVel.speedUpdate(rect2.xVel, rect2.yVel)

    if rect1.rect.colliderect(rect2.rect):
        collision(rect1, rect2)

    updateWin()

pygame.quit()