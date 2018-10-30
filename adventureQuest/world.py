import  items
import  enemies
import  player
import  json
import  numpy as np
import npc as NPC
import sys
import random

_levels = {}
_world = {}
starting_position = (0,0)
_items = {}
_enemies = {}
trade_inventory = []
trade_gold = 0
world_size = (0,0)

class MapTile:
  def __init__(self, x, y, intro_text = "Another empty room.  It appears your journey continues!", map_symbol = "X", is_hidden = False, search_level = 0):
    self.x = x
    self.y = y
    self.intro_text = intro_text
    self.is_hidden = is_hidden
    self.map_symbol = map_symbol
    self.search_level = search_level
    self.visited = False
        
  def __str__(self):
    return self.intro_text

  def enter_room(self, player):
    if self.visited:
      print("You have already been in this room.  There is nothing more to find\n")
    else:
      player.xp_gain(1)
      print(self.intro_text)
      self.modify_player(player)

  def modify_player(self,player):
    self.visited = True

  def search(self, player):
    if not self.is_hidden:
      print("There is nothing to unusual in this room.")
      return
    if player.search_skill >= self.search_level:
      self.is_hidden = False
      player.xp_gain(self.search_level)
      print("You search the room and find a small switch on the wall.\nAfter pressing it, a door opens that wasn't there before.")
    else:
      print("After looking around the room, you do not see anything out of the ordinary.\nThis appears to be just another empty room.")  
   
class StartingRoom(MapTile):
  def __init__(self, x, y, intro_text = "You awake in a dark, damp room in the middle of a cave.  Your first thought is escape!"):
    super().__init__(x, y , intro_text, "S", False)
    
  def modify_player(self, player):
    player.victory = False
    super().modify_player(player)

class EmptyRoom(MapTile):
  def __init__(self, x, y, is_hidden = False, search_lvl = 0):
    super().__init__(x, y, "Another empty room.  Your journey continues!", "X", is_hidden = is_hidden, search_level = search_lvl)
   
class LootRoom(MapTile):
  def __init__(self, x, y, intro_text = "You found stuff!  Pick it up?", item = None, is_trap = False, is_hidden = False, search_lvl = 0):
    self.is_trap = is_trap
    self.gold = random.randint(5,25)
    if item is None:
      num_items = random.randint(1,2)
      self.loot = []
      for i in range(num_items):
        item = np.random.choice(_items['item'],size=1,p=_items['prob'])[0]
        self.loot.append(getattr(__import__('items'),item)())
    else:
      self.loot = [getattr(__import__('items'),item)()]
    super().__init__(x, y, intro_text, is_hidden = is_hidden, search_level = search_lvl)
  
  def enter_room(self, player):
    if self.visited:
      print("You have already been in this room and found everything you can")
    else:
      __confirm = input(self.intro_text + '[y/n]')
      if __confirm.lower() == 'y':
        self.modify_player(player)

  def modify_player(self, player):
    print("You find a small pile of rocks.  After moving some of them around, you discover:\n")
    player.add_loot(self.gold,self.loot)
    self.loot = []
    self.gold = 0
    super().modify_player(player)
    if self.is_trap:
      world.swap_tile(self.x, self.y, EnemyRoom(self.x, self.y, "As you reach for the loot, you hear something behind you...", None, True))
          
class EnemyRoom(MapTile):
  def __init__(self, x, y, intro_text = "An enemy!  AHHHH!", enemy = None, enemy_level = 1, is_trap = False, is_hidden = False, search_lvl = 0):
    enemy_level = random.randint(_enemies['enemy_min_level'],_enemies['enemy_max_level'])
    if enemy is None:
      enemy = np.random.choice(_enemies['enemy'],size=1,p=_enemies['prob'])[0]
      self.enemy = getattr(__import__('enemies'),enemy)(enemy_level)
    else:
      self.enemy = getattr(__import__('enemies'),enemy)(enemy_level)
    self.is_trap = is_trap
    super().__init__(x, y, intro_text, is_hidden = is_hidden, search_level = search_lvl)

  def enter_room(self, player):
    if self.visited:
      if self.enemy.is_alive():
        print("The {} has been paitently waiting for your return and strikes as soon as you enter!".format(self.enemy.name))
        self.enemy.attack(player)
      else:
        print("The lifeless body of the {} lies at your feet.  You take one last look to ensure it is dead and continue on your journey.".format(self.enemy.name))
    else:
      print("A dark figure appears from the shadows.  A fierce {} stands before you, furious with you tresspassing in his home.".format(self.enemy.name))
      self.modify_player(player)

  def modify_player(self, player):
    if self.visited:
      self.is_trap = False
    if self.is_trap and self.enemy.is_alive():
      self.enemy.attack(player)
    super().modify_player(player)
      
