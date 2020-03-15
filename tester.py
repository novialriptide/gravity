import pygame
import os

import engine

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Tester")
render_size = 7

tileset = engine.tileset(os.path.join("data","tiles.png"),(5,5),render_size=render_size)

tiled_map_contents = engine.generate_tiledmap((4,3))

tile_map = engine.tiledmap(tiled_map_contents,tileset,(0,0),render_size=render_size)
tile_map.modify_layer((0,1),1,layer_id=0)
tile_map.add_new_layer()
tile_map.modify_layer((0,1),1,layer_id=1)
tile_map.generate_collision_rects()

player = engine.entity((0,0),(5,5),map_class=tile_map,render_size=render_size)
player_speed = 0.05
player_movement = [0,0]

player.new_animation_data("idle",[
    player.texture_color_rect((231,0,127))
])

player.new_animation_data("forward",[
    player.texture_color_rect((231,124,127)),
    player.texture_color_rect((0,20,127)),
    player.texture_color_rect((101,30,167)),
])
player.new_animation_data("backward",[
    player.texture_color_rect((231,104,127)),
    player.texture_color_rect((0,20,0)),
    player.texture_color_rect((101,130,0)),
])
player.new_animation_data("left",[
    player.texture_color_rect((231,124,0)),
    player.texture_color_rect((0,20,127)),
    player.texture_color_rect((0,130,167)),
])
player.new_animation_data("right",[
    player.texture_color_rect((0,0,127)),
    player.texture_color_rect((0,20,0)),
    player.texture_color_rect((101,130,167)),
])

text1 = engine.text_formating("If everything seems to be working,everything is working.",20,(255,255,255))

running = True
while(running):
    if player_movement == [0,0]:
        player.play_animation("idle")
        player.update_animation_tick()
    if player_movement[1] > 0:
        player.play_animation("backward")
        player.update_animation_tick()
    if player_movement[1] < 0:
        player.play_animation("forward")
        player.update_animation_tick()
    if player_movement[0] < 0:
        player.play_animation("left")
        player.update_animation_tick()
    if player_movement[0] > 0:
        player.play_animation("right")
        player.update_animation_tick()

    screen.fill((100,100,100))
    tile_map.pygame_render_map(screen,(0,0))
    player.pygame_render(screen)
    player.move(player_movement,obey_collisions=True)
    text1.pygame_render(screen,(0,300))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_movement[1] = -player_speed
            if event.key == pygame.K_s:
                player_movement[1] = player_speed
            if event.key == pygame.K_a:
                player_movement[0] = -player_speed
            if event.key == pygame.K_d:
                player_movement[0] = player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_movement[1] = 0
                player.stop_animation()
            if event.key == pygame.K_s:
                player_movement[1] = 0
                player.stop_animation()
            if event.key == pygame.K_a:
                player_movement[0] = 0
                player.stop_animation()
            if event.key == pygame.K_d:
                player_movement[0] = 0
                player.stop_animation()