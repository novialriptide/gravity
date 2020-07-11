"""
requirements
 - pypresence
"""
import pygame
import sys
import json

import gamedenRE

SCREEN_SIZE = (500,500)
RENDER_SIZE = 1/10

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("GameDenREWRITE Tester")

# default tile map setup
default_tileset = gamedenRE.tileset("test.png",(500,500))
test_tilemap = gamedenRE.convert_tiledjson("test.json")
d_tilemap = gamedenRE.tilemap(test_tilemap, default_tileset)
d_tilemap_image = d_tilemap.get_image_map(render_size=RENDER_SIZE)
map_pos = (0,0)

# player entity setup
t_width, t_height = d_tilemap.tile_size
start_pos = (t_width*2*RENDER_SIZE, t_height*1*RENDER_SIZE)
player_rect = pygame.Rect(start_pos[0], start_pos[1], 20, 20)
player = gamedenRE.entity(player_rect, 300, d_tilemap)
player.weight = 5
player.jump_speed = 0.2
player_speed = 5

moving_right = False
moving_left = False

valid_gravity_settings = ["bottom", "top", "right", "left"]
current_gravity_setting = valid_gravity_settings[0]

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              sys.exit()
        if event.type == pygame.KEYDOWN:
            """
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_UP:
                if player.is_floating_tick < 6:
                    player.vertical_momentum = -10
            """
            if event.key == pygame.K_s: current_gravity_setting = valid_gravity_settings[0]
            if event.key == pygame.K_w: current_gravity_setting = valid_gravity_settings[1]
            if event.key == pygame.K_a: current_gravity_setting = valid_gravity_settings[2]
            if event.key == pygame.K_d: current_gravity_setting = valid_gravity_settings[3]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
    if clock.get_fps() != 0: delta_time = 1/clock.get_fps()
    else: delta_time = 0

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += player_speed
    if moving_left == True:
        player_movement[0] -= player_speed
    collision_rects = d_tilemap.get_collision_rects(map_pos, 0, render_size=RENDER_SIZE)

    screen.fill((115, 115, 115))
    screen.blit(d_tilemap_image, map_pos)
    player.move(player_movement, collision_rects, direction=current_gravity_setting)
    pygame.draw.rect(screen, (100,100,100), player.rect)

    w_width, w_height = SCREEN_SIZE
    fps_text = gamedenRE.text(f"FPS: {int(clock.get_fps())}", 15, "Arial", (0,0,0))
    screen.blit(fps_text, (int(w_width - w_width/75 - fps_text.get_rect().width),int(w_height/75)))

    pygame.display.flip()
    clock.tick(60)