import pygame
import math
from random import randint
import csv

display_width = 800
display_height = 600
white = (255, 255, 255)
green = (0, 255, 0)

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Focus')
clock = pygame.time.Clock()

ingame = True
jumping = False
airtime = 0
count = 0
objpos = 600
rate_of_change = 5 # Speed at which the incoming object moves

while ingame: 
    objpos -= rate_of_change

    if jumping:
        count += 3 # every tick (or frame), the jump distance will change by 3

        if count < 60:
            airtime = count % 60
        else:
            airtime = 60 - (count - 60)

    if airtime == 0:
        jumping = False
        count = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ingame = False
            
        if event.type == pygame.KEYDOWN and airtime == 0:
            if event.key == pygame.K_SPACE:
                jumping = True

    gameDisplay.fill((0, 0, 0))
    pygame.draw.rect(gameDisplay, white, (200, 300 - airtime, 30, 30))
    pygame.draw.rect(gameDisplay, green, (objpos, 310, 25, 10))
    
    if 200 < objpos < 230 or 200 < objpos + 25 < 230: # Player starts at 200, rectangle is 30 pixels
        if 310 < 300 - airtime + 30 <= 330: # Collision with bullet
            ingame = False   

    pygame.display.update()
    if objpos < 100:
        objpos = 800
        rate_of_change = randint(4, 8)

    clock.tick(60)

