import pygame
import pymap

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Tester")

tileset = pymap.tileset("tiles.png", (5,5))

tile_map = pymap.tiledmap((3,4),tileset)
tile_map.modify_layer((0,0),1)
tile_map.add_new_layer()
tile_map.modify_layer((0,0),1, layer_id=1)
print(tile_map.tilemap)
print(tile_map.pygame_get_sprites(render_size=10))

running = True
while(running):
    screen.fill((100,100,100))
    tilemap = tile_map.pygame_render_map(render_size=10)
    screen.blit(tilemap, (0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False