import pygame
from pygame import gfxdraw
from sys import exit
import numpy as np
from scipy import interpolate
import math

width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'curve_pattern.png'

background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pt = np.array([0, 0])
pt1 = np.array([0, 0])

pts = []
knots = []
count = 0
size = len(pts)
# screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock = pygame.time.Clock()


def drawPoint(pt, color='GREEN', thick=3):
    pygame.draw.circle(screen, GREEN, pt, thick)



# HW2 implement drawLine with drawPoint
def drawLine(pt0, pt1, color='GREEN', thick=3):
    m = len(pts)
    n = m-1
    pt0 = np.array(pt0, dtype='f')
    pt1 = np.array(pt1, dtype='f')
    line = np.arange(0.,1.0, 0.005)
    curve = np.arange(0, len(pts), 1)
    for t in line:
        interp = (1 - t) * pt0 + t * pt1
        drawPoint(interp, GREEN)

    for t in np.arange(0, len(pts) - 1, 0.001):
        px = [0.0,0.0]
        for i in curve:
            xn, xd = 1, 1
            for j in np.arange(0, len(pts), 1):
                if j != i:
                    xn = xn * (t - j)
                    xd = xd * (i - j)
            px = px + np.dot(pts[i], (xn)/ (xd))
        px = px.astype(int)
        drawPoint(px, color=RED, thick=1)



def drawPolylines(color='GREEN', thick=3):
    if (count < 2): return
    for i in range(count - 1):
        drawLine(pts[i], pts[i+1], GREEN)
        #pygame.draw.line(screen, color, pts[i], pts[i + 1], thick)


# Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0

while not done:
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
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

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
