import pygame

class tileset:
    def __init__(self, textures, tile_size, tiles_distance=0):
        self.textures = pygame.image.load(textures)
        self.tile_size = tile_size
        self.tiles_distance = tiles_distance
        self.tileset_size = (
            int((self.textures.get_size())[0]/self.tile_size[0]), 
            int((self.textures.get_size())[1]/self.tile_size[1])
        )
    def get_tile_id_pos(self, tile_id):
        if (self.tileset_size[0]*self.tileset_size[1]) > tile_id:
            return (
                int(tile_id%(self.tileset_size)[0]), 
                int(tile_id/(self.tileset_size)[0])
            )
    def pygame_render(self, tile_id, render_size=1):
        """Returns an image of a tile. tile_id can never be 0"""
        if tile_id != 0:
            tile_id = tile_id - 1
            tile = pygame.Surface(self.tile_size)
            tile.blit(self.textures, (0, 0), (
                self.tile_size[0]*(self.get_tile_id_pos(tile_id))[0], 
                self.tile_size[1]*(self.get_tile_id_pos(tile_id))[1],
                self.tile_size[0], 
                self.tile_size[1]
            ))
            tile = pygame.transform.scale(tile, (
                self.tile_size[0]*render_size, 
                self.tile_size[1]*render_size
            ))
            return tile
        else:
            return pygame.Surface(self.tile_size)


class tiledmap:
    def __init__(self, map_size, tileset_class, chunk_size=(5,5)):
        self.tileset = tileset_class

        self.tile_size = tileset_class.tile_size
        self.map_size = (map_size[1], map_size[0])
        self.chunk_size = chunk_size
        self.tilemap = {
            #map_contents[layer_number][row][column]
            "map_contents": [[[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])]]
        }
        self.map_textures_path = tileset_class.textures
    def modify_tile(self, location, tile_id, layer_id=0):
        """Changes a tile ID texture"""
        row, column = location
        self.tilemap["map_contents"][layer_id][row][column] = tile_id
    def get_tile_id(self, location, layer):
        row, column = location
        return self.tilemap["map_contents"][layer][row][column]
    def get_layer_count(self):
        return len(self.tilemap["map_contents"])
    def save(self, file_path, file_name):
        """Saves the map into a file"""
        pass
    def pygame_render_chunk(self, chunk_location, render_size=1, lighting=False):
        """Renders a chunk of a layer of the map"""
        surface = pygame.Surface((
            self.tile_size[0]*self.chunk_size[0]*render_size,
            self.tile_size[1].tile_size[1]()*self.chunk_size[1]*render_size
        ))
    def pygame_render_layer(self, layer_id, render_size=1):
        """Renders a specific layer of the map"""
        surface = pygame.Surface((
            self.tile_size[0]*(self.map_size)[0]*render_size,
            self.tile_size[1]*(self.map_size)[1]*render_size
        ))
        try:
            for row in range((self.map_size)[0]+1):
                for column in range((self.map_size)[1]+1):
                    tile_id = self.get_tile_id((row, column), layer_id)
                    surface.blit(
                        self.tileset.pygame_render(tile_id, render_size=render_size), 
                        (
                            column*self.tile_size[0], 
                            row*self.tile_size[1]
                        ))
        except IndexError:
            return surface
    def pygame_render_map(self, render_size=1, lighting=False):
        """Renders the whole map"""
        surface = pygame.Surface((
            self.tile_size[0]*(self.map_size)[0]*render_size,
            self.tile_size[1]*(self.map_size)[1]*render_size
        ))
        for layer in range(self.get_layer_count()):
            surface.blit(
                pygame_render_layer(layer, render_size=1, lighting=lighting),
                (0,0)
            )
        return surface
    def test_for_collusions(self, hitbox):
        """Tests for collusions if the hitbox is inside a wall."""
        x1,y1,x2,y2 = hitbox