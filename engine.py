#######################################################
#    GAME DEN ENGINE v1.0 (2020)                      #
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
    def __init__(self, map_size, tileset_class, render_size=1, chunk_size=(5,5)):
        self.tileset = tileset_class
        self.tile_size = tileset_class.tile_size
        self.map_size = (map_size[1], map_size[0])
        self.chunk_size = chunk_size
        self.map_textures_path = tileset_class.textures
        self.render_size = render_size
        self.tilemap = {
            #map_contents[layer_number][row][column]
            "map_contents": [[[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])]],
            "collision_layer": 0
        }

    def load_map(self, map_contents):
        """Load a pre-made map"""
        self.tilemap = map_contents

    def modify_layer(self, location, tile_id, layer_id=0):
        """Changes a tile ID texture"""
        row, column = location
        if layer_id != self.tilemap["collision_layer"]:
            self.tilemap["map_contents"][layer_id][row][column] = tile_id
        if layer_id == self.tilemap["collision_layer"]:
            self.tilemap["map_contents"][layer_id][row][column] = 1

    def add_new_layer(self):
        """Adds a new layer with an empty multidimensional array"""
        self.tilemap["map_contents"].append([[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])])

########################## OPTIONS METHODS #########################

    def set_render_size(self, render_size):
        self.render_size = render_size

############################ GET METHODS ###########################

    def get_tile_id(self, location, layer):
        """Returns a tile ID from the specified location"""
        row, column = location
        return self.tilemap["map_contents"][layer][row][column]

    def get_collision_rects(self):
        """Returns a list of pygame Rects from the collision layer"""
        collision_rects = []
        try:
            for row in range(self.map_size[0]+1):
                for column in range(self.map_size[1]+1):
                    new_rect = pygame.Rect(((
                        column*self.tile_size[0]*self.render_size, 
                        row*self.tile_size[1]*self.render_size
                    ),(
                        self.tile_size[0]*self.render_size, 
                        self.tile_size[1]*self.render_size
                    )))
                    collision_rects.append(new_rect)
        except IndexError:
            return collision_rects

########################### RENDER METHODS ##########################

    def pygame_render_chunk(self, chunk_location, lighting=False):
        """Renders a chunk of a layer of the map"""
        surface = pygame.Surface((
            self.tile_size[0]*self.chunk_size[0]*self.render_size,
            self.tile_size[1]*self.chunk_size[1]*self.render_size
        ))

    def pygame_render_layer(self, layer_id):
        """Renders a specific layer of the map"""
        surface = pygame.Surface((
            self.tile_size[0]*self.map_size[0]*self.render_size,
            self.tile_size[1]*self.map_size[1]*self.render_size
        ))
        try:
            for row in range(self.map_size[0]+1):
                for column in range(self.map_size[1]+1):
                    tile_id = self.get_tile_id((row, column), layer_id)
                    surface.blit(
                        self.tileset.pygame_render(tile_id), (
                            column*self.tile_size[0]*self.render_size, 
                            row*self.tile_size[1]*self.render_size
                        ))
        except IndexError:
            return surface

    def pygame_render_map(self, lighting=False):
        """Renders the whole map"""
        surface = pygame.Surface((
            self.tile_size[0]*self.map_size[0]*self.render_size,
            self.tile_size[1]*self.map_size[1]*self.render_size
        ))
        for layer in range(len(self.tilemap["map_contents"])):
            if layer != self.tilemap["collision_layer"]:
                surface.blit(
                    self.pygame_render_layer(layer),
                    (0,0)
                )
        return surface