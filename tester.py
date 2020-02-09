import pymap

tile_map = pymap.tiled("map", (3,4))
print(tile_map.get_tilemap())
tile_map.modify_tile((0,0),1)
print(tile_map.get_tilemap())
print(tile_map.get_name(), tile_map.get_rows(), tile_map.get_columns())