class DungeonEnd(MapTile):
  def __init__(self, x, y, intro_text = "You found a door!"):
    super().__init__(x, y, intro_text, "E", False)
    
  def enter_room(self, player):
    __keyFound = False
    for i in player.inventory:
      if isinstance(i, items.DungeonKey):
        __keyFound = True
        break
    if __keyFound:
      __leave = input("Would you like to leave the dungeon?[y/n]")
      if __leave:
        print("You made it to the end of the dungeon alive!  However there is still more to explore before you are finally free...")
        player.victory = True
        #end level here
    else:
      print("You have found the exit to the dungeon but it appears to be locked and you don't have the right key.\nYou will have to continue exploring until you find it.")

class NPCTile(MapTile):
  def __init__(self, x, y, npc = NPC.NPC("Steve"), intro_text = "Another traveler stands before you"):
    self.npc = npc
    super().__init__(x, y, intro_text, "T", False)
 
 
def load_levels():
  with open('resources/levels.json','r') as f:
    global _levels
    _levels = json.load(f) 

def load_tiles(level):
  """
  This function loads a reference text file to build the world.
  This can be called each time the player advances levels to trigger a new map.
  Map is a list structure of 1-letter references to rooms:
    S = Starting room (1 per map)
    E = Enemy room
    T = NPC Room
    L = Loot room
    X = Empty room
    D = Dungeon exit
  """
  
  tile_list = {'S':"StartingRoom",
               'E':"EnemyRoom",
               'L':"LootRoom",
               'T':"NPCTile",
               'D':"DungeonEnd"
               }
 
  current_level = _levels[level]
  
  global _items
  _items = current_level['items']
  global _enemies
  _enemies = current_level['enemies']
  global trade_inventory
  global trade_gold
  trader = current_level['trade_inventory']
  for item, qty in trader.items():
    if item == 'Gold':
      trade_gold = qty
    else:
      for i in range(qty):
        trade_inventory.append(getattr(__import__("items"),item)())

  global _world
  global starting_position
  global world_size
  start_found = False
  end_found = False
  world_size_list = list(world_size)
  for y in range(len(current_level["map"])):
    row = current_level["map"][y].split("|")
    if y > world_size_list[1]:  world_size_list[1] = y
    for x in range(len(row)):
      if x > world_size_list[0]:  world_size_list[0] = x
      if row[x].upper() == "E":
        end_found = True
      if row[x].upper() == "S":
        starting_position = (x,y)
        tile = tile_list["S"]
        start_found = True
      elif row[x].upper() == "X":
        tile = np.random.choice(["EnemyRoom","LootRoom","EmptyRoom"],size=1,p=[0.4,0.3,0.3])[0]
      else:
        tile = tile_list.get(row[x].upper())
      kwargs = {}
      if tile is None:  continue
      for kwarg in current_level['kwargs']:
        if kwarg['x'] == x and kwarg['y'] == y:
          kwargs = kwarg['kwargs']
      _world[(x,y)] = getattr(sys.modules[__name__],tile)(x=x,y=y,**kwargs)
  if not (start_found and end_found):
    raise SyntaxError("Map is invalid!")
  world_size = tuple(world_size_list)
 
def tile_at(x,y):
  return _world.get((x,y))
  
def swap_tile(x,y,new_tile):
  if isinstance(new_tile,MapTile):
    _world[(x,y)] = new_tile
  else:
    raise SyntaxError("Not a Map Tile")