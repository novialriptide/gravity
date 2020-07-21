import pymunk
import pygame
import sys

SCREEN_SIZE = [500,500]
friction = 1
elasticity = 0
SEGMENTS = [
    {"elasticity": elasticity, "friction": friction, "point1": [0,0], "point2": [500,0], "radius": 1},
    {"elasticity": elasticity, "friction": friction, "point1": [0,500], "point2": [500,500], "radius": 1},
    {"elasticity": elasticity, "friction": friction, "point1": [0,0], "point2": [0,500], "radius": 1},
    {"elasticity": elasticity, "friction": friction, "point1": [500,0], "point2": [500,500], "radius": 1}
]

def rect_to_poly(rect: pygame.Rect) -> pymunk.Poly:
    w, h = 10, 10
    poly = pymunk.Poly(body, [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)])

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

# character
body = pymunk.Body(100, 1666)
body.position = 100,100
w, h = 10, 10
poly = pymunk.Poly(body, [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)])

space.add(body, poly)

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
    pygame.draw.rect(screen, (255,255,255), [
        body.position[0], body.position[1],
        w, h
    ])

    pygame.display.flip()
    space.step(0.02)
