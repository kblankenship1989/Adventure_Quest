import random
import items
import enemies
import player
import world

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
    player.add_loot(self.loot)
    print("You have found: " + "\n\n".join([str(x) for x in self.loot]))
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
