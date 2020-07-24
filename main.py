import pygame
import pymunk
import pypresence

import random
import sys
import json

import gamedenRE

SCREEN_SIZE = (500,500)
RENDER_SIZE = 1/5

NOISE_TEXTURE_IMAGE_PATH = "textures/parallax/noise.png"
NOISE_TEXTURE_IMAGE = pygame.image.load(NOISE_TEXTURE_IMAGE_PATH)
NOISE_TEXTURE_IMAGE.set_alpha(40)

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("GRAVITY: BETA")
dt = 1

# camera
camera_pos = [0,0]
camera_lag_speed = 20

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

# pymunk setup
space = pymunk.Space()

# default tile map setup
default_tileset = gamedenRE.tileset("textures/tilesets/1.png",(500,500))
test_tilemap = gamedenRE.convert_tiledjson("levels/map2.json")
d_tilemap = gamedenRE.tilemap(test_tilemap, default_tileset)
d_tilemap_image = d_tilemap.get_image_map()
t_w, t_h = d_tilemap_image.get_rect().width, d_tilemap_image.get_rect().height
d_tilemap_image = pygame.transform.scale(d_tilemap_image, (int(t_w*RENDER_SIZE), int(t_h*RENDER_SIZE)))
map_pos = (0,0)

# player entity setup
t_width, t_height = d_tilemap.tile_size
body = pymunk.Body(100, 1666)
body.position = t_width*5*RENDER_SIZE, t_height*3*RENDER_SIZE
player = gamedenRE.entity(body, [200*RENDER_SIZE,200*RENDER_SIZE])
player.poly.friction = 1
player.poly.elasticity = 0
space.add(player.body, player.poly)

# gravity
gravity_speed = 5000
space.gravity = 0,dt*-gravity_speed

# collisions
polys = gamedenRE.rects_to_polys(space, d_tilemap.get_collision_rects((0,0), 0, render_size=RENDER_SIZE))
"""
# discord rpc
try:
    discord_rpc = pypresence.Presence(733388751878881441)
    discord_rpc.connect()
    discord_rpc.update(state="Beta Testing")
except: pass
"""
while(True):
    if clock.get_fps() != 0: dt = clock.get_fps()/1000
    else: dt = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            discord_rpc.close()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: space.gravity = 0,dt*gravity_speed
            if event.key == pygame.K_w: space.gravity = 0,dt*-gravity_speed
            if event.key == pygame.K_a: space.gravity = dt*-gravity_speed,0
            if event.key == pygame.K_d: space.gravity = dt*gravity_speed,0

    # camera movements
    _m = int(SCREEN_SIZE[0]/2)-int(player.width/2)
    camera_pos[0] += (player.body.position[0]-camera_pos[0]-_m)/camera_lag_speed
    _m = int(SCREEN_SIZE[1]/2)-int(player.height/2)
    camera_pos[1] += (player.body.position[1]-camera_pos[1]-_m)/camera_lag_speed

    # map + background
    screen.fill((115, 115, 115))
    screen.blit(d_tilemap_image, (map_pos[0]-int(camera_pos[0]), map_pos[1]-int(camera_pos[1])))

    # draw main object
    x, y = player.body.position
    local_vertices = player.poly.get_vertices()
    player_vertices = []
    for vertice in local_vertices:
        vx, vy = vertice
        player_vertices.append([vx+x-int(camera_pos[0]), vy+y-int(camera_pos[1])])
    pygame.draw.polygon(screen, (61,143,166), player_vertices)
    
    # debugging tilemap hitboxes
    """
    for rect in polys:
        pygame.draw.rect(screen, (255,255,255), [rect[1].position[0]-rect[0].width/2-camera_pos[0], rect[1].position[1]-rect[0].height/2-camera_pos[1], rect[0].width, rect[0].height])
    """

    # front parallax objects
    for f_object in front_objects:
        _fx = f_object["position"][0] - int(camera_pos[0]+(f_object["rect"].width)/2) * f_object["scroll_speed"]
        _fy = f_object["position"][1] - int(camera_pos[1]+(f_object["rect"].height)/2) * f_object["scroll_speed"]
        screen.blit(f_object["image"], (_fx, _fy))

    # HUD
    w_width, w_height = SCREEN_SIZE
    fps_text = gamedenRE.text(f"FPS: {int(clock.get_fps())}", 15, "Arial", (0,0,0))
    screen.blit(fps_text, (int(w_width - w_width/75 - fps_text.get_rect().width),int(w_height/75)))

    pygame.display.flip()
    space.step(0.02)
    clock.tick(60)