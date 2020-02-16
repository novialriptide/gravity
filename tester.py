import pygame
import pymap

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Tester")

map_options = (
    (3,4),
    "",
    (5,5)
)
tile_map = pymap.tiled(map_options)
tile_map.modify_tile((0,0),1)

running = True
while(running):
    screen.blit(tile_map.pygame_render((0,0), 0), (0,0))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False