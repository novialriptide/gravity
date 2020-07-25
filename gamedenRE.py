import pygame
import os
import json
import numpy
import math
import pymunk

def _calculate_segment_intersection(x1,y1,x2,y2,x3,y3,x4,y4):
    exception_msg = "two lines inputted are parallel or coincident"

    dem = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if dem == 0:
        raise Exception(exception_msg)

    t1 = (x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)
    t = t1/dem
    
    u1 = (x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)
    u = -(u1/dem)

    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        Px = x1 + t*(x2-x1)
        Py = y1 + t*(y2-y1)
        return Px, Py
    else:
        raise Exception(exception_msg)

def convert_rect_to_wall(rect):
    return (rect.left, rect.top, rect.right, rect.top), (rect.left, rect.bottom, rect.right, rect.bottom), (rect.left, rect.top, rect.left, rect.bottom), (rect.right, rect.top, rect.right, rect.bottom)

def convert_rects_to_walls(rects):
    walls = []
    for rect in rects:
        wall_lines = convert_rect_to_wall(rect)
        for wall_line in range(len(wall_lines)):
            walls.append(wall_lines[wall_line])
    return walls

def get_ray_endpoint(coord1,coord2,walls):
    x1, y1 = coord1
    x2, y2 = coord2
    line_length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    highest_point = (x2, y2)
    highest_point_length = line_length
    for wall in walls:
        try:
            c = _calculate_segment_intersection(x1, y1, x2, y2, wall[0], wall[1], wall[2], wall[3])
            c_length = math.sqrt((x1-c[0])**2 + (y1-c[1])**2)
            if highest_point_length > c_length:
                highest_point = c
                highest_point_length = c_length
        except: pass
    return highest_point

def get_v_movement(degree,speed):
    radian = math.radians(degree) 
    x_distance = math.cos(radian)*speed
    y_distance = math.sin(radian)*speed
    return [x_distance, y_distance]

def text(text,size,font,color):
    pygame.font.init()
    formatting = pygame.font.SysFont(font,size)
    text_surface = formatting.render(text,True,color)
    return text_surface

