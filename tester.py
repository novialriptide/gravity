import pygame
import sys

import gamedenRE

SCREEN_SIZE = [500,500]

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pymunk Tester")

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()