import pygame
import pymap

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Tester")

tileset = pymap.tileset("tiles.png", (5,5))

tile_map = pymap.tiledmap((3,4),tileset)
print(tile_map.tilemap)
tile_map.modify_tile((0,0),1)
print(tile_map.tilemap)

print("tileset size: ", tileset.tileset_size)
print("17 pos:", tileset.get_tile_id_pos(17))

running = True
while(running):
    screen.fill((255,255,255))
    tile = tileset.pygame_render(6,render_size=10)
    screen.blit(tile, (0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False