import items
import enemies
import tiles
import player
import json

_world = {}
starting_position = (0,0)
world_size = (0,0)
_items = []
_enemies = []

def load_tiles(level = "level_1"):
  """
  This function loads a reference text file to build the world.
  This can be called each time the player advances levels to trigger a new map.
  Map is a list structure of 1-letter references to rooms:
    S = Starting room (1 per map)
    E = Enemy room
    T = Trap room
    L = Loot room
    X = Empty room
    H = Hidden room
    D = Dungeon exit
    I:***** - Specific item room (must specify name of item after colon)
    B:***** - Boss / specific enemy room (must specify name of enemy after colon)
  """
  global world_size
  world_size_x, world_size_y = world_size
      
  
  tile_list = {'S':"StartingRoom",
               'E':"EnemyRoom",
               'H':"HiddenRoom",
               'L':"LootRoom",
               'X':"EmptyRoom",
               'D':"DungeonEnd",
               'I':"LootRoom",
               'B':"EnemyRoom"}

  with open('resources/map_%s.json'%level,'r') as _map:
    _map_json = json.load(_map)
  
  global _items
  _items = _map_json['items']
  global _enemies
  _enemies = _map_json['enemies']

  global _world
  global starting_position
  for room in _map_json['rooms']:
    
    if room['kwargs']['x'] > world_size_x: world_size_x = room['kwargs']['x']
    if room['kwargs']['y'] > world_size_y: world_size_y = room['kwargs']['y']
    if room['tile'].lower() == "StartingRoom".lower():  starting_position = (room['kwargs']['x'], room['kwargs']['y'])
    _world[(room['kwargs']['x'],room['kwargs']['y'])] = getattr(__import__('tiles'),room['tile'])(**room['kwargs'])
  #max_x = len(max(map_grid,key=len))
  #for y in range(len(map_grid)):
    #for x in range(len(map_grid[y])):
      #if x > world_size_x:
        #world_size_x = x
      #if y > world_size_y:
        #world_size_y = y
      #tile = map_grid[y][x]
      #tile_split = tile.split(":")
      #tile_type = tile_split[0]
      #if tile_type not in tile_list.keys():
        #_world[(x,y)] = None
        #continue
      #if tile_type == 'S':
        #global starting_position
        #starting_position = (x,y)
      #if len(tile_split) > 1:
        #_world[(x,y)] = getattr(__import__('tiles'),tile_list[tile_type])(x,y,tile_split[1])
      #else:      
        #_world[(x,y)] = getattr(__import__('tiles'),tile_list[tile_type])(x,y)
  world_size = (world_size_x, world_size_y)

def tile_exists(x,y):
  return (x,y) in _world.keys()

def get_tile(x,y):
  if tile_exists(x,y):
    return _world[(x,y)]
  else:
    raise IndexError

def set_tile(x,y,tile):
  if tile_exists(x,y):
    _world[(x,y)] = tile
  else:
    raise IndexError  
