import pygame

class tileset:
    def __init__(self, tile_textures, tile_size, tiles_distance=0):
        pass
    def get_textures_path(self):
        pass
    def get_width():
        pass
    def get_height():
        pass
    def pygame_render(self, tile_id):
        pass

class tiledmap:
    def __init__(self, map_options):
        map_size, tileset_class = map_options
        tilemap_template = {
            "map_contents": [[]] #map_contents[layer_number][row][column]
        }
        self.tile_width = tileset_class.get_width()
        self.tile_height = tileset_class.get_height()
        self.rows, self.columns = map_size
        self.tilemap = tilemap_template
        self.map_textures_path = tileset_class.get_textures_path()
        row_template = []
        for column in range(self.columns):
            row_template.append(0)
        for row in range(self.rows):
            self.tilemap["map_contents"][0].append(row_template.copy())
    def modify_tile(self, location, tile_id, layer_id=0):
        """Changes a tile ID"""
        row, column = location
        self.tilemap["map_contents"][layer_id][row][column] = tile_id
    def get_name(self):
        return self.tilemap["name"]
    def get_layers(self):
        return len(self.tilemap["map_contents"])
    def get_rows(self):
        return len(self.tilemap["map_contents"][0])
    def get_columns(self):
        return len(self.tilemap["map_contents"][0][0])
    def get_tilemap(self):
        return self.tilemap
    def save(self, file_path, file_name):
        """Saves the map into a file"""
        pass
    def pygame_render_chunk(self, chunk_location):
        """Renders a section of a layer of the map"""
        pass
    def pygame_render_layer(self, layer_id, lighting=False):
        """Renders a specific layer of the map"""
        surface = pygame.Surface((100,100))

        for row in range(self.get_rows()):
            for column in range(self.get_columns()):
                tileTexture = "something"
                location = (column*tilemap.tilesize, row*tilemap.tilesize)
                surface.blit(texture, location)
        return surface
    def pygame_render(self, lighting=False):
        """Renders the whole map"""
        surface = pygame.Surface((100,100))
        for layer in range(self.get_layers()):
            pygame_render(location, layer, lighting=lighting)
    def test_for_collusions(self, hitbox):
        """Tests for collusions if the hitbox is inside a wall."""
        x1,x2,y1,y2 = hitbox