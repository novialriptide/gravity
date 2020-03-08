import pygame
import engine 

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Tester")
render_size = 10

tileset = engine.tileset("tiles.png", (5,5), render_size=render_size)

tile_map = engine.tiledmap((3,4),tileset,(0,0))
tile_map.modify_layer((0,0),1, layer_id=0)
tile_map.modify_layer((0,1),1, layer_id=0)
tile_map.add_new_layer()
tile_map.modify_layer((0,0),1, layer_id=1)
tile_map.modify_layer((0,3),1, layer_id=1)
tile_map.set_render_size(render_size)

print(tile_map.tilemap)
print(tile_map.get_collision_rects())
print(tile_map.get_map_border_rect())

running = True
while(running):
    screen.fill((100,100,100))
    tile_map.pygame_render_map(screen, (0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False