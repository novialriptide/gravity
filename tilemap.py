import pygame

class tilemap:
    def __init__(self,map_data,tileset,render_size=1):
        self.map_data = map_data
        self.map_contents = self.map_data["contents"]
        self.map_size = (len(self.map_contents[0][0]), len(self.map_contents[0]))

        self.render_size = render_size
    
        self.tileset = tileset
        self.tile_size = tileset.tile_size
        self.textures = tileset.textures

    @property
    def rect(self):
        x, y = self.position[0], self.position[1]
        width, height = self.map_size
        return pygame.Rect(x, y, width*self.render_size, height*self.render_size)
    
    @property
    def position(self):
        pass

    def get_tile_id(self, layer):
        pass

    def get_collision_rects(self, layer):
        """Returns a list of pygame Rects from a layer from the specified position"""
        collision_rects = []
        x,y == self.position
        tile_width, tile_height = self.tile_size

        for row in range(self.map_size[1]):
            for column in range(self.map_size[0]):
                tile_id = self.get_tile_id((row,column),layer)
                if tile_id != 0:
                    collision_rects.append(pygame.Rect(((
                        x+column*tile_width*self.render_size,
                        y+row*tile_height*self.render_size
                    ),(
                        tile_width*self.render_size,
                        tile_height*self.render_size
                    ))))
        if layer == self.tilemap["collision_layer"]: 
            self.collision_rects = collision_rects
        return collision_rects

    def create_new_layer(self):
        """Adds a new layer with an empty multidimensional array"""
        self.tilemap["contents"].append([[0 for j in range(self.map_size[0])] for i in range(self.map_size[1])])

    def pygame_render(self,position,layer=-1):
        if layer == -1:
            # render whole map
        if layer >= 0:
            # render a single layer