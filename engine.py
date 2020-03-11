#######################################################
#    GAME DEN ENGINE v1.0 (2020)                      #
#    tileset, tiledmap, physics, entity               #
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

    def pygame_render(self, tile_id):
        """Returns an image of a tile. tile_id can never be 0"""
        if tile_id != 0:
            tile_id = tile_id - 1
            tile = pygame.Surface(self.tile_size)
            tile_pos = self.get_tile_id_pos(tile_id)
            tile.blit(self.textures, (0, 0), (
                self.tile_size[0]*tile_pos[0], 
                self.tile_size[1]*tile_pos[1],
                self.tile_size[0], 
                self.tile_size[1]
            ))
            tile = pygame.transform.scale(tile, (
                self.tile_size[0]*self.render_size, 
                self.tile_size[1]*self.render_size
            ))
            return tile
        else:
            return pygame.Surface(self.tile_size)

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

####################### GET COLLISION METHODS ######################

    def get_collision_rects(self):
        """Returns a list of pygame Rects from the collision layer from the specified position"""
        collision_rects = []
        try:
            for row in range(self.map_size[0]+1):
                for column in range(self.map_size[1]+1):
                    tile_id = self.get_tile_id((row, column), self.tilemap["collision_layer"])
                    if tile_id == 1:
                        new_rect = pygame.Rect(((
                            self.position[0]*column*self.tile_size[0]*self.render_size, 
                            self.position[1]*row*self.tile_size[1]*self.render_size
                        ),(
                            self.tile_size[0]*self.render_size, 
                            self.tile_size[1]*self.render_size
                        )))
                        collision_rects.append(new_rect)
        except IndexError:
            return collision_rects
    
    def get_map_border_rect(self):
        """Returns a pygame Rect for collision or camera from the specified position"""
        return pygame.Rect(self.position, (
            self.render_size*self.tile_size[0]*self.map_size[0],
            self.render_size*self.tile_size[1]*self.map_size[1]
        ))

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
                    map_surface.blit(
                        self.tileset.pygame_render(tile_id), (
                            column*self.tile_size[0]*self.render_size, 
                            row*self.tile_size[1]*self.render_size
                    ))
        except IndexError:
            surface.blit(map_surface, self.position)

    def pygame_render_map(self, surface, lighting=False):
        """Renders the whole map"""
        for layer in range(len(self.tilemap["map_contents"])):
            if layer != self.tilemap["collision_layer"]:
                self.pygame_render_layer(surface, layer)

class physics:
    def get_map_rect_collision(self, rect, rects, movement):
        rect.move((
            rect.x+movement[0],
            rect.y+movement[1]
        ))
        if rect.collidelist(rects):
            return True

class entity:
    def __init__(self, position, size, texture=None, render_size=1):
        self.position = (position[0], position[1])
        self.size = (size[0], size[1])
        self.entity_data = {}
        self.texture = texture
        self.render_size = render_size
        self.frame = 0

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
        self.position = (self.position[0]+vx, self.position[1]+vy)

######################### ANIMATION METHODS ########################

    def set_frame(self, frame):
        self.frame = frame

    def set_animation(self, animation_id):
        pass

######################### RENDERING METHODS ########################

    def pygame_render(self, surface):
        """Renders the entity's sprite"""
        pass
