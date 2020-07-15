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
player.mass = 10
player.jump_speed = 0.2

# gravity
gravity_speed = 60
gravity_setting = [0, gravity_speed]

while(True):
    if clock.get_fps() != 0: dt = clock.get_fps()/1000
    else: dt = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: gravity_setting = [0, dt*gravity_speed]
            if event.key == pygame.K_w: gravity_setting = [0, dt*-gravity_speed]
            if event.key == pygame.K_a: gravity_setting = [dt*-gravity_speed, 0]
            if event.key == pygame.K_d: gravity_setting = [dt*gravity_speed, 0]

    player_movement = [0,0]
    collision_rects = d_tilemap.get_collision_rects(map_pos, 0, render_size=RENDER_SIZE)
    payload = {
        "collisions": collision_rects,
        "gravity": gravity_setting
    }
    player.physics = payload

    screen.fill((115, 115, 115))
    screen.blit(d_tilemap_image, map_pos)
    player.move(player_movement)
    pygame.draw.rect(screen, (100,100,100), player.rect)

    w_width, w_height = SCREEN_SIZE
    fps_text = gamedenRE.text(f"FPS: {int(clock.get_fps())}", 15, "Arial", (0,0,0))
    screen.blit(fps_text, (int(w_width - w_width/75 - fps_text.get_rect().width),int(w_height/75)))

    pygame.display.flip()
    print(player.momentum, player.mass)
    clock.tick(60)