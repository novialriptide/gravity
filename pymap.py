import pygame

class tiled:
    def __init__(self, map_name, map_size):
        tilemap_template = {
            "name": None,
            "map_contents": [[]] #map_contents[layer_number][row][column]
        }
        self.rows, self.columns = map_size
        self.tilemap = tilemap_template
        self.tilemap["name"] = map_name
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
    def get_rows(self):
        return len(self.tilemap["map_contents"][0])
    def get_columns(self):
        return len(self.tilemap["map_contents"][0][0])
    def get_tilemap(self):
        return self.tilemap
    def save(self):
        pass
    def render(self):
        """Renders the whole map"""
        pass
    def render(self, layer_id):
        """Renders a specific layer"""
        pass