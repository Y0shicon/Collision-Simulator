import pygame
import math
from random import randint
from pygame_widgets import *

class Spheres(object):

    def __init__(self, pos, win):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = 30
        #Density = g/pixel
        self.density = 0.01
        self.xVel = randint(-10, 10)
        self.yVel = randint(-10, 10)
        self.mass = self.density * 4/3 * math.pi * (self.radius)**3
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.rectHitbox = pygame.Rect(
            self.x - self.radius, self.y - self.radius, 2*self.radius, 2*self.radius)
        self.showInfo = False

        '--------------------------------> The Sliders <---------------------------------------'
        
        #X Velocity
        self.xVelSlider = Slider(win, 75, 630, 150, 20, min = -10, max = 10, step = 1)
        self.xVelTextBox = TextBox(win, 140, 660, 40, 30)
        self.xVelText = textOnScreen('X Velocity', 22, (0,0,0), 120, 600)
        self.xVelTextBox.setText(self.xVel)
        self.xVelSlider.setValue(self.xVel)

        #Y Velocity
        self.yVelSlider = Slider(win, 320, 630, 150, 20, min = -10, max = 10, step = 1)
        self.yVelTextBox = TextBox(win, 350, 660, 40, 30)
        self.yVelText = textOnScreen('Y Velocity', 22, (0,0,0), 400, 600)
        self.yVelTextBox.setText(self.yVel)
        self.yVelSlider.setValue(self.yVel)

        #Radius
        self.radiusSlider = Slider(win, 575, 630, 200, 20, min = 5, max = 95, step = 1)
        self.radiusTextBox = TextBox(win, 640, 660, 40, 30)
        self.radiusText = textOnScreen('Radius', 22, (0,0,0), 650, 600)
        self.radiusTextBox.setText(self.radius)
        self.radiusSlider.setValue(self.radius)

        #Mass and Density
        self.densitySlider = Slider(win, 850, 630, 300, 20, min = 0.001, max = 2, step = 0.005)
        self.densityTextBox = TextBox(win, 1170, 620, 60, 30)
        self.densityText = textOnScreen('Density (g/pixel)', 22, (0,0,0), 1000, 600)
        self.massTextBox = TextBox(win, 1170, 660, 60, 30)
        self.massText = textOnScreen('Mass - ', 19, (0,0,0), 1100, 680)
        self.massUnitText = textOnScreen('kg', 15, (0,0,0), 1240, 680)
        self.massTextBox.setText("{:.3f}".format(self.mass/1000))
        self.densityTextBox.setText(self.density)
        self.densitySlider.setValue(self.density)

        '-------------------------------> The Arrows <-------------------------------------'

        #X Direction Arrow
        self.arrowlen = 150#in pixels
        self.xConstant = self.arrowlen // abs(self.xVel) if self.xVel != 0 else 0
        self.yConstant = self.arrowlen // abs(self.yVel) if self.yVel != 0 else 0

    def draw(self, win):
        self.rectHitbox = pygame.Rect(
            self.x - self.radius, self.y - self.radius, 2*self.radius, 2*self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self, screenWidth, screenHeight):
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

    def showData(self, win):

        '--------------------->Displaying all infoboxes<----------------------'
        self.xVelSlider.draw()
        self.yVelSlider.draw()
        self.xVelTextBox.draw()
        self.yVelTextBox.draw()

        self.radiusSlider.draw()
        self.radiusTextBox.draw()
        
        self.densitySlider.draw()
        self.densityTextBox.draw()

        self.massTextBox.draw()

        self.densityText.draw(win, center = True)
        self.massUnitText.draw(win, center = True)
        self.massText.draw(win, center = True)
        self.radiusText.draw(win, center = True)
        self.xVelText.draw(win, center = True)
        self.yVelText.draw(win, center = True)

        #Miscellaneous - The hitbox for focus on the sphere chosen
        pygame.draw.rect(win, (255, 0, 0), self.rectHitbox, 2)

        '-----------------------> Showing the arrows <-------------------'
        self.xConstant = self.arrowlen // abs(self.xVel) if self.xVel != 0 else 0
        self.yConstant = self.arrowlen // abs(self.yVel) if self.yVel != 0 else 0
        self.xEnd = self.x + self.xConstant * self.xVel
        self.yEnd = self.y + self.yConstant * self.yVel
        #If both x vel and y vel are 0, then constant = 0
        try:
            self.slantConstant = self.arrowlen/math.sqrt(self.xVel ** 2 + self.yVel ** 2)
        except ZeroDivisionError:
            self.slantConstant = 0
        self.xEndSlant = self.x + self.slantConstant * self.xVel
        self.yEndSlant = self.y + self.slantConstant * self.yVel

        self.xArrow = Arrow((self.x, self.y), (self.xEnd, self.y), (255,0,0), (255,0,100), 10)
        self.yArrow = Arrow((self.x, self.y), (self.x, self.yEnd), (0,255,0), (0,255,100), 10)
        self.projectionArrow = Arrow((self.x, self.y), (self.xEndSlant, self.yEndSlant), (0,0,255), (100,0,255), 10)

        self.xArrow.draw(win)
        self.yArrow.draw(win)
        self.projectionArrow.draw(win)

        '----------------------> Updating the slider and textbox values <------------'

        self.xVel = self.xVelSlider.getValue()
        self.yVel = self.yVelSlider.getValue()
        self.radius = self.radiusSlider.getValue()
        self.density = self.densitySlider.getValue()
        self.mass = self.density * 4/3 * math.pi * (self.radius)**3


        self.xVelTextBox.setText(self.xVelSlider.getValue())
        self.yVelTextBox.setText(self.yVelSlider.getValue())
        self.radiusTextBox.setText(self.radiusSlider.getValue())
        self.densityTextBox.setText("{:.3f}".format(self.densitySlider.getValue()))
        self.massTextBox.setText("{:.3f}".format(self.mass/1000))


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

    def draw(self, win, center=False):
        self.text = 'X Velocity -> ' + str(self.xSpeed) + '    Y Velocity -> ' + str(
            self.ySpeed) + '    Mass -> ' + "{:.2f}".format(self.mass/1000) + 'kg'
        self.textsurface = self.myfont.render(self.text, True, self.color)
        if center:
            rect = self.textsurface.get_rect(center=(self.x, self.y))
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

    def draw(self, win, center=False, rotate=False):
        textsurface = self.myfont.render(self.text, True, self.color)
        if rotate:
            textsurface = pygame.transform.rotate(textsurface, self.angle)
        if center:
            rect = textsurface.get_rect(center=(self.x, self.y))
            win.blit(textsurface, rect)
        else:
            win.blit(textsurface, (self.x, self.y))


