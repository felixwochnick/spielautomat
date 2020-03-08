import sys
import pygame
import random


def getColorName(colorNumber: int):
    """
    0 => black
    1 => white
    2 => yellow
    3 => green
    4 => blue
    5 => red
    """

    colorName = ''

    if colorNumber == 0:
        colorName = 'black'
    elif colorNumber == 1:
        colorName = 'white'
    elif colorNumber == 2:
        colorName = 'yellow'
    elif colorNumber == 3:
        colorName = 'green'
    elif colorNumber == 4:
        colorName = 'blue'
    elif colorNumber == 5:
        colorName = 'red'

    return colorName


def getColor(colorName: str):
    """
    black   =>  (0, 0, 0)
    white   =>  (255, 255, 255)
    yellow  =>  (252, 248, 0)
    green   =>  (21, 255, 0)
    blue    =>  (0, 157, 255)
    red     =>  (255, 0, 47)
    """

    color = ()

    if colorName == 'black':
        color = (0, 0, 0)
    elif colorName == 'white':
        color = (255, 255, 255)
    elif colorName == 'yellow':
        color = (252, 248, 0)
    elif colorName == 'green':
        color = (21, 255, 0)
    elif colorName == 'blue':
        color = (0, 157, 255)
    elif colorName == 'red':
        color = (255, 0, 47)

    return color


class Window:
    def __init__(self, monney=30, windowSize=[800, 600]):
        pygame.init()
        self.__windowSize = windowSize
        self.__screen = pygame.display.set_mode(self.__windowSize)
        self.__font = pygame.font.SysFont(None, 30)

        # standard text
        self.__EMPTYWIN  = '                                                    '
        self.__NOWIN     = 'Kein Gewinn:       +0€      '
        self.__LWIN      = 'Kleiner Gewinn:    +2€      '
        self.__BWIN      = 'Großer Gewinn:     +4€      '
        self.__NOMONNEY  = 'Du hast kein Geld mehr!     '

        self.__SUM       = monney
        self.__SUM_RESET = monney
        self.__TEXT_SUM  = f'Gesamter Gewinn:    {self.__SUM}€     '

        self.__build()

    def __build(self):
        self.automat = Automat(self.__screen)
        self.text = TextField(self.__screen, self.__font, 10, 15, self.__EMPTYWIN)
        self.textSUM = TextField(self.__screen, self.__font, 10, 55, self.__TEXT_SUM)
        self.btn = Button(self.__screen, self.__font, 400, 10, text="Spielen")
        self.btnReset = Button(self.__screen, self.__font, 400, 50, text="Reset")

    def reset(self):
        self.__SUM = self.__SUM_RESET
        self.text.update(self.__EMPTYWIN)
        self.textSUM.update(f'Gesamter Gewinn:    {self.__SUM}€     ')

    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePosX, mousePosY = pygame.mouse.get_pos()
                    # Mouse on btn
                    if (
                        mousePosX > self.btn.getPosition()[0] and mousePosX < (self.btn.getPosition()[0] + self.btn.getPosition()[2])
                    ) and (
                        mousePosY > self.btn.getPosition()[1] and mousePosY < (self.btn.getPosition()[1] + self.btn.getPosition()[3])
                    ):
                        if self.__SUM >= 2:
                            self.__SUM -= 2
                            win = self.automat.play()
                            if win == 0:
                                self.text.update(self.__NOWIN)
                            elif win == 1:
                                self.text.update(self.__LWIN)
                                self.__SUM += 2
                            elif win == 2:
                                self.text.update(self.__BWIN)
                                self.__SUM += 4
                            self.textSUM.update(f'Gesamter Gewinn:    {self.__SUM}€     ')
                        else:
                            self.text.update(self.__NOMONNEY)

                    # Mouse on btnReset
                    if (
                        mousePosX > self.btnReset.getPosition()[0] and mousePosX < (self.btnReset.getPosition()[0] + self.btnReset.getPosition()[2])
                    ) and (
                        mousePosY > self.btnReset.getPosition()[1] and mousePosY < (self.btnReset.getPosition()[1] + self.btnReset.getPosition()[3])
                    ):
                        self.reset()


class Border:
    def __init__(self, screen, x=100, y=100, size=100, color=(255, 255, 255)):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__color = color
        self.__screen = screen
        self.show()

    def changeColor(self, color=(255, 255, 255)):
        self.__color = color

    def show(self):
        pygame.draw.rect(self.__screen, self.__color, (self.__x, self.__y, self.__size, self.__size), 1)
        pygame.display.flip()


