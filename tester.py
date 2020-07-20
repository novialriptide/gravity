import pymunk
import time

space = pymunk.Space()
space.gravity = 0,-100

body = pymunk.Body(1, 1666)
body.position = 1,100
w, h = 10, 10
poly = pymunk.Poly(body, [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)])

space.add(poly)

while(True):
    space.step(0.02)
    print(poly.body.position)
    time.sleep(0.2)