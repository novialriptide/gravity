import pygame

class tileset:
    def __init__(self, tile_textures, tile_size, tiles_distance=0):
        self.tile_textures = pygame.image.load(tile_textures)
        self.tile_size = tile_size
        self.tiles_distance = tiles_distance
    def get_textures_path(self):
        return self.tile_textures
    def get_tile_size(self):
        return self.tile_size
    def get_tileset_size(self):
        return (
            int((self.tile_textures.get_size())[0]/self.tile_size[0]), 
            int((self.tile_textures.get_size())[1]/self.tile_size[1])
        )
    def get_tile_id_pos(self, tileID):
        if (self.get_tileset_size())[0]*(self.get_tileset_size()[1]) > tileID:
            return (
                int(tileID%(self.get_tileset_size())[0]), 
                int(tileID/(self.get_tileset_size())[0])
            )
    def pygame_render(self, tile_id):
        """Returns an image of a tile"""
        tile = pygame.Surface(self.tile_size)
        tile.blit(self.tile_textures, (0, 0), (30, 30, self.tile_size[0], self.tile_size[1]))

class tiledmap:
    def __init__(self, map_size, tileset_class, chunk_size=(5,5)):
        self.tileset = tileset_class

        self.tile_size = tileset_class.get_tile_size()
        self.map_size = (map_size[1], map_size[0])
        self.chunk_size = chunk_size
        self.tilemap = {
            #map_contents[layer_number][row][column]
            "map_contents": [[[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])]]
        }
        self.map_textures_path = tileset_class.get_textures_path()
    def modify_tile(self, location, tile_id, layer_id=0):
        """Changes a tile ID texture"""
        row, column = location
        self.tilemap["map_contents"][layer_id][row][column] = tile_id
    def get_tile_id(self, location, layer):
        row, column = location
        return self.tilemap["map_contents"][layer][row][column]
    def get_layer_count(self):
        return len(self.tilemap["map_contents"])
    def get_map_size(self):
        return (len(self.tilemap["map_contents"][0]), len(self.tilemap["map_contents"][0][0]))
    def get_chunk_size(self):
        return self.chunk_size
    def get_tilemap(self):
        return self.tilemap
    def save(self, file_path, file_name):
        """Saves the map into a file"""
        pass
    def pygame_render_chunk(self, chunk_location, render_size=1, lighting=False):
        """Renders a chunk of a layer of the map"""
        surface = pygame.Surface((
            self.tile_size[0]*self.get_chunk_width()*render_size,
            self.tile_size[1].get_height()*self.get_chunk_height()*render_size
        ))
    def pygame_render_layer(self, layer_id, render_size=1, lighting=False):
        """Renders a specific layer of the map"""
        surface = pygame.Surface((
            self.tile_size[0]*(self.get_map_size())[0]*render_size,
            self.tile_size[1]*(self.get_map_size())[1]*render_size
        ))
        for row in range((self.get_map_size())[0]):
            for column in range((self.get_map_size())[1]):
                tile_id = self.get_tile_id((row, column), layer_id)
                #surface.blit(
                #    self.tileset.pygame_render(tile_id), 
                #    (column*self.tile_size[0], row*self.tile_size[1])
                #)
        return surface
    def pygame_render_map(self, render_size=1, lighting=False):
        """Renders the whole map"""
        surface = pygame.Surface((
            self.tile_size[0]*(self.get_map_size())[0]*render_size,
            self.tile_size[1]*(self.get_map_size())[1]*render_size
        ))
        for layer in range(self.get_layer_count()):
            surface.blit(
                pygame_render(location, layer, render_size=1, lighting=lighting),
                (0,0)
            )
        return surface
    def test_for_collusions(self, hitbox):
        """Tests for collusions if the hitbox is inside a wall."""
        x1,x2,y1,y2 = hitbox