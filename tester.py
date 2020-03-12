import pygame
import engine 

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Tester")
render_size = 10

tileset = engine.tileset("tiles.png", (5,5), render_size=render_size)

tile_map = engine.tiledmap((3,4),tileset,(0,0), render_size=render_size)
tile_map.modify_layer((0,1),1, layer_id=0)
tile_map.add_new_layer()
tile_map.modify_layer((0,1),1, layer_id=1)
tile_map.generate_collision_rects()

player = engine.entity((0, 0), (5,5), map_class=tile_map, render_size=render_size)
player_speed = 3
player.force_texture_rect((220,20,220))

running = True
while(running):
    screen.fill((100,100,100))
    tile_map.pygame_render_map(screen, (0,0))
    player.pygame_render(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(tile_map.collision_rects)
            if event.key == pygame.K_w:
                player.move((0,-player_speed), obey_collisions=True)
            if event.key == pygame.K_s:
                player.move((0,player_speed), obey_collisions=True)
            if event.key == pygame.K_a:
                player.move((-player_speed,0), obey_collisions=True)
            if event.key == pygame.K_d:
                player.move((player_speed,0), obey_collisions=True)