def convert_tiledjson(path):
    """Converts a tiled json map in GameDen's formatting"""
    with open(path, 'r') as file:
        loaded_json = json.load(file)

    contents = []
    for layer in range(len(loaded_json["layers"])):
        json_contents = loaded_json["layers"][layer]["data"]
        n = loaded_json["width"]
        layer_contents = [json_contents[i * n:(i + 1) * n] for i in range((len(json_contents) + n - 1) // n )]
        contents.append(layer_contents)
    tilemap = {
        #contents[layer_number][row][column]
        "contents": contents,
        "collision_layer": None,
        "invisible_layers": []
    }
    return tilemap

def grayscale(img):
    """Heavy function, turns an image to black and white"""
    arr = pygame.surfarray.array3d(img)

    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)

class button:
    def __init__(self, position: tuple, image_path, render_size: int = 1):
        x, y = position
        self.x, self.y = [x,y]
        self.image = pygame.image.load(image_path)
        self.render_size = render_size

    @property
    def rect(self):
        x, y = self.x, self.y
        return pygame.Rect(x, y,
            self.image.get_width()*self.render_size, 
            self.image.get_height()*self.render_size
        )

    def is_hovering(self, mouse_position: tuple) -> bool:
        """If the position inputed is on top of the button, it'll return True"""
        return self.rect.collidepoint(mouse_position)

    def pygame_render(self,surface):    
        image = pygame.transform.scale(self.image,(
            self.image.get_width()*self.render_size, 
            self.image.get_height()*self.render_size
        ))
        surface.blit(image, (self.rect.x, self.rect.y))

class tileset:
    def __init__(self, 
        textures_path: str, 
        tile_size: tuple, 
        tiles_distance: int = 0
    ):
        self.textures = pygame.image.load(textures_path)
        self.tile_size = tile_size
        self.tiles_distance = tiles_distance
        self.tileset_size = (
            int((self.textures.get_size())[0]/self.tile_size[0]),
            int((self.textures.get_size())[1]/self.tile_size[1])
        )

    def get_tile_id_pos(self,tile_id: int) -> tuple:
        """Returns the position of the inputed tile ID"""
        if (self.tileset_size[0]*self.tileset_size[1]) > tile_id:
            return (
                int(tile_id%(self.tileset_size)[0]),
                int(tile_id/(self.tileset_size)[0])
            )

    def pygame_render(self,position: tuple, surface, tile_id: int):
        """Renders an image of a tile. tile_id can never be 0"""
        t_width, t_height = self.tile_size
        if tile_id != 0:
            tile_id = tile_id - 1

            # cropping
            tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
            tile = tile.convert_alpha()
            t_x, t_y = self.get_tile_id_pos(tile_id)
            tile.blit(self.textures,(0,0),(
                t_width*t_x, t_height*t_y,
                t_width, t_height
            ))
            surface.blit(tile,position)

    def pygame_render2(self, tile_id: int):
        """Returns an image of a tile. tile_id can never be 0"""
        tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
        tile = tile.convert_alpha()
        if tile_id != 0:
            self.pygame_render(tile, (0,0), tile_id)
            return tile
        else: return tile

def rects_to_polys(space: pymunk.Space, rects: list) -> list:
    """This function should executed ONCE"""
    for rect in rects:
        def zero_gravity(body, gravity, damping, dt):
            pymunk.Body.update_velocity(body, (0,0), damping, dt)    
        _w, _h = rect[0].width, rect[0].height

        rect_b = pymunk.Body(1, 2, body_type=pymunk.Body.STATIC)
        rect_b.position = rect[0].x+_w/2, rect[0].y+_h/2
        rect_b.gameden = {"tile_id": rect[1]}
        rect_poly = pymunk.Poly(rect_b, [(-_w/2,-_h/2), (_w/2,-_h/2), (_w/2,_h/2), (-_w/2,_h/2)])
        rect_poly.friction = 0.8
        rect_poly.gameden = {"tile_id": rect[1]}
        space.add(rect_b, rect_poly)
        rect_b.velocity_func = zero_gravity

        rect.append(rect_b)
        rect.append(rect_poly)
        
    return rects

class tilemap:
    def __init__(self, map_data: dict, tileset):
        self.map_data = map_data
        map_contents = self.map_data["contents"]
        self.map_size = (len(map_contents[0][0]), len(map_contents[0]))
    
        self.tileset = tileset
        self.tile_size = tileset.tile_size
        self.textures = tileset.textures

    def get_position_by_px(self, position: tuple) -> tuple:
        x_px, y_px = position
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size

        return (
            (t_width*m_width-x_px)/m_width,
            (t_height*m_width-y_px)/m_height
        )

    def get_tile_id(self, position: tuple, layer: int) -> int:
        row,column = position
        try: return self.map_data["contents"][layer][row][column]
        except TypeError:
            raise Exception(f"tile location doesn't exist ({row}, {column})")

    def get_collision_rects(self, position: tuple, layer: int, render_size: int = 1) -> list:
        collision_rects = []
        a_x, a_y = position
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size

        y = 0
        for row in range(m_height):
            x = 0
            for column in range(m_width):
                tile_id = self.get_tile_id((row,column),layer)
                if tile_id != 0:
                    collision_rects.append(
                        [pygame.Rect(((a_x+x, a_y+y),(t_width*render_size, t_height*render_size))), tile_id]
                    )
                x += int(t_width*render_size)
            y += int(t_height*render_size)
        return collision_rects

    def set_position(self, new_position):
        self.rect.x, self.rect.y = new_position

    def create_new_layer(self):
        self.tilemap["contents"].append([[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])])
    
    def get_image_layer(self, layer_id: int):
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size
        map_surface = pygame.Surface((
            t_width*m_width,
            t_height*m_height
        ), pygame.SRCALPHA, 32)
        map_surface = map_surface.convert_alpha()
        
        for row in range(m_height):
            for column in range(m_width):
                tile_id = self.get_tile_id((row,column),layer_id)
                self.tileset.pygame_render((
                    column*t_width,
                    row*t_height
                ), map_surface, tile_id)

        return map_surface

    def get_image_map(self):
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size
        map_surface = pygame.Surface((
            t_width*m_width,
            t_height*m_height
        ), pygame.SRCALPHA, 32)
        map_surface = map_surface.convert_alpha()

        for layer in range(len(self.map_data["contents"])):
            if layer not in self.map_data["invisible_layers"]:
                map_surface.blit(self.get_image_layer(layer), (0,0))
        
        return map_surface

class entity:
    def __init__(self, body, size, tps=300, tilemap=None):
        self.tps = tps
        self.tilemap = tilemap

        # animations
        self.tick = 0
        self.current_texture = None
        self.image_offset_position = [0,0]

        # pymunk setup
        self.body = body
        self.width, self.height = size
        self.poly = pymunk.Poly(self.body, [
            (-self.width/2,-self.height/2), (self.width/2,-self.height/2), (self.width/2,self.height/2), (-self.width/2,self.height/2)
        ])
    
    def set_position(self, position: tuple, tilemap, tilemap_render_size: int = 1):
        x, y = position
        m_x, m_y = tilemap.position
        t_width, t_height = tilemap.tile_size

        self.body.position[0] = m_x+t_width*tilemap.render_size*x
        self.body.position[1] = m_y+t_height*tilemap.render_size*y
    