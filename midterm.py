import pygame
from pygame import gfxdraw
from sys import exit
import numpy as np
from scipy import interpolate
import math
from datetime import datetime



width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)



background_image_filename = 'curve_pattern.png'



background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
pygame.display.set_caption("ImagePolylineMouseButton")



# Define the colors we will use in RGB format

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (210, 100, 200)
PINK = (255, 182, 180)



pt = np.array([0, 0])



# get the key pressed to command the program
keypressed = pygame.key.get_pressed()



pts = []
knots = []
count = 0
size = len(pts)

# screen.blit(background, (0,0))

screen.fill(WHITE)



# https://kite.com/python/docs/pygame.Surface.blit

clock = pygame.time.Clock()





def drawPoint(pt, color='GREEN', thick=3, ):
    pygame.draw.circle(screen, color, pt, thick)


def controlPoint(pt, color):
        pygame.draw.rect(screen, color, (pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin), 5)


font = pygame.font.SysFont("consolas", 20)





# HW2 implement drawLine with drawPoint

def drawLine(pt0, pt1, color='GREEN', thick=3):
    m = len(pts)
    n = m - 1
    pt0 = np.array(pt0, dtype='f')
    pt1 = np.array(pt1, dtype='f')
    line = np.arange(0., 1.0, 0.005)
    for t in line:
        interp = (1 - t) * pt0 + t * pt1
        drawPoint(interp, GREEN)




#equations for all curves in the program grouped together for eazier viewing
# equation for the lagrange curve
def lagrange(pt0, pt1, color, thick=1):
    curve = np.arange(0, len(pts), 1)
    for t in np.arange(0, len(pts) - 1, 0.001):
        px = [0.0, 0.0]
        for i in curve:
            xn, xd = 1, 1
            for j in np.arange(0, len(pts), 1):
                if j != i:
                    xn = xn * (t - j)
                    xd = xd * (i - j)
            px = px + np.dot(pts[i], (xn) / (xd))
        px = px.astype(int)
        drawPoint(px, color, thick=1)

#make hermite piecwise curve
def hermite(pt0, pt1, color, thick=1):
    curve = np.arange(0, len(pts), 1)
    for i in np.arange(0, len(pts)-1, 1):
        h = [0.0, 0.0]
        s = i/len(pts)
        for t in np.arange(0, len(pts), 1):
            h1 = 2*s**3 - 3*s**2 +1
            h2 = -2 * s ** 3 + 3 * s ** 2
            h3 = s ** 3 - 2 * s ** 2 + s
            h4 = s ** 3 - s ** 2
            for j in np.arange(0, len(pts), 1):
                if j != i:
                    her = h1*pts[j] + h2*pts[j] + h3 *(.5*pts[j] - pts[j-1]) + h4 * (.5*pts[j]-pts[j-2])
        her = her + np.dot(her, pts[i])
        her = her.astype(int)
        drawPoint(her, RED, 3)

#make bezier curve
def bezier(pt0, pt1, color, thick=5):
    for i in np.arange(0, 1, .001):
        bez = np.zeros(2, dtype=np.float32)

        for j in np.arange(0, len(pts), 1):
            if len(pts) > 3:
                bez = bez + np.dot(((len(pts) - 1)**j, j) * ((1 - i) ** (len(pts) - 1 - j)) * (i ** j), pts[j])
            if j < len(pts)-1:
                bez_sl = np.dot((1-i),pts[j] + np.dot(i, pts[j+1]))
                bez_sl = bez_sl.astype(int)
                drawPoint(bez_sl, BLUE, 1)
            if i == 0:
                pygame.draw.rect(screen, PINK, (pts[j][0] - margin, pts[j][1] - margin, 2 * margin, 2 * margin), 2)
        bez = bez.astype(int)
        drawPoint(bez, PURPLE, 3)



# draws the lines
#The final function for the program that will be implemented to draw out, move, and delete the points
def drawPolylines(color='GREEN', thick=3):

    if (count < 2): return

    for i in range(count - 1):

        # draws the straights lines connected by the dots

        drawLine(pts[i], pts[i + 1], GREEN)

        if event.type == pygame.KEYUP and event.key == pygame.K_l:
            # draws the lagrange curves
            lagrange(pts[i], pts[i + 1], PURPLE)
            pygame.draw.rect(screen, PINK, (1, 1, 350, 50))
            printText("Lagrange")

        # white out the entire page
        if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                # screen.fill(WHITE)
                screen.fill(WHITE)

        if event.type == pygame.KEYUP and event.key == pygame.K_h:
            hermite(pts[i], pts[i + 1], PINK)
            pygame.draw.rect(screen, PINK, (1, 1, 350, 50))
            printText("Hermite")

        if event.type == pygame.KEYUP and event.key == pygame.K_b:
            bezier(pts[i], pts[i + 1], RED)
            pygame.draw.rect(screen, PINK, (1, 1, 350, 50))
            printText("Bezier")




#functions for making the clock and timezones that can appear
def printText(msg, color='BLACK', pos=(1, 1)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

def time():

    pygame.draw.rect(screen, PINK, (1, 1, 350, 50))
    date = datetime.now()
    dateandtime = date.strftime("%d/%m/%Y %H:%M:%S")
    printText(dateandtime)





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
        # elif event.type == pygame.K_BACKSPACE and event.button == LEFT:
        # pygame.sprite.remove(cp)
        else:
            pressed = 0



    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = np.array([x, y])
    pygame.draw.circle(screen, RED, pt, 0)



    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        pts.append(pt)
        count += 1
        controlPoint((pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin), BLUE)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        clean = screen.fill(WHITE)
        screen.blit(clean,(pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin) )
        print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) + " button:" + repr(
            button1) + " pressed:" + repr(pressed) + " add pts ...")
        
        print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) + " button:" + repr(
            button1) + " pressed:" + repr(pressed))



    time()
    if len(pts) > 1:
        drawPolylines('GREEN', 1)


    # Go ahead and update the screen with what we've drawn.

    # This MUST happen after all the other drawing commands.

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed



pygame.quit()