class mTextBox(object):
    def __init__(self, text, pos, color):
        self.text = text
        self.num = 0
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.color = color
        self.width = 80
        self.height = 40
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.activateTyping = False
        self.size = 30

    def draw(self, window):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(window, self.color, self.rect, 2)
        self.input = textOnScreen(
            self.text, self.size, (255, 150, 100), self.x, self.y)
        self.input.draw(window, center=True)


class Arrow(object):

    def __init__(self, start, end, lineColor, triangleColor, triangleRadius):
        self.start = start
        self.end = end
        self.lineColor = lineColor
        self.triangleColor = triangleColor
        self.triangleRadius = triangleRadius

    def draw(self, screen):
        pygame.draw.line(screen, self.lineColor, self.start, self.end, 4)
        rotation = math.degrees(math.atan2(
            self.start[1]-self.end[1], self.end[0]-self.start[0]))+90
        pygame.draw.polygon(screen, self.triangleColor, ((self.end[0]+self.triangleRadius*math.sin(math.radians(rotation)), self.end[1]+self.triangleRadius*math.cos(math.radians(rotation))), (self.end[0]+self.triangleRadius*math.sin(math.radians(
            rotation-120)), self.end[1]+self.triangleRadius*math.cos(math.radians(rotation-120))), (self.end[0]+self.triangleRadius*math.sin(math.radians(rotation+120)), self.end[1]+self.triangleRadius*math.cos(math.radians(rotation+120)))))
