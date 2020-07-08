import pygame
import json

def convert_tiledjson(path, collision_layer: int = None, invisible_layers: list = []):
    """Converts a tiled json map in GameDen's formatting"""
    with open(path, 'r') as file:
        loaded_json = json.load(file)

    contents = []
    for layer in range(len(loaded_json["layers"])):
        json_contents = loaded_json["layers"][layer]["data"]
        n = loaded_json["width"]
        layer_contents = [json_contents[i * n:(i + 1) * n] for i in range((len(json_contents) + n - 1) // n )]
        contents.append(layer_contents)
    tilemap = {
        #contents[layer_number][row][column]
        "contents": contents,
        "collision_layer": collision_layer,
        "invisible_layers": invisible_layers
    }
    return tilemap

class tileset:
    def __init__(self,textures_path,tile_size,tiles_distance=0):
        self.textures = pygame.image.load(textures_path)
        self.tile_size = tile_size
        self.tiles_distance = tiles_distance
        self.tileset_size = (
            int((self.textures.get_size())[0]/self.tile_size[0]),
            int((self.textures.get_size())[1]/self.tile_size[1])
        )

    def get_tile_id_pos(self,tile_id: int) -> tuple:
        """Returns the position of the inputed tile ID"""
        if (self.tileset_size[0]*self.tileset_size[1]) > tile_id:
            return (
                int(tile_id%(self.tileset_size)[0]),
                int(tile_id/(self.tileset_size)[0])
            )

    def pygame_render(self,position: tuple, surface, tile_id: int, render_size: int = 1):
        """Renders an image of a tile. tile_id can never be 0"""
        t_width, t_height = self.tile_size
        if tile_id != 0:
            tile_id = tile_id - 1

            # cropping
            tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
            tile = tile.convert_alpha()
            t_x, t_y = self.get_tile_id_pos(tile_id)
            tile.blit(self.textures,(0,0),(
                t_width*t_x, t_height*t_y,
                t_width, t_height
            ))

            # resizing to fit render_size
            tile = pygame.transform.scale(tile,(
                int(t_width*render_size),
                int(t_height*render_size)
            ))

            surface.blit(tile,position)

    def pygame_render2(self, tile_id: int, render_size=1):
        """Returns an image of a tile. tile_id can never be 0"""
        tile = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32)
        tile = tile.convert_alpha()
        if tile_id != 0:
            self.pygame_render(tile, (0,0), tile_id, render_size=render_size)
            return tile
        else: return tile

class tilemap:
    def __init__(self, map_data: dict, tileset):
        self.map_data = map_data
        map_contents = self.map_data["contents"]
        self.map_size = (len(map_contents[0][0]), len(map_contents[0]))
    
        self.tileset = tileset
        self.tile_size = tileset.tile_size
        self.textures = tileset.textures

    def get_position_by_px(self, position: tuple) -> tuple:
        x_px, y_px = position
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size

        return (
            (t_width*m_width-x_px)/m_width,
            (t_height*m_width-y_px)/m_height
        )

    def get_tile_id(self, position: tuple, layer: int) -> int:
        row,column = position
        try: return self.map_data["contents"][layer][row][column]
        except TypeError:
            raise Exception(f"tile location doesn't exist ({row}, {column})")

    def get_collision_rects(self, layer: int, render_size: int = 1) -> list:
        """Returns a list of pygame Rects from a layer from the specified position"""
        collision_rects = []
        x, y == self.position
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size

        for row in range(m_height):
            for column in range(m_width):
                tile_id = self.get_tile_id((row,column),layer)
                if tile_id != 0:
                    collision_rects.append(pygame.Rect(((
                        x+column*t_width*render_size,
                        y+row*t_height*render_size
                    ),(
                        t_width*render_size,
                        t_height*render_size
                    ))))
        if layer == self.map_data["collision_layer"]: 
            self.collision_rects = collision_rects
        return collision_rects

    def set_position(self, new_position):
        self.rect.x, self.rect.y = new_position

    def create_new_layer(self):
        self.tilemap["contents"].append([[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])])
    
    def pygame_render_layer(self, position, surface, layer_id: int, render_size: int = 1):
        t_width, t_height = self.tile_size
        m_width, m_height = self.map_size
        map_surface = pygame.Surface((
            t_width*m_width*render_size,
            t_height*m_height*render_size
        ), pygame.SRCALPHA, 32)
        map_surface = map_surface.convert_alpha()
        
        for row in range(m_height):
            for column in range(m_width):
                tile_id = self.get_tile_id((row,column),layer_id)
                self.tileset.pygame_render((
                    column*t_width*render_size,
                    row*t_height*render_size
                ), map_surface, tile_id, render_size=render_size)

        surface.blit(map_surface,position)

    def pygame_render_map(self, position, surface, render_size: int = 1):
        for layer in range(len(self.map_data["contents"])):
            if layer not in self.map_data["invisible_layers"]:
                self.pygame_render_layer(position,surface,layer,render_size=render_size)