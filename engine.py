#######################################################
#    GAME DEN ENGINE v1.4.9 (2020)                    #
#    text_formating,tileset,tiledmap,entity,          #
#    pygame_timer                                     #
#######################################################
#    DEVELOPED BY ANDREW HONG                         #
#######################################################
import pygame
import os
import json

def generate_tiledmap(map_size):
    """Creates a new empty multidimensional array in GameDen's formatting"""
    width,height = map_size
    tilemap = {
        #map_contents[layer_number][row][column]
        "map_contents": [[[0 for j in range(width)] for i in range(height)]],
        "collision_layer": 0
    }
    return tilemap

def convert_tiledjson(path):
    """Converts a tiled json map in GameDen's formatting"""
    with open(path, 'r') as file:
        loaded_json = json.load(file)

    map_contents = []
    for layer in range(len(loaded_json["layers"])):
        json_contents = loaded_json["layers"][layer]["data"]
        n = loaded_json["width"]
        layer_contents = [json_contents[i * n:(i + 1) * n] for i in range((len(json_contents) + n - 1) // n )]
        map_contents.append(layer_contents)
    tilemap = {
        #map_contents[layer_number][row][column]
        "map_contents": map_contents,
        "collision_layer": 0
    }
    return tilemap

class text_formating:
    def __init__(self,size,font="default",font_type="ttf",render_size=1):
        pygame.font.init()
        self.font = font
        self.size = size
        self.render_size = render_size
        self.font_type = font_type

        if self.font == "default":
            # planned to implement custom font in v2.0 with GameDen's format
            font_used = os.path.join("textures","pixel.ttf")
            self.font_type = "ttf"

        self.formatting = pygame.font.SysFont(font_used,size*render_size)

    def get_rect(self):
        """Returns a pygame Rect for collision"""
        return pygame.Rect(self.position,(
            self.formatting.get_width()*self.render_size,
            self.formatting.get_height()*self.render_size
        ))
    
    def pygame_render(self,surface,text,position,color=(255,255,255)):
        """Renders a text with the formatting applied"""
        x,y = position
        position = (x,y)
        text_surface = self.formatting.render(text,True,color)
        surface.blit(text_surface,(x,y))

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
            else:
                return False
        except AttributeError:
            pass

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

    def set_render_size(self,render_size):
        """Changes the size of the tile when rendering"""
        self.render_size = render_size

    def pygame_render(self,surface,position,tile_id):
        """Renders an image of a tile. tile_id can never be 0"""
        if tile_id != 0:
            tile_id = tile_id - 1
            tile = pygame.Surface(self.tile_size)
            tile_pos = self.get_tile_id_pos(tile_id)
            tile.blit(self.textures,(0,0),(
                self.tile_size[0]*tile_pos[0],
                self.tile_size[1]*tile_pos[1],
                self.tile_size[0],
                self.tile_size[1]
            ))
            tile = pygame.transform.scale(tile,(
                self.tile_size[0]*self.render_size,
                self.tile_size[1]*self.render_size
            ))
            surface.blit(tile,position)

    def pygame_render2(self, tile_id):
        """Returns an image of a tile. tile_id can never be 0"""
        tile = pygame.Surface(self.tile_size)
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
            len(self.tilemap["map_contents"][0]), #height          # I HAVE NO IDEA HOW TO FIX THIS
            len(self.tilemap["map_contents"][0][0]) #width
        )
        self.chunk_size = chunk_size
        self.map_textures_path = tileset_class.textures
        self.render_size = render_size
        self.position = position
        self.original_position = position
        self.collision_rects = []

########################## OPTIONS METHODS #########################

    def set_render_size(self,render_size):
        """Changes the size of the map when rendering"""
        self.render_size = render_size

######################## ENTITY DATA METHODS #######################

    def add_map_data(self, data_name, data_contents):
        self.tilemap[data_name] = data_contents
    
    def remove_map_data(self, data_name):
        del self.tilemap[data_name]

########################### LAYER METHODS ##########################

    def modify_layer(self,position,tile_id,layer_id=0):
        """Changes a tile ID texture"""
        row,column = position
        if layer_id != self.tilemap["collision_layer"]:
            self.tilemap["map_contents"][layer_id][row][column] = tile_id
        if layer_id == self.tilemap["collision_layer"]:
            self.tilemap["map_contents"][layer_id][row][column] = 1

    def add_new_layer(self):
        """Adds a new layer with an empty multidimensional array"""
        self.tilemap["map_contents"].append([[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])])

