import pymunk
import pygame
import sys

import gamedenRE

SCREEN_SIZE = [500,500]
friction = 1
elasticity = 0
SEGMENTS = [
    {"elasticity": elasticity, "friction": friction, "point1": [0,0], "point2": [500,0], "radius": 1},
    {"elasticity": elasticity, "friction": friction, "point1": [0,500], "point2": [500,500], "radius": 1},
    {"elasticity": elasticity, "friction": friction, "point1": [0,0], "point2": [0,500], "radius": 1},
    {"elasticity": elasticity, "friction": friction, "point1": [500,0], "point2": [500,500], "radius": 1}
]
RECTS = [
    [pygame.Rect(50,50,100,100)]
]

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pymunk Tester")

# pymunk setup
gravity_speed = 1
space = pymunk.Space()
space.gravity = 0,gravity_speed

# collisions
for segment in SEGMENTS:
    s = pymunk.Segment(space.static_body, segment["point1"], segment["point2"], segment["radius"])
    s.elasticity = segment["elasticity"]
    s.friction = segment["friction"]
    space.add(s)

rect_number = 0
for rect in RECTS:
    def zero_gravity(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, (0,0), damping, dt)
    
    rect_b = pymunk.Body(1, 2, body_type=pymunk.Body.STATIC)
    rect_b.position = rect[0].x, rect[0].y
    _w, _h = rect[0].width, rect[0].height
    rect_poly = pymunk.Poly(rect_b, [(-_w/2,-_h/2), (_w/2,-_h/2), (_w/2,_h/2), (-_w/2,_h/2)])
    space.add(rect_b, rect_poly)
    rect_b.velocity_func = zero_gravity

    rect.append(rect_b)
    rect.append(rect_poly)

    rect_number += 1

# character
body = pymunk.Body(100, 1666)
body.position = 100,100
player = gamedenRE.entity(body, [50,50])
"""
w, h = 50, 50
poly = pymunk.Poly(body, [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)])
"""
space.add(player.body, player.poly)

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: space.gravity = 0,gravity_speed
            if event.key == pygame.K_w: space.gravity = 0,-gravity_speed
            if event.key == pygame.K_a: space.gravity = -gravity_speed,0
            if event.key == pygame.K_d: space.gravity = gravity_speed,0
    screen.fill((0,0,0))
    for segment in SEGMENTS:
        pygame.draw.line(screen, (255,255,255), segment["point1"], segment["point2"], width=segment["radius"])
    for rect in RECTS:
        pygame.draw.rect(screen, (255,255,255), [rect[1].position[0]-rect[0].width/2, rect[1].position[1]-rect[0].height/2, rect[0].width, rect[0].height])
    pygame.draw.rect(screen, (0,255,0), [
        player.body.position[0]-player.width/2, player.body.position[1]-player.height/2,
        player.width, player.height
    ])

    pygame.display.flip()
    space.step(0.02)
