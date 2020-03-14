#######################################################
#    GAME DEN ENGINE v1.0 (2020)                      #
#    tileset, tiledmap, entity                        #
#    DEVELOPED BY: ANDREW HONG                        #
#######################################################
import pygame

class tileset:
    def __init__(self, textures, tile_size, render_size=1, tiles_distance=0):
        self.textures = pygame.image.load(textures)
        self.tile_size = tile_size
        self.tiles_distance = tiles_distance
        self.render_size = render_size
        self.tileset_size = (
            int((self.textures.get_size())[0]/self.tile_size[0]), 
            int((self.textures.get_size())[1]/self.tile_size[1])
        )

    def get_tile_id_pos(self, tile_id):
        """Returns the position of the inputed tile ID"""
        if (self.tileset_size[0]*self.tileset_size[1]) > tile_id:
            return (
                int(tile_id%(self.tileset_size)[0]), 
                int(tile_id/(self.tileset_size)[0])
            )

    def set_render_size(self, render_size):
        """Changes the size of the tile when rendering"""
        self.render_size = render_size

    def pygame_render(self, surface, position, tile_id):
        """Returns an image of a tile. tile_id can never be 0"""
        if tile_id != 0:
            tile_id = tile_id - 1
            tile = pygame.Surface(self.tile_size)
            tile_pos = self.get_tile_id_pos(tile_id)
            tile.blit(self.textures, (0, 0), (
                self.tile_size[0]*tile_pos[0], 
                self.tile_size[1]*tile_pos[1],
                self.tile_size[0], self.tile_size[1]
            ))
            tile = pygame.transform.scale(tile, (
                self.tile_size[0]*self.render_size, 
                self.tile_size[1]*self.render_size
            ))
            surface.blit(tile, position)

class tiledmap:
    def __init__(self, map_size, tileset_class, position, render_size=1, chunk_size=(5,5)):
        self.tileset = tileset_class
        self.tile_size = tileset_class.tile_size
        self.map_size = (map_size[1], map_size[0])
        self.chunk_size = chunk_size
        self.map_textures_path = tileset_class.textures
        self.render_size = render_size
        self.position = position
        self.original_position = position
        self.collision_rects = []
        self.tilemap = {
            #map_contents[layer_number][row][column]
            "map_contents": [[[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])]],
            "collision_layer": 0
        }

    def load_map(self, map_contents):
        """Load a pre-made map"""
        self.tilemap = map_contents

########################## OPTIONS METHODS #########################

    def set_render_size(self, render_size):
        """Changes the size of the map when rendering"""
        self.render_size = render_size

########################### LAYER METHODS ##########################

    def modify_layer(self, position, tile_id, layer_id=0):
        """Changes a tile ID texture"""
        row, column = position
        if layer_id != self.tilemap["collision_layer"]:
            self.tilemap["map_contents"][layer_id][row][column] = tile_id
        if layer_id == self.tilemap["collision_layer"]:
            self.tilemap["map_contents"][layer_id][row][column] = 1

    def add_new_layer(self):
        """Adds a new layer with an empty multidimensional array"""
        self.tilemap["map_contents"].append([[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])])

############################ GET METHODS ###########################

    def get_tile_id(self, position, layer):
        """Returns a tile ID from the specified position"""
        row, column = position
        return self.tilemap["map_contents"][layer][row][column]

####################### GET/COLLISION METHODS ######################

    def generate_collision_rects(self):
        """Returns a list of pygame Rects from the collision layer from the specified position"""
        collision_rects = []
        try:
            for row in range(self.map_size[0]+1):
                for column in range(self.map_size[1]+1):
                    tile_id = self.get_tile_id((row, column), self.tilemap["collision_layer"])
                    if tile_id == 1:
                        new_rect = pygame.Rect(((
                            self.position[0]+column*self.tile_size[0]*self.render_size, 
                            self.position[1]+row*self.tile_size[1]*self.render_size
                        ),(
                            self.tile_size[0]*self.render_size, 
                            self.tile_size[1]*self.render_size
                        )))
                        collision_rects.append(new_rect)
        except IndexError:
            self.collision_rects = collision_rects
            return collision_rects
    
    def optimize_collision_rects(self):
        """Combines some Rects together in collision_rects to optimize frames per second"""
        pass
    
    def get_map_border_rect(self):
        """Returns a pygame Rect for collision or camera from the specified position"""
        return pygame.Rect(self.position, (
            self.render_size*self.tile_size[0]*self.map_size[0],
            self.render_size*self.tile_size[1]*self.map_size[1]
        ))

    def get_map_rect_collision(self, rect, movement):
        vx, vy = movement
        test_rect = rect.copy()
        test_rect.move((
            rect.x+vx,
            rect.y+vy
        ))
        print(rect.x+vx,rect.y+vy)
        self.generate_collision_rects()
        return test_rect.collidelist(self.collision_rects)