############################ GET METHODS ###########################

    def get_position(self,position):
        """Returns a tuple to reveal the a tilemap position"""
        x,y = position
        x = int((x-self.position[0])/(self.tile_size[0]*self.render_size))
        y = int((y-self.position[1])/(self.tile_size[1]*self.render_size))
        return (x, y)

    def get_tile_id(self,position,layer):
        """Returns a tile ID from the specified position"""
        row,column = position
        try:
            return self.tilemap["map_contents"][layer][row][column]
        except TypeError:
            raise Exception(f"tile location doesn't exist ({row}, {column})")

    def get_tile_id2(self,position,layer):
        """Returns a tile ID from the specified position in pixels"""
        x, y = self.get_position(position)
        try:
            return self.tilemap["map_contents"][layer][x][y]
        except TypeError:
            raise Exception(f"tile location doesn't exist ({x}, {y})")

####################### GET/COLLISION METHODS ######################

    def generate_collision_rects(self):
        """Returns a list of pygame Rects from the collision layer from the specified position"""
        collision_rects = []
        for row in range(self.map_size[0]):
            for column in range(self.map_size[1]):
                tile_id = self.get_tile_id((row,column),self.tilemap["collision_layer"])
                if tile_id == 1:
                    new_rect = pygame.Rect(((
                        self.position[0]+column*self.tile_size[0]*self.render_size,
                        self.position[1]+row*self.tile_size[1]*self.render_size
                    ),(
                        self.tile_size[0]*self.render_size,
                        self.tile_size[1]*self.render_size
                    )))
                    collision_rects.append(new_rect)
        self.collision_rects = collision_rects
        return collision_rects
    
    def optimize_collision_rects(self):
        """Combines some Rects together in collision_rects to optimize ticks per second"""
        """Planned to implement in v2.0"""
        pass
    
    def get_map_rect(self):
        """Returns a pygame Rect for collision or camera"""
        return pygame.Rect(self.position,(
            self.render_size*self.tile_size[0]*self.map_size[0],
            self.render_size*self.tile_size[1]*self.map_size[1]
        ))

    def get_map_rect_collision(self,rect,movement):
        vx,vy = movement
        test_rect = rect.copy()
        test_rect.move((
            rect.x+vx,
            rect.y+vy
        ))
        return test_rect.collidelist(self.collision_rects)

######################## POSITIONING METHODS #######################

    def reset_position(self):
        """Sets the map's position to a specific position"""
        self.position = self.original_position

    def center(self, surface_size):
        """Centers the position"""
        surface_width, surface_height = surface_size
        map_size = self.get_map_rect().size
        self.set_position((
            surface_width/2-map_size[1]/2,
            surface_height/2-map_size[0]/2
        ))

    def center_x(self, surface_size):
        """Centers the position only by the x position"""
        surface_width, surface_height = surface_size
        map_size = self.get_map_rect().size
        self.set_position((
            surface_width/2-map_size[1]/2,
            self.position[1]
        ))

    def center_y(self, surface_size):
        """Centers the position only by the y position"""
        surface_width, surface_height = surface_size
        map_size = self.get_map_rect().size
        self.set_position((
            self.position[0],
            surface_height/2-map_size[0]/2
        ))

    def set_position(self,position):
        """Sets the map's position to a specific position"""
        self.position = position

    def move(self,vposition):
        """Moves the map from its relative position"""
        self.position = (
            self.position[0]+vposition[0],
            self.position[1]+vposition[1]
        )

######################### RENDERING METHODS ########################

    def pygame_render_chunk(self,surface,map_size,chunk_position,lighting=False):
        """Renders a chunk of a layer of the map"""
        map_surface = pygame.Surface((
            self.tile_size[1]*self.chunk_size[1]*self.render_size,
            self.tile_size[0]*self.chunk_size[0]*self.render_size
        ))

    def pygame_render_layer(self,surface,layer_id,lighting=False):
        """Renders a specific layer of the map"""
        map_surface = pygame.Surface((
            self.tile_size[1]*self.map_size[1]*self.render_size,
            self.tile_size[0]*self.map_size[0]*self.render_size
        ))

        for row in range(self.map_size[0]):
            for column in range(self.map_size[1]):
                tile_id = self.get_tile_id((row,column),layer_id)
                self.tileset.pygame_render(map_surface,(
                    column*self.tile_size[0]*self.render_size,
                    row*self.tile_size[1]*self.render_size
                ),tile_id)
        surface.blit(map_surface,self.position)

    def pygame_render_map(self,surface,lighting=False):
        """Renders the entire map"""
        for layer in range(len(self.tilemap["map_contents"])):
            if layer != self.tilemap["collision_layer"]:
                self.pygame_render_layer(surface,layer)

class entity:
    def __init__(self,position,size,tps=300,map_class=None,render_size=1):
        x,y = position
        width,height = size
        self.position = (x,y)
        self.size = (width,height)
        self.entity_data = {"animation_sprites": {}}
        self.render_size = render_size
        self.tick = 0
        self.tps = tps
        self.map_class = map_class
        self.current_texture = None

        self.original_position = (position[0],position[1])

    def add_entity_data(self, data_name, data_contents):
        self.entity_data[data_name] = data_contents
    
    def remove_entity_data(self, data_name):
        del self.entity_data[data_name]

