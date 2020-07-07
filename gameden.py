#######################################################
#    GAME DEN ENGINE (2020)                           #
#######################################################
import pygame
import os
import json
import numpy
import math

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

def text(text,size,font,color,render_size=1):
    pygame.font.init()
    formatting = pygame.font.SysFont(font,size*render_size)
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
        "collision_layer": 0,
        "invisible_layers": [0]
    }
    return tilemap

def grayscale(img):
    """Heavy function, turns an image to black and white"""
    arr = pygame.surfarray.array3d(img)

    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)

class button:
    def __init__(self,position,image_path,render_size=1):
        x, y = position
        self.image = pygame.image.load(image_path)
        self.render_size = render_size
        self.rect = pygame.Rect(x, y,
            self.image.get_width()*self.render_size, 
            self.image.get_height()*self.render_size
        )
    
    @property
    def size(self):
        return [self.rect.width, self.rect.height]

    @property
    def position(self):
        return [self.rect.x, self.rect.y]

    def set_position(self,position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def is_hovering(self,mouse_position):
        """If the position inputed is on top of the button, it'll return True"""
        return self.rect.collidepoint(mouse_position)

    def pygame_render(self,surface):    
        image = pygame.transform.scale(self.image,(
            self.image.get_width()*self.render_size, 
            self.image.get_height()*self.render_size
        ))
        surface.blit(image, self.position)

class pygame_timer:
    def __init__(self, time):
        """Creates a timer"""
        self.time = time
        self.valid = True
        self.started = False

    def start(self):
        """Starts the timer."""
        if self.started == False:
            self.origin_ticks = pygame.time.get_ticks()
            self.started = True

    def check_time(self, make_invalid=False):
        """Returns a boolean if the timer has reached its targeted frame"""
        current_ticks = pygame.time.get_ticks()
        try:
            if current_ticks - self.origin_ticks >= self.time and self.valid and self.started:
                self.origin_ticks = current_ticks
                if make_invalid == True:
                    self.valid = False
                return True
            else: return False
        except AttributeError: pass

class tileset:
    def __init__(self,textures,tile_size,render_size=1,tiles_distance=0):
        self.textures = pygame.image.load(textures)
        self.tile_size = tile_size
        self.tiles_distance = tiles_distance
        self.render_size = render_size
        self.tileset_size = (
            int((self.textures.get_size())[0]/self.tile_size[0]),
            int((self.textures.get_size())[1]/self.tile_size[1])
        )

    def get_tile_id_pos(self,tile_id):
        """Returns the position of the inputed tile ID"""
        if (self.tileset_size[0]*self.tileset_size[1]) > tile_id:
            return (
                int(tile_id%(self.tileset_size)[0]),
                int(tile_id/(self.tileset_size)[0])
            )

    def pygame_render(self,surface,position,tile_id):
        """Renders an image of a tile. tile_id can never be 0"""
        if tile_id != 0:
            tile_id = tile_id - 1
            tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
            tile = tile.convert_alpha()
            tile_pos = self.get_tile_id_pos(tile_id)
            tile.blit(self.textures,(0,0),(
                self.tile_size[0]*tile_pos[0],
                self.tile_size[1]*tile_pos[1],
                self.tile_size[0], self.tile_size[1]
            ))
            tile = pygame.transform.scale(tile,(
                self.tile_size[0]*self.render_size,
                self.tile_size[1]*self.render_size
            ))
            surface.blit(tile,position)

    def pygame_render2(self, tile_id):
        """Returns an image of a tile. tile_id can never be 0"""
        tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
        tile = tile.convert_alpha()
        if tile_id != 0:
            self.pygame_render(tile,(0,0),tile_id)
            return tile
        else: return tile

class tiledmap:
    def __init__(self,tiledmap,tileset_class,position,render_size=1,chunk_size=(5,5)):
        self.tileset = tileset_class
        self.tile_size = tileset_class.tile_size
        self.tilemap = tiledmap
        self.map_size = (
            len(self.tilemap["contents"][0]), #height          # I HAVE NO IDEA HOW TO FIX THIS
            len(self.tilemap["contents"][0][0]) #width
        )
        self.chunk_size = chunk_size
        self.map_textures_path = tileset_class.textures
        self.render_size = render_size
        self.position = position
        self.collision_rects = []
    
    @property
    def map_rect(self):
        """Returns a pygame Rect for collision or camera"""
        return pygame.Rect(self.position,(
            self.render_size*self.tile_size[0]*self.map_size[1],
            self.render_size*self.tile_size[1]*self.map_size[0]
        ))

    def modify_layer(self,position,tile_id,layer_id=0):
        """Changes a tile ID texture"""
        row,column = position
        if layer_id != self.tilemap["collision_layer"]:
            self.tilemap["contents"][layer_id][row][column] = tile_id
        if layer_id == self.tilemap["collision_layer"]:
            self.tilemap["contents"][layer_id][row][column] = 1

    def add_new_layer(self):
        """Adds a new layer with an empty multidimensional array"""
        self.tilemap["contents"].append([[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])])

    def get_position(self,position):
        """Returns a tuple to reveal the tilemap position"""
        x,y = position
        x = int((x-self.position[0])/(self.tile_size[0]*self.render_size))
        y = int((y-self.position[1])/(self.tile_size[1]*self.render_size))
        return (x, y)

    def get_tile_id(self,position,layer):
        """Returns a tile ID from the specified position"""
        row,column = position
        try: return self.tilemap["contents"][layer][row][column]
        except TypeError:
            raise Exception(f"tile location doesn't exist ({row}, {column})")

    def get_tile_id2(self,position,layer):
        """Returns a tile ID from the specified position in pixels"""
        x, y = self.get_position(position)
        try: return self.tilemap["contents"][layer][x][y]
        except TypeError:
            raise Exception(f"tile location doesn't exist ({x}, {y})")

    def generate_rects(self, layer):
        """Returns a list of pygame Rects from a layer from the specified position"""
        collision_rects = []
        for row in range(self.map_size[0]):
            for column in range(self.map_size[1]):
                tile_id = self.get_tile_id((row,column),layer)
                if tile_id != 0:
                    new_rect = pygame.Rect(((
                        self.position[0]+column*self.tile_size[0]*self.render_size,
                        self.position[1]+row*self.tile_size[1]*self.render_size
                    ),(
                        self.tile_size[0]*self.render_size,
                        self.tile_size[1]*self.render_size
                    )))
                    collision_rects.append(new_rect)
        if layer == self.tilemap["collision_layer"]: 
            self.collision_rects = collision_rects
        return collision_rects

    def center(self, surface_size):
        """Centers the position"""
        surface_width, surface_height = surface_size
        map_size = self.map_rect.size
        self.position = [
            surface_width/2-map_size[0]/2,
            surface_height/2-map_size[1]/2
        ]

    def move(self,vposition):
        """Moves the map from its relative position"""
        self.position = (
            self.position[0]+vposition[0],
            self.position[1]+vposition[1]
        )

    def pygame_render_chunk(self,surface,map_size,chunk_position):
        """Renders a chunk of a layer of the map"""
        map_surface = pygame.Surface((
            self.tile_size[1]*self.chunk_size[1]*self.render_size,
            self.tile_size[0]*self.chunk_size[0]*self.render_size
        ))

    def pygame_render_layer(self,surface,layer_id):
        """Renders a specific layer of the map"""
        map_surface = pygame.Surface((
            self.tile_size[1]*self.map_size[1]*self.render_size,
            self.tile_size[0]*self.map_size[0]*self.render_size
        ), pygame.SRCALPHA, 32)
        map_surface = map_surface.convert_alpha()

        for row in range(self.map_size[0]):
            for column in range(self.map_size[1]):
                tile_id = self.get_tile_id((row,column),layer_id)
                self.tileset.pygame_render(map_surface,(
                    column*self.tile_size[0]*self.render_size,
                    row*self.tile_size[1]*self.render_size
                ),tile_id)
        surface.blit(map_surface,self.position)

    def pygame_render_map(self,surface):
        """Renders the entire map"""
        for layer in range(len(self.tilemap["contents"])):
            if layer not in self.tilemap["invisible_layers"]:
                self.pygame_render_layer(surface,layer)
    
    def get_rendered_map(self):
        """Returns a surface of the entire map"""
        surface = pygame.Surface((
            self.tile_size[1]*self.map_size[1]*self.render_size,
            self.tile_size[0]*self.map_size[0]*self.render_size
        ), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()
        old_position = self.position
        self.position = (0,0)
        for layer in range(len(self.tilemap["contents"])):
            if layer not in self.tilemap["invisible_layers"]:
                self.pygame_render_layer(surface,layer)
        self.position = old_position
        return surface

class Rect:
   def __init__(self, x, y, w, h):
      self.x = x
      self.y = y
      self.w = w
      self.h = h
   def collidepoint(self, p):
      return (self.x > p[0] > self.x+self.w) and\
         (self.y > p[1] > self.y+self.h)

   def colliderect(self, rect):
      here = self.collidepoint(rect.x) or self.collidepoint(rect.y) or self.collidepoint(rect.x+rect.w) or self.collidepoint(rect.y+rect.h)
      there = rect.collidepoint(self.x) or rect.collidepoint(self.y) or rect.collidepoint(self.x+self.w) or rect.collidepoint(self.y+self.h)
      return there or here

class entity:
    def __init__(self,rect,tps=300,map_class=None,render_size=1):
        self.entity_data = {"animation_sprites": {}}
        self.render_size = render_size
        self.tick = 0
        self.tps = tps
        self.map_class = map_class
        self.current_texture = None
        self.rect = rect
        self.image_offset_position = [0,0]
        self.position_float = [self.rect.x, self.rect.y]

    @property
    def image_size(self):
        return self.current_texture.get_rect().size

    @property
    def image_position(self):
        return [self.rect.x+self.image_offset_position[0], self.rect.y+self.image_offset_position[1]]

    @property
    def image_position_middle(self):
        return [
            int((self.rect.left + self.image_offset_position[0] + self.rect.right + self.image_offset_position[0])/2), 
            int((self.rect.bottom + self.image_offset_position[1] + self.rect.top + self.image_offset_position[1])/2)
        ]

    @property
    def size(self):
        return self.rect.size

    @property
    def position(self):
        return [self.rect.x, self.rect.y]

    @property
    def position_middle(self):
        return [int((self.rect.left + self.rect.right)/2), int((self.rect.bottom + self.rect.top)/2)]

    @property
    def position_offset(self):
        """WIP: Returns the entity's offset position to the tile they're standing on"""
        position_in_tiles = self.map_class.get_position(self.get_position())
        return (
            self.rect.x-(position_in_tiles[0]*self.map_class.tile_size[0]*self.map_class.render_size),
            self.rect.y-(position_in_tiles[1]*self.map_class.tile_size[1]*self.map_class.render_size)
        )

    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def set_position(self,position):
        """Sets the entity's position to a specific position in pixels"""
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.position_float = position
    
    def set_position2(self,position,tilemap):
        """Sets the entity's position to a specific position"""
        self.rect.x = tilemap.position[0]+tilemap.tile_size[0]*tilemap.render_size*position[0]
        self.rect.y = tilemap.position[1]+tilemap.tile_size[1]*tilemap.render_size*position[1]
        self.position_float = [self.rect.x, self.rect.y]

    def center(self,surface_size):
        """Centers the position"""
        surface_width, surface_height = surface_size
        map_size = self.map_rect.size
        self.rect.x = surface_width/2-map_size[0]/2,
        self.rect.y = surface_height/2-map_size[1]/2
        self.position_float = [self.rect.x, self.rect.y]

    def move(self,movement,obey_collisions=False,movement_accurate=False):
        """Moves the object relative from it's position"""
        player_rect = self.rect
        collisions = self.map_class.collision_rects
        collision_types = {
            "top": False,
            "bottom": False,
            "right": False,
            "left": False
        }
        if movement_accurate:
            self.position_float[0] += movement[0]
            player_rect.x += movement[0] + (self.position_float[0] - self.rect.x)
        else:
            player_rect.x += movement[0]

        if obey_collisions:
            hit_list = self.collision_test(player_rect,collisions)
            for tile in hit_list:
                if movement[0] > 0:
                    player_rect.right = tile.left
                    collision_types["right"] = True
                elif movement[0] < 0:
                    player_rect.left = tile.right
                    collision_types["left"] = True

        if movement_accurate:
            self.position_float[1] += movement[1]
            player_rect.y += movement[1] + (self.position_float[1] - self.rect.y)
        else:
            player_rect.y += movement[1]

        if obey_collisions:
            hit_list = self.collision_test(player_rect,collisions)
            for tile in hit_list:
                if movement[1] > 0:
                    player_rect.bottom = tile.top
                    collision_types["bottom"] = True
                elif movement[1] < 0:
                    player_rect.top = tile.bottom
                    collision_types["top"] = True
        
        return collision_types

    def play_animation(self,animation_dict_name):
        """Starts the animation"""
        number_of_sprites = len(self.entity_data["animation_sprites"][animation_dict_name])
        if self.tick == number_of_sprites*self.tps:
            self.tick = 0
        try:
            self.current_texture = self.entity_data["animation_sprites"][str(animation_dict_name)][self.tick//self.tps]
            width, height = self.current_texture.get_size()
            self.current_texture = pygame.transform.scale(self.current_texture, (
                width*self.render_size,
                height*self.render_size
            ))
            self.rect = pygame.Rect(
                (self.rect.x, self.rect.y),
                (width*self.render_size,height*self.render_size)
            )
        except IndexError:
            raise Exception(f"sprite does not exist ({self.tick//self.tps})")
        except ZeroDivisionError:
            raise Exception(f"tps is invalid")

    def stop_animation(self):
        """Stops the animation"""
        self.tick = 0
    
    def new_animation_data(self,name,data):
        """Stores the entity's sprite information. Inside the data variable should be a list of the sprite images in order"""
        self.entity_data["animation_sprites"][str(name)] = data

    def pygame_render(self,surface):
        """Renders the entity's sprite"""
        surface.blit(self.current_texture,(
            self.rect.x+self.image_offset_position[0]*self.render_size, 
            self.rect.y+self.image_offset_position[1]*self.render_size
        ))

class projectile:
    def __init__(self,rect,end_pos,speed,render_size=1):
        self.rect = rect
        self.start_pos = (rect.x, rect.y)
        self.end_pos = end_pos
        self.speed = speed
        self.moving = True
        self.entity = entity(rect,render_size=render_size)
        self.render_size = render_size

        x1,y1 = self.start_pos
        x2,y2 = self.end_pos
        modifier = 0
        if x2-x1 == 0:
            original_degree = 90
            if y2-y1 < 0:
                original_degree = 90+180
        else:
            original_degree = math.degrees(math.atan((y2-y1)/(x2-x1)))
        if x2-x1 < 0:
            modifier = 180
        self.degree = original_degree+modifier
        self.movement = get_v_movement(self.degree,speed)

    def update_pos(self, move_after_collisions=False, obey_collisions=False, deflect=False):
        if self.moving:
            collisions = self.entity.move(self.movement,obey_collisions=obey_collisions,movement_accurate=True)
            if collisions["right"] or collisions["left"] or collisions["top"] or collisions["bottom"]:
                if move_after_collisions:
                    self.moving = False
                if deflect:
                    pass

    def pygame_render_rect(self,surface,color):
        current_pos = self.entity.position
        width, height = self.rect.size
        pygame.draw.rect(
            surface, color, [current_pos[0]-width/2, current_pos[1]-height/2, 
            width*self.render_size, 
            height*self.render_size
        ])

class network:
    def __init__(self):
        pass