class Point:
    def __init__(self, screen, x=100, y=100, rad=25, color=(255, 255, 255)):
        self.__x = x
        self.__y = y
        self.__rad = rad
        self.__color = color
        self.__screen = screen
        self.show()

    def changeColor(self, color=(255, 255, 255)):
        self.__color = color

    def show(self):
        pygame.draw.circle(self.__screen, self.__color, (self.__x, self.__y), self.__rad, 0)
        pygame.display.flip()


class AutomatPart:
    def __init__(self, screen, x=100, y=100, size=100, color=[(255, 255, 255), (255, 255, 255)]):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__color = color
        self.__screen = screen

        self.__border = Border(self.__screen, self.__x, self.__y, self.__size, self.__color[0])
        self.__point = Point(self.__screen, int(self.__x + (self.__size / 2)), int(self.__y + (self.__size / 2)), int(self.__size / 4), self.__color[1])

    def show(self):
        self.__border.show()
        self.__point.show()

    def changeColorPoint(self, color=(255, 255, 255)):
        self.__point.changeColor(color)
        self.__point.show()


class Automat:
    def __init__(self, screen, x=100, y=100, size=100, number=3, color=[[(255, 255, 255), (255, 255, 255)], [(255, 255, 255), (255, 255, 255)], [(255, 255, 255), (255, 255, 255)]]):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__color = color
        self.__screen = screen
        self.__number = number
        self.__automatParts = []

        x = 0
        while x < self.__number:
            self.__automatParts.append(AutomatPart(self.__screen, self.__x + self.__size * x, self.__y, self.__size, self.__color[x]))
            x += 1

    def show(self):
        for automatPart in self.__automatParts:
            automatPart.show()

    def changeColorPoint(self, position, color=(255, 255, 255)):
        self.__automatParts[position].changeColorPoint(color)

    def changeColorPoints(self, color=[(255, 255, 255), (255, 255, 255), (255, 255, 255)]):
        x = 0
        for automatPart in self.__automatParts:
            automatPart.changeColorPoint(color[x])
            x += 1

    def play(self):
        colorNumbers = [random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)]
        color = []

        for colorNumber in colorNumbers:
            color.append(getColor(getColorName(colorNumber)))

        self.changeColorPoints(color=color)

        if colorNumbers[0] == colorNumbers[1] or colorNumbers[0] == colorNumbers[2] or colorNumbers[2] == colorNumbers[1]:
            x = 1
        else:
            x = 0
        if colorNumbers[0] == colorNumbers[1] and colorNumbers[0] == colorNumbers[2]:
            x = 2

        return x


class TextField:
    def __init__(self, screen, font, x=100, y=100, text='', color=(255, 255, 255)):
        self.__screen = screen
        self.__x = x
        self.__y = y
        self.__font = font
        self.__text = text
        self.__color = color

        self.show()

    def show(self):
        self.__surface = self.__font.render(self.__text, True, self.__color, (0, 0, 0))

        self.__screen.blit(self.__surface, (self.__x, self.__y))
        pygame.display.flip()

    def update(self, text, color=(255, 255, 255)):
        self.__text = text
        self.__color = color
        self.__surface = self.__font.render(self.__text, True, self.__color, (0, 0, 0))
        self.__screen.blit(self.__surface, (self.__x, self.__y))
        pygame.display.flip()


class Button:
    def __init__(self, screen, font, x=100, y=100, size=[100, 30], text="", color=[(255, 255, 255), (0, 180, 255)]):
        self.__screen = screen
        self.__x = x
        self.__y = y
        self.__size = size
        self.__font = font
        self.__text = text
        self.__color = color

        self.show()

    def show(self):
        self.__btn = pygame.draw.rect(self.__screen, self.__color[1], (self.__x, self.__y, self.__size[0], self.__size[1]), 0)

        self.__surface = self.__font.render(self.__text, True, self.__color[0])
        self.__textrect = self.__surface.get_rect()
        self.__textrect.center = (self.__x + self.__size[0] / 2, self.__y + self.__size[1] / 2)

        self.__screen.blit(self.__surface, self.__textrect)
        pygame.display.flip()

    def getPosition(self):
        return [self.__x, self.__y, self.__size[0], self.__size[1]]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(type(int(sys.argv[1])))
        window = Window(monney=int(sys.argv[1]), windowSize=[510, 300])
    else:
        window = Window(windowSize=[510, 300])
    window.mainLoop()