######################## POSITIONING METHODS #######################

    def reset_position(self):
        """Sets the map's position to a specific position"""
        self.position = self.original_position

    def set_position(self, position):
        """Sets the map's position to a specific position"""
        self.position = position

    def move(self, vposition):
        """Moves the map from its relative position"""
        self.position = (
            self.position[0]+vposition[0],
            self.position[1]+vposition[1]
        )

######################### RENDERING METHODS ########################

    def pygame_render_chunk(self, surface, chunk_position, lighting=False):
        """Renders a chunk of a layer of the map"""
        map_surface = pygame.Surface((
            self.tile_size[0]*self.chunk_size[0]*self.render_size,
            self.tile_size[1]*self.chunk_size[1]*self.render_size
        ))

    def pygame_render_layer(self, surface, layer_id, lighting=False):
        """Renders a specific layer of the map"""
        map_surface = pygame.Surface((
            self.tile_size[0]*self.map_size[0]*self.render_size,
            self.tile_size[1]*self.map_size[1]*self.render_size
        ))
        try:
            for row in range(self.map_size[0]+1):
                for column in range(self.map_size[1]+1):
                    tile_id = self.get_tile_id((row, column), layer_id)
                    self.tileset.pygame_render(map_surface, (
                        column*self.tile_size[0]*self.render_size, 
                        row*self.tile_size[1]*self.render_size
                    ), tile_id)
        except IndexError:
            surface.blit(map_surface, self.position)

    def pygame_render_map(self, surface, lighting=False):
        """Renders the whole map"""
        for layer in range(len(self.tilemap["map_contents"])):
            if layer != self.tilemap["collision_layer"]:
                self.pygame_render_layer(surface, layer)

class entity:
    def __init__(self, position, size, fps=3, map_class=None, render_size=1):
        x, y = position
        width, height = size
        self.position = (x, y)
        self.size = (width, height)
        self.entity_data = {}
        self.render_size = render_size
        self.frame = 0
        self.fps = fps
        self.map_class = map_class
        self.current_texture = None

        self.original_position = (position[0], position[1])

########################## OPTIONS METHODS #########################

    def set_render_size(self, render_size):
        """Changes the size of the entity when rendering"""
        self.render_size = render_size

####################### GET COLLISION METHODS ######################

    def get_rect(self):
        """Returns a pygame Rect for collision"""
        return pygame.Rect(self.position, (
            self.size[0]*self.render_size,
            self.size[1]*self.render_size
        ))
        
######################## POSITIONING METHODS #######################

    def reset_position(self):
        """Sets the entity's position to a specific position"""
        self.position = self.original_position

    def set_position(self, position):
        """Sets the entity's position to a specific position"""
        self.position = position

    def move(self, vposition, obey_collisions=False):
        """Moves the entity from its relative position"""
        vx, vy = vposition
        if obey_collisions == False:
            self.position = (self.position[0]+vx, self.position[1]+vy)
        if obey_collisions == True:
            if self.map_class.get_map_rect_collision(self.get_rect(), (vx, vy)):
                self.position = (self.position[0]+vx, self.position[1]+vy)

######################## PLACEHOLDER METHODS #######################

    def force_texture_rect(self, color):
        """Forces the texture of the entity to be a pygame Rect"""
        texture = pygame.Surface((
            self.size[0]*self.render_size,
            self.size[1]*self.render_size
        ))
        pygame.draw.rect(texture, color, (
            self.position[0], self.position[1], 
            self.size[0]*self.render_size, 
            self.size[1]*self.render_size
        ))
        self.current_texture = texture

######################### ANIMATION METHODS ########################

    def set_frame(self, frame):
        """Sets the animation timeline"""
        self.frame = frame

    def set_fps(self, fps):
        self.fps = fps

    def play_animation(self, animation_name):
        pass
    
    def set_animation_data(self, payload):
        """Stores the entity's sprite"""
        self.entity_data["animation_sprites"] = payload

######################### RENDERING METHODS ########################

    def pygame_render(self, surface):
        """Renders the entity's sprite"""
        surface.blit(self.current_texture, self.position)