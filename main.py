"""
requirements
 - pypresence
"""
import pygame
import pypresence

import random
import sys
import json

import gamedenRE

SCREEN_SIZE = (500,500)
RENDER_SIZE = 1/8

NOISE_TEXTURE_IMAGE_PATH = "noise.png"
NOISE_TEXTURE_IMAGE = pygame.image.load(NOISE_TEXTURE_IMAGE_PATH)
NOISE_TEXTURE_IMAGE.set_alpha(40)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("GRAVITY: BETA")

# camera
camera_pos = [0,0]
camera_lag_speed = 25

# parallax objects
front_objects = [
    {
        "image": NOISE_TEXTURE_IMAGE,
        "rect": NOISE_TEXTURE_IMAGE.get_rect(),
        "scroll_speed": 0.25,
        "position": [0,0]
    }
]
back_objects = []

# default tile map setup
default_tileset = gamedenRE.tileset("test.png",(500,500))
test_tilemap = gamedenRE.convert_tiledjson("test.json")
d_tilemap = gamedenRE.tilemap(test_tilemap, default_tileset)
d_tilemap_image = d_tilemap.get_image_map(render_size=RENDER_SIZE)
map_pos = (0,0)

# player entity setup
t_width, t_height = d_tilemap.tile_size
start_pos = (t_width*2*RENDER_SIZE, t_height*1*RENDER_SIZE)
player_rect = pygame.Rect(start_pos[0], start_pos[1], 200*RENDER_SIZE, 200*RENDER_SIZE)
player = gamedenRE.entity(player_rect, 300, d_tilemap)
player.mass = 10

# gravity
gravity_speed = 60
gravity_setting = [0, gravity_speed]

# discord rpc
try:
    discord_rpc = pypresence.Presence(733388751878881441)
    discord_rpc.connect()
    discord_rpc.update(state="Campaign", details="Beta Testing")
except: pass

while(True):
    if clock.get_fps() != 0: dt = clock.get_fps()/1000
    else: dt = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            discord_rpc.close()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: gravity_setting = [0, dt*gravity_speed]
            if event.key == pygame.K_w: gravity_setting = [0, dt*-gravity_speed]
            if event.key == pygame.K_a: gravity_setting = [dt*-gravity_speed, 0]
            if event.key == pygame.K_d: gravity_setting = [dt*gravity_speed, 0]

    # camera movements
    _m = int(SCREEN_SIZE[0]/2)-int(player.rect.width/2)
    camera_pos[0] += (player.rect.x-camera_pos[0]-_m)/camera_lag_speed
    _m = int(SCREEN_SIZE[1]/2)-int(player.rect.height/2)
    camera_pos[1] += (player.rect.y-camera_pos[1]-_m)/camera_lag_speed

    player_movement = [0,0]
    collision_rects = d_tilemap.get_collision_rects(map_pos, 0, render_size=RENDER_SIZE)
    payload = {
        "collisions": collision_rects,
        "gravity": gravity_setting
    }
    player.physics = payload

    screen.fill((115, 115, 115))
    screen.blit(d_tilemap_image, (map_pos[0]-int(camera_pos[0]), map_pos[1]-int(camera_pos[1])))
    player.move(player_movement)
    pygame.draw.rect(screen, (100,100,100), [player.rect.x-int(camera_pos[0]), player.rect.y-int(camera_pos[1]), player.rect.width, player.rect.height])

    # parallax objects
    for f_object in front_objects:
        _fx = f_object["position"][0] - int(camera_pos[0]+(f_object["rect"].width)/2) * f_object["scroll_speed"]
        _fy = f_object["position"][1] - int(camera_pos[1]+(f_object["rect"].height)/2) * f_object["scroll_speed"]
        screen.blit(f_object["image"], (_fx, _fy))
    
    # HUD
    w_width, w_height = SCREEN_SIZE
    fps_text = gamedenRE.text(f"FPS: {int(clock.get_fps())}", 15, "Arial", (0,0,0))
    screen.blit(fps_text, (int(w_width - w_width/75 - fps_text.get_rect().width),int(w_height/75)))

    pygame.display.flip()
    clock.tick(60)