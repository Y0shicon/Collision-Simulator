import pygame
import math
from random import randint
from pygame_widgets import *


class Spheres(object):

    def __init__(self, pos, win):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = 45
        #Density = g/pixel
        self.density = 0.01
        self.xVel = randint(-10, 10)
        self.yVel = randint(-10, 10)
        self.mass = self.density * 4/3 * math.pi * (self.radius)**3
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.rectHitbox = pygame.Rect(
            self.x - self.radius - 5, self.y - self.radius - 5, 2*(self.radius + 5), 2*(self.radius+5))
        self.showInfo = False

        self.angle = math.degrees(
            math.atan(abs(self.yVel / self.xVel))) if self.xVel != 0 else 0

        '--------------------------------> The Sliders <---------------------------------------'

        # X Velocity
        self.xVelSlider = Slider(
            win, 75, 70, 150, 20, min=-15, max=15, step=0.1)
        self.xVelTextBox = TextBox(win, 130, 100, 40, 30)
        self.xVelText = textOnScreen('X Velocity', 22, (0, 0, 0), 150, 35)
        self.xVelTextBox.setText("{:.2f}".format(self.xVel))
        self.xVelSlider.setValue(self.xVel)

        # Y Velocity
        self.yVelSlider = Slider(
            win, 320, 70, 150, 20, min=-15, max=15, step=0.1)
        self.yVelTextBox = TextBox(win, 370, 100, 40, 30)
        self.yVelText = textOnScreen('Y Velocity', 22, (0, 0, 0), 450, 35)
        self.yVelTextBox.setText("{:.2f}".format(self.yVel))
        self.yVelSlider.setValue(self.yVel)

        # Radius
        self.radiusSlider = Slider(
            win, 575, 70, 175, 20, min=5, max=95, step=1)
        self.radiusTextBox = TextBox(win, 640, 100, 40, 30)
        self.radiusText = textOnScreen('Radius', 22, (0, 0, 0), 650, 35)
        self.radiusTextBox.setText("{:.2f}".format(self.radius))
        self.radiusSlider.setValue(self.radius)

        # Density
        self.densitySlider = Slider(
            win, 840, 70, 250, 20, min=0.001, max=1.5, step=0.005)
        self.densityTextBox = TextBox(win, 950, 100, 60, 30)
        self.densityText = textOnScreen(
            'Density (g/pixel)', 22, (0, 0, 0), 950, 35)
        self.densityTextBox.setText("{:.3f}".format(self.density))
        self.densitySlider.setValue(self.density)

        # Mass
        self.massTextBox = TextBox(win, 765, 126, 60, 30)
        self.massText = textOnScreen('Mass - ', 19, (0, 0, 0), 730, 140)
        self.massUnitText = textOnScreen('kg', 15, (0, 0, 0), 835, 140)
        self.massTextBox.setText("{:.3f}".format(self.mass/1000))

        '-------------------------------> The Arrows <-------------------------------------'

        # X Direction Arrow
        self.arrowlen = 150  # in pixels
        self.xConstant = self.arrowlen // abs(
            self.xVel) if self.xVel != 0 else 0
        self.yConstant = self.arrowlen // abs(
            self.yVel) if self.yVel != 0 else 0

    def draw(self, win):
        self.rectHitbox = pygame.Rect(
            self.x - self.radius - 5, self.y - self.radius - 5, 2*(self.radius + 5), 2*(self.radius+5))
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self, rect, neg=1):

        # Setting Up boundaries

        left = rect.left
        right = rect.right
        top = rect.top
        bottom = rect.bottom

        '''print(
            'Left : ' , left,
            ';Right : ', right,
            ';X : ', self.x,
            ';X Vel :', self.xVel,
            ';Top : ', top,
            ';Bottom : ', bottom,
            ';Y : ', self.y,
            ';Y Vel :', self.yVel
            )'''

        if self.x - self.radius >= left and self.x + self.radius <= right:
            self.x += self.xVel * neg
        elif self.x - self.radius < left:
            self.xVel = abs(self.xVel) * neg
            self.x = left + self.radius
        elif self.x + self.radius > right:
            self.xVel = abs(self.xVel) * -1 * neg
            self.x = right - self.radius

        if self.y - self.radius >= top and self.y + self.radius <= bottom:
            self.y += self.yVel * neg
        elif self.y - self.radius < top:
            self.yVel = abs(self.yVel) * neg
            self.y = top + self.radius
        elif self.y + self.radius > bottom:
            self.yVel = abs(self.yVel) * -1 * neg
            self.y = bottom - self.radius

        # Updating angle
        self.angle = math.degrees(
            math.atan(abs(self.yVel / self.xVel))) if self.xVel != 0 else 0

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

        self.densityText.draw(win, center=True)
        self.massUnitText.draw(win, center=True)
        self.massText.draw(win, center=True)
        self.radiusText.draw(win, center=True)
        self.xVelText.draw(win, center=True)
        self.yVelText.draw(win, center=True)

        # Miscellaneous - The hitbox for focus on the sphere chosen
        pygame.draw.rect(win, (255, 0, 0), self.rectHitbox, 2)

        '-----------------------> Showing the arrows <-------------------'
        self.xConstant = self.arrowlen // abs(
            self.xVel) if self.xVel != 0 else 0
        self.yConstant = self.arrowlen // abs(
            self.yVel) if self.yVel != 0 else 0
        self.xEnd = self.x + self.xConstant * self.xVel
        self.yEnd = self.y + self.yConstant * self.yVel
        # If both x vel and y vel are 0, then constant = 0
        try:
            self.slantConstant = self.arrowlen / \
                math.sqrt(self.xVel ** 2 + self.yVel ** 2)
        except ZeroDivisionError:
            self.slantConstant = 0
        self.xEndSlant = self.x + self.slantConstant * self.xVel
        self.yEndSlant = self.y + self.slantConstant * self.yVel

        self.xArrow = Arrow((self.x, self.y), (self.xEnd,
                                               self.y), (255, 0, 0), (255, 0, 100), 10)
        self.yArrow = Arrow(
            (self.x, self.y), (self.x, self.yEnd), (0, 255, 0), (0, 255, 100), 10)
        self.projectionArrow = Arrow(
            (self.x, self.y), (self.xEndSlant, self.yEndSlant), (0, 0, 255), (100, 0, 255), 10)

        self.xArrow.draw(win)
        self.yArrow.draw(win)
        self.projectionArrow.draw(win)

        '----------------------> Updating the slider and textbox values <------------'

        self.xVel = self.xVelSlider.getValue()
        self.yVel = self.yVelSlider.getValue()
        self.radius = self.radiusSlider.getValue()
        self.rectHitbox = pygame.Rect(
            self.x - self.radius - 5, self.y - self.radius - 5, 2*(self.radius + 5), 2*(self.radius+5))
        self.density = self.densitySlider.getValue()
        self.mass = self.density * 4/3 * math.pi * (self.radius)**3

        self.xVelTextBox.setText("{:.2f}".format(self.xVelSlider.getValue()))
        self.yVelTextBox.setText("{:.2f}".format(self.yVelSlider.getValue()))
        self.radiusTextBox.setText(self.radiusSlider.getValue())
        self.densityTextBox.setText(
            "{:.3f}".format(self.densitySlider.getValue()))
        self.massTextBox.setText("{:.3f}".format(self.mass/1000))

    def showProjectileArrow(self, win):
        try:
            self.slantConstant = self.arrowlen / \
                math.sqrt(self.xVel ** 2 + self.yVel ** 2)
        except ZeroDivisionError:
            self.slantConstant = 0
        self.xEndSlant = self.x + self.slantConstant * self.xVel
        self.yEndSlant = self.y + self.slantConstant * self.yVel
        self.projectionArrow = Arrow(
            (self.x, self.y), (self.xEndSlant, self.yEndSlant), (0, 0, 255), (100, 0, 255), 10)
        self.projectionArrow.draw(win)


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
        self.text = 'X Velocity -> ' + "{:.2f}".format(self.xSpeed) + '    Y Velocity -> ' + "{:.2f}".format(
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


class mDisplayInfoInSim(object):

    def __init__(self, sphereList, win, infoRect='Hi'):
        self.sphereList = sphereList
        self.velocityList = []
        for sphere in self.sphereList:
            self.velocityList.append([sphere.xVel, sphere.yVel])
        self.nSphere = len(sphereList)
        self.infoRect = infoRect
        self.win = win
        self.x = 30
        self.y = 60
        # For every 2 new spheres, the size the text will reduce by 3
        self.size = 18
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.size)

    def draw(self):
        for i in range(self.nSphere):
            self.text = 'X Velocity -> ' + "{:.2f}".format(self.velocityList[i][0]) + '    Y Velocity -> ' + "{:.2f}".format(
                self.velocityList[i][1]) + '    Mass -> ' + "{:.2f}".format(self.sphereList[i].mass/1000) + 'kg'
            self.color = self.sphereList[i].color
            self.textsurface = self.myfont.render(self.text, True, self.color)
            # Every time i is odd, x position is added by 70 and everytime i is even, y position is added by 30
            if i % 2 == 0:
                self.win.blit(self.textsurface, (self.x, self.y + (i//2)*30))
            else:
                self.win.blit(self.textsurface,
                              (self.x + 520, self.y + (i//2)*30))

    def speedUpdate(self):
        self.velocityList = []
        for sphere in self.sphereList:
            self.velocityList.append([sphere.xVel, sphere.yVel])


class textOnScreen(object):

    def __init__(self, text, size, color, x, y, **kwargs):
        self.text = text
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.font = kwargs.get('font', 'Comic Sans MS')
        self.myfont = pygame.font.SysFont(self.font, self.size)
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


class clickableImage:
    def __init__(self, path, surface, pos, res, **kwargs):
        self.path = path
        self.res = res
        self.img = pygame.image.load(self.path)
        self.img = pygame.transform.scale(self.img, (self.res))
        self.surface = surface
        self.img.convert(self.surface)
        self.pos = pos
        # ?Defining collision boxes
        self.rect = self.img.get_rect()
        self.rect.center = self.pos[0], self.pos[1]
        # ?Defining an on click img
        self.onClickImgPath = kwargs.get('onClickImgPath', False)
        if self.onClickImgPath:
            self.onClickImg = pygame.image.load(self.onClickImgPath)
            self.onClickImg = pygame.transform.scale(
                self.onClickImg, (round(self.res[0]/1.1), round(self.res[1]/1.1)))
            self.onClickImg.convert(self.surface)
        # ?Should only be true when the image is clicked
        self.isClicked = False

    def draw(self):
        if self.isClicked and self.onClickImgPath:
            self.surface.blit(self.onClickImg, self.rect)
        else:
            self.surface.blit(self.img, self.rect)

    def clicked(self):
        self.isClicked = not self.isClicked
