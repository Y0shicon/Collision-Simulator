import pygame
import pygame.gfxdraw

pygame.init()

win = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Pause Button')


class Pause:

    def __init__(self, pos, win):
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.radius = 50
        self.win = win

    def draw(self):
        pygame.draw.circle(self.win, (0, 0, 0),
                           center=self.pos, radius=self.radius, width=5)
        pygame.draw.line(self.win, (0, 0, 0), (self.x - self.radius/3, self.y - self.radius//1.5 ), (self.x - self.radius/3, self.y + self.radius//1.5 ),
                         width=3)
        pygame.draw.line(self.win, (0, 0, 0), (self.x + self.radius/3, self.y - self.radius//1.5 ), (self.x + self.radius/3, self.y + self.radius//1.5 ),
                         width=3)

if __name__ == '__main__':

    pauseButton = Pause((200, 200), win)

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        win.fill((255, 255, 255))
        #pygame.gfxdraw.aacircle(win, 100, 100, 15, (0,0,0))
        pauseButton.draw()
        pygame.display.flip()


    pygame.quit()
