import pygame

class tileset:
    def __init__(self, tile_textures, tile_size, tiles_distance=0):
        self.tile_textures = tile_textures
        self.width, self.height = tile_size
        self.tiles_distance = tiles_distance
    def get_textures_path(self):
        return self.tile_textures
    def get_width():
        return self.width
    def get_height():
        return self.height
    def pygame_render(self, tile_id):
        """Returns an image of a tile"""
        pass

class tiledmap:
    def __init__(self, map_options, chunk_size=(5,5)):
        map_size, tileset_class = map_options
        tilemap_template = {
            "map_contents": [[]] #map_contents[layer_number][row][column]
        }
        self.tile_width = tileset_class.get_width()
        self.tile_height = tileset_class.get_height()
        self.rows, self.columns = map_size
        self.tilemap = tilemap_template
        self.map_textures_path = tileset_class.get_textures_path()
        self.chunk_width, self.chunk_height = chunk_size
        row_template = []
        for column in range(self.columns):
            row_template.append(0)
        for row in range(self.rows):
            self.tilemap["map_contents"][0].append(row_template.copy())
    def modify_tile(self, location, tile_id, layer_id=0):
        """Changes a tile ID texture"""
        row, column = location
        self.tilemap["map_contents"][layer_id][row][column] = tile_id
    def get_tile_id(self, location, layer):
        row, column = location
        return self.tilemap["map_contents"][layer][row][column]
    def get_layer_count(self):
        return len(self.tilemap["map_contents"])
    def get_rows(self):
        return len(self.tilemap["map_contents"][0])
    def get_columns(self):
        return len(self.tilemap["map_contents"][0][0])
    def get_chunk_width(self):
        return self.chunk_width
    def get_chunk_height(self):
        return self.chunk_height
    def get_tilemap(self):
        return self.tilemap
    def save(self, file_path, file_name):
        """Saves the map into a file"""
        pass
    def pygame_render_chunk(self, chunk_location, render_size=1, lighting=False):
        """Renders a chunk of a layer of the map"""
        surface = pygame.Surface((
            tileset_class.get_width()*self.get_chunk_width()*render_size,
            tileset_class.get_height()*self.get_chunk_height()*render_size
        ))
    def pygame_render_layer(self, layer_id, render_size=1, lighting=False):
        """Renders a specific layer of the map"""
        surface = pygame.Surface((
            tileset_class.get_width()*self.get_columns()*render_size,
            tileset_class.get_height()*self.get_rows()*render_size
        ))

        for row in range(self.get_rows()):
            for column in range(self.get_columns()):
                tile_id = self.get_tile_id((row, column), layer_id)
                surface.blit(
                    tileset_class.pygame_render(tile_id), 
                    (column*tileset_class.get_width(), row*tileset_class.get_height())
                )
        return surface
    def pygame_render_map(self, render_size=1, lighting=False):
        """Renders the whole map"""
        surface = pygame.Surface((
            tileset_class.get_width()*self.get_columns()*render_size,
            tileset_class.get_height()*self.get_rows()*render_size
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