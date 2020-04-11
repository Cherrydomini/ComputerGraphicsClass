"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
barycentric reference http://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html
http://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html
https://docs.scipy.org/doc/numpy/reference/generated/numpy.concatenate.html
https://www.programiz.com/python-programming/examples/multiply-matrix
"""
import matplotlib.pyplot as plt
import pygame
from pygame import gfxdraw
from sys import exit
import numpy as np
import scipy

width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'curve_pattern.png'

background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Barycentric Coordinates")

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pt = np.array([0, 0])
pt1 = np.array([0, 0])

barycoord = []


pts = []
knots = []
count = 0
size = len(pts)
# screen.blit(background, (0,0))
screen.fill(WHITE)



# Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0

# https://kite.com/python/docs/pygame.Surface.blit
clock = pygame.time.Clock()


def drawPoint(pt, color='GREEN', thick=3):
    pygame.draw.circle(screen, GREEN, pt, thick)


# HW2 implement drawLine with drawPoint
def drawLine(pt0, pt1, color='GREEN', thick=3):
    pt0 = np.array(pt0, dtype='f')
    pt1 = np.array(pt1, dtype='f')
    line = np.arange(0.,1.0, 0.005)
    for t in line:
        interp = (1 - t) * pt0 + t * pt1
        drawPoint(interp, GREEN)


def drawPolylines(color='GREEN', thick=3):
    if (count < 2): return
    for i in range(count - 1):
        drawLine(pts[i], pts[i+1], GREEN)
        if count == 3:
            drawLine(pts[0], pts[i-1], GREEN)

font = pygame.font.SysFont("consolas", 20)

def printText(msg, color='BLACK', pos=(50, 50)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

def pointInTriangle():
    flag = None
    pygame.draw.rect(screen, WHITE, (50, 50, 400, 100))
    x1, y1 = barycoord[0]
    x2, y2 = barycoord[1]
    x3, y3 = barycoord[2]
    xp = x
    yp = y

    c1 = (x2 - x1) * (yp - y1) - (y2 - y1) * (xp - x1)
    c2 = (x3 - x2) * (yp - y2) - (y3 - y2) * (xp - x2)
    c3 = (x1 - x3) * (yp - y3) - (y1 - y3) * (xp - x3)
    if (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0):
        flag = True
        printText("You're in the Triangle!")
    else:
       flag = False
       printText("You're NOT the Triangle!")

while not done:
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
            x1, y1 = pt
            barycoord.append([x,y])
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = np.array([x, y])
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        pts.append(pt)
        print(pt)
        count += 1
        pygame.draw.rect(screen, BLUE, (pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin), 5)
        print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) + " button:" + repr(
            button1) + " pressed:" + repr(pressed) + " add pts ...")
    else:
        print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) + " button:" + repr(
            button1) + " pressed:" + repr(pressed))


    if len(pts) > 1:
        drawPolylines('GREEN', 1)
        # drawLagrangePolylines(BLUE, 10, 3)
    if len(pts) == 3:
        pointInTriangle()


    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
