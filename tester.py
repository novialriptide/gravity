"""
requirements
 - pypresence
"""
import pygame
import sys
import json

import gamedenRE

SCREEN_SIZE = (500,500)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("GameDenREWRITE Tester")

default_tileset = gamedenRE.tileset("test.png",(500,500))
test_tilemap = gamedenRE.convert_tiledjson("test.json")
d_tilemap = gamedenRE.tilemap(test_tilemap, default_tileset)
print(test_tilemap)
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              sys.exit()
    screen.fill((115, 115, 115))
    d_tilemap.pygame_render_map((0,0),screen,render_size=1/10)
    pygame.display.flip()