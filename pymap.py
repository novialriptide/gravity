import pygame

class tiled:
    def __init__(self, map_name, map_size, map_textures_path):
        tilemap_template = {
            "name": None,
            "map_contents": [[]] #map_contents[layer_number][row][column]
        }
        self.rows, self.columns = map_size
        self.tilemap = tilemap_template
        self.tilemap["name"] = map_name
        self.map_textures_path = map_textures_path
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
    def save(self, file_path):
        """Saves the map into a file"""
        pass
    def pygame_render(self, location, surface, lighting=False):
        """Renders the whole map"""
        for layer in range(self.get_layers()):
            pygame_render(location, pygame_window, layer, lighting=lighting)
    def pygame_render(self, location, surface, layer_id, lighting=False):
        """Renders a specific layer"""
        for row in range(self.get_rows):
            for column in range(self.get_columns):
                window.blit(
                    tilemap.textures[tilemap.tilemap[row][column]], 
                    (column*tilemap.tilesize, row*tilemap.tilesize)
                )
    def test_for_collusions(self, hitbox):
        """Tests for collusions if the hitbox is inside a wall."""
        x1,x2,y1,y2 = hitbox