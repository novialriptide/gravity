import pygame
import pymap

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Tester")

tileset = pymap.tileset("tiles.png", (5,5))

tile_map = pymap.tiledmap((3,4),tileset)
print(tile_map.get_tilemap())
tile_map.modify_tile((0,0),1)
print(tile_map.get_tilemap())
tile_map.pygame_render_layer(0)

print(tileset.get_tileset_size())
print(tileset.get_tile_id_pos(17))

"""
running = True
while(running):
    screen.blit(tile_map.pygame_render_map((0,0), 0), (0,0))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False
"""