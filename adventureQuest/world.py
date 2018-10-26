import  items
import  enemies
import  player
import  json
import  numpy as np
import npc as NPC

_levels = {}
_world = {}
starting_position = (0,0)
_items = []
_enemies = []
trade_inventory = []
trade_gold = 0

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
  def __init__(self, x, y):
    super().__init__(x, y, "Another empty room.  Your journey continues!", "X", False)
   
class LootRoom(MapTile):
  def __init__(self, x, y, intro_text = "You found stuff!  Pick it up?", item = None, is_trap = False):
    self.is_trap = is_trap
    self.gold = random.randint(5,25)
    if item is None:
      num_items = random.randint(1,(len(world._items)-1 if len(world._items) < 4 else 4))
      self.loot = []
      for i in range(num_items):
        item = world._items.pop(random.randint(0, len(world._items)-1))
        self.loot.append(getattr(__import__('items'),item)())
    else:
      self.loot = [getattr(__import__('items'),item)()]
    __amt =  random.randint(0,50)
    if __amt > 0:  self.loot.append(items.Gold(__amt))
    super().__init__(x, y, intro_text)
  
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
      world.set_tile(self.x, self.y, EnemyRoom(self.x, self.y, "As you reach for the loot, you hear something behind you...", None, True))
      world.get_tile(self.x, self.y).enter_room()
          
class EnemyRoom(MapTile):
  def __init__(self, x, y, intro_text = "An enemy!  AHHHH!", enemy = None, is_trap = False):
    if enemy is None:
      enemy = world._enemies.pop(random.randint(0, len(world._enemies)-1))
      self.enemy = getattr(__import__('enemies'),enemy)()
    else:
      self.enemy = getattr(__import__('enemies'),enemy)()
    self.is_trap = is_trap
    super().__init__(x, y, intro_text)

  def enter_room(self, player):
    if self.visited:
      if self.enemy.is_alive():
        print("The {} has been paitently waiting for your return and strikes as soon as you enter!".format(self.enemy.name))
      else:
        print("The lifeless body of the {} lies at your feet.  You take one last look to ensure it is dead and continue on your journey.".format(self.enemy.name))
    else:
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
    T = Trap room
    L = Loot room
    X = Empty room
    D = Dungeon exit
    I:***** - Specific item room (must specify name of item after colon)
    B:***** - Boss / specific enemy room (must specify name of enemy after colon)
  """
  
  tile_list = {'S':"StartingRoom",
               'E':"EnemyRoom",
               'L':"LootRoom",
               'T':"TraderRoom",
               'H':"Hidden",
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
  start_found = False
  end_found = False
  for x in range(len(current_level["map"])):
    row = current_level["map"].split("|")
  for y in range(len(row)):
    if row[y].upper() == "E":
      end_found = True
    if row[y].upper() == "S":
      starting_position = (x,y)
      tile_key = "S"
      start_found = True
    elif row[y].upper() == "X":
      tile = np.random.choice(["EnemyRoom","LootRoom","EmptyRoom"],1,[0.4,0.3,0.3])
    else:
      tile = tile_list[row[y].upper()]
    kwargs = None
    for kwarg in level['kwargs']:
      if kwarg['x'] == x and kwarg['y'] == y:
        kwargs = kwarg['kwargs']
    if not (start_found and end_found):
      raise SyntaxError("Map is invalid!")
    _world[(x,y)] = getattr(__import__("tiles",tile))(x=x,y=y,**kwargs)
 
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