########################## OPTIONS METHODS #########################

    def set_render_size(self,render_size):
        """Changes the size of the entity when rendering"""
        self.render_size = render_size

    def set_map_class(self,map_class):
        self.map_class = map_class

####################### GET COLLISION METHODS ######################

    def get_rect(self):
        """Returns a pygame Rect for collision"""
        return pygame.Rect(self.position,(
            self.size[0]*self.render_size,
            self.size[1]*self.render_size
        ))

# predict the velocity movement by only 1 pixel, but it also predicts the velocity movement to see if there will be an invisible wall.

    def predict_x_movement(self, vx):
        if self.map_class.get_map_rect_collision(self.get_rect(),(vx,0)) != -1:
            return True
        else: return False

    def predict_y_movement(self, vy):
        if self.map_class.get_map_rect_collision(self.get_rect(),(0,vy)) != -1:
            return True
        else: return False
        
######################## POSITIONING METHODS #######################

    def reset_position(self):
        """Sets the entity's position to a specific position"""
        self.position = self.original_position

    def set_position(self,position):
        """Sets the entity's position to a specific position in pixels"""
        self.position = position
    
    def set_position2(self,position,tilemap):
        """Sets the entity's position to a specific position"""
        self.position = (
            tilemap.position[0]+tilemap.tile_size[0]*tilemap.render_size*position[0],
            tilemap.position[1]+tilemap.tile_size[1]*tilemap.render_size*position[1]
        )

    def center(self, surface_size):
        """Centers the position"""
        surface_width, surface_height = surface_size
        map_size = self.get_map_rect().size
        self.set_position((
            surface_width/2-map_size[0]/2,
            surface_height/2-map_size[1]/2
        ))

    def move(self,vposition,obey_collisions=False):
        """Moves the entity from its relative position in pixels"""
        vx,vy = vposition
        if obey_collisions == False:
            self.position = (self.position[0]+vx,self.position[1]+vy)
        if obey_collisions == True:
            if self.map_class.get_map_rect_collision(self.get_rect(),(vx,vy)) == -1:
                self.position = (self.position[0]+vx,self.position[1]+vy)
            if self.predict_x_movement(vx) and vx > 0: # collision detected
                self.position = (self.position[0]-vx,self.position[1])
            if self.predict_x_movement(vx) and vx < 0: # collision detected
                self.position = (self.position[0]-vx,self.position[1]) 
            if self.predict_y_movement(vy) and vy > 0: # collision detected
                self.position = (self.position[0],self.position[1]-vy)
            if self.predict_y_movement(vy) and vy < 0: # collision detected
                self.position = (self.position[0],self.position[1]-vy)
                
######################## PLACEHOLDER METHODS #######################

    def texture_color_rect(self,color):
        """Returns a Rect of the entity in 1 color"""
        texture = pygame.Surface((
            self.size[0]*self.render_size,
            self.size[1]*self.render_size
        ))
        pygame.draw.rect(texture,color,(
            0,0,
            self.size[0]*self.render_size,
            self.size[1]*self.render_size
        ))
        return texture

    def force_texture_rect(self,color):
        """Forces the texture of the entity to be a pygame Rect"""
        texture = pygame.Surface((
            self.size[0]*self.render_size,
            self.size[1]*self.render_size
        ))
        pygame.draw.rect(texture,color,(
            self.position[0],self.position[1],
            self.size[0]*self.render_size,
            self.size[1]*self.render_size
        ))
        self.current_texture = texture

######################### ANIMATION METHODS ########################

    def set_tps(self,tps):
        """Sets the tps (ticks per second)"""
        self.tps = tps

    def update_animation_tick(self):
        """Updates animation tick"""
        self.tick += 1

    def play_animation(self,animation_dict_name):
        """Starts the animation"""
        number_of_sprites = len(self.entity_data["animation_sprites"][animation_dict_name])
        if self.tick == number_of_sprites*self.tps:
            self.tick = 0
        self.current_texture = self.entity_data["animation_sprites"][str(animation_dict_name)][self.tick//self.tps]
    
    def stop_animation(self):
        """Stops the animation"""
        self.tick = 0
    
    def new_animation_data(self,name,data):
        """Stores the entity's sprite information. Inside the data variable should be a list of the sprite images in order"""
        self.entity_data["animation_sprites"][str(name)] = data

######################### RENDERING METHODS ########################

    def pygame_render(self,surface):
        """Renders the entity's sprite"""
        surface.blit(self.current_texture,self.position)