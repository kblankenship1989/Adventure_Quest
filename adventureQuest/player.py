import items
import random
import enemies
import world

class Player:
  def __init__(self, name, difficulty):
    self.name = name
    print("Welcome to THE DUNGEON, " + name)
    if difficulty.lower() == "easy":
      self.hp = 100
      self.max_hp = 100
      self.repair_skill = 5
      self.search_level = 5
      self.initiative = 10
      self.gold = items.Gold(50)
      self.inventory = [items.HealthPotion(10), items.HealthPotion(10)]
      self.equipped_weapon = items.Dagger()
      self.equipped_armour = items.LightArmour()
    elif difficulty.lower() == "medium":
      self.hp = 75
      self.max_hp = 75
      self.repair_skill = 3
      self.search_level = 3
      self.initiative = 5
      self.gold = items.Gold(25)
      self.inventory = [items.HealthPotion(10)]
      self.equipped_weapon = items.Dagger()
      self.equipped_armour = items.Cloth()
    else:
      self.hp = 50
      self.max_hp = 50
      self.repair_skill = 1
      self.search_level = 1
      self.initiative = 3
      self.gold = items.Gold(15)
      self.inventory = []
      self.equipped_weapon = items.Rock()
      self.equipped_armour = items.Cloth()
    self.location_x, self.location_y = world.starting_position
    self.prev_location_x = self.location_x
    self.prev_location_y = self.location_y
    self.victory = False  
  
  def is_alive(self):
    return self.hp > 0

  def print_health(self):
    print("Current HP:  {} of {}".format(self.hp, self.max_hp))
  
  def print_inventory(self):
    print("Current inventory:\n\nEquipped Weapon: "
          + str(self.equipped_weapon)
          + "\n\nEquipped Armour: "
          + str(self.equipped_armour)
          + "\n\n".join([str(x) for x in self.inventory])
          + "\n\n" + str(self.gold) + "\n")
    
  def print_map(self):
    map_print = '--'
    max_x, max_y = world.world_size
    for k in range(max_x+1):
      map_print += "-"
    map_print += "\n"
    for y in range(max_y+1):
      map_print += "|"
      for x in range(max_x+1):
        if x == self.location_x and y == self.location_y:
          map_print += "O"
        elif world.tile_exists(x,y):
          if world.get_tile(x,y).visited:
            map_print += world.get_tile(x,y).map_symbol
          else:
            map_print += " "
        else:
          map_print += " "
      map_print += "|\n"
    for k in range(max_x+1):
      map_print += "-"
    map_print += "--\n"
    print(map_print)
  
  def move(self, dx, dy):
    self.prev_location_x = self.location_x
    self.prev_location_y = self.location_y
    self.location_x += dx
    self.location_y += dy

  def move_north(self):
    __dx = 0
    __dy = -1
    self.move(__dx, __dy)

  def move_east(self):
    __dx = 1
    __dy = 0
    self.move(__dx, __dy)

  def move_south(self):
    __dx = 0
    __dy = 1
    self.move(__dx, __dy)

  def move_west(self):
    __dx = -1
    __dy = 0
    self.move(__dx, __dy)
  
  def search(self, dx, dy):
    __tile = world.get_tile(self.location_x + dx, self.location_y + dy)
    __tile.search(self)
    world.set_tile(self.location_x + dx, self.location_y + dy, __tile)    

  def search_north(self):
    __dx = 0
    __dy = -1
    self.search(__dx, __dy)

  def search_east(self):
    __dx = 1
    __dy = 0
    self.search(__dx, __dy)

  def search_south(self):
    __dx = 0
    __dy = 1
    self.search(__dx, __dy)

  def search_west(self):
    __dx = -1
    __dy = 0
    self.search(__dx, __dy)

  def flee(self, enemy):
    __player_initiative = self.initiative - self.equipped_weapon.weapon_penalty - self.equipped_armour.armour_penalty
    __tile = world.get_tile(self.location_x, self.location_y)
    if enemy.initiative > __player_initiative:
      print("As you attempt to flee, the {} is too quick for you and strikes one last time.\n{} deals {} damage to you, but your {} manages to block {} of it.".format(enemy.name, enemy.name, enemy.damage, self.equipped_armour.name, self.equipped_armour.protection))
      self.hp -= (enemy.damage - self.equipped_armour.protection if enemy.damage > self.equipped_armour.protection else 0)
    if self.is_alive():
      print("You manage to escape back the way you came, but the {} will be waiting when you return....".format(enemy.name))
      __tile.is_trap = True
      world.set_tile(self.location_x, self.location_y, __tile)
      self.location_x = self.prev_location_x
      self.location_y = self.prev_location_y
    else:
      print("The {} has dealt a critical blow, leaving you mortally bleeding as it poises for the final strike!\nYou watch helplessly as your death comes.".format(enemy.name))
         #game_over
      
  def attack(self, enemy):
    __player_initiative = self.initiative - self.equipped_weapon.weapon_penalty - self.equipped_armour.armour_penalty
    if enemy.initiative > __player_initiative:
      if enemy.is_alive():
        print("Your prepare to attack but the {} is too quick for you and strikes first.\n{} deals {} damage to you, but your {} manages to block {} of it.".format(enemy.name, enemy.name, enemy.damage, self.equipped_armour.name, self.equipped_armour.protection))
        self.hp -= (enemy.damage - self.equipped_armour.protection if enemy.damage > self.equipped_armour.protection else 0)
        if self.is_alive():
          enemy.hp -= (self.equipped_weapon.damage - enemy.protection if self.equipped_weapon.damage > enemy.protection else 0)
          print("You strike back in retaliation, dealing {} damage to the {}, but its tough skin blocks {} of it.".format(self.equipped_weapon.damage, enemy.name, enemy.protection))
          if random.randint(0,9) < 2:
            self.equipped_weapon.weardown(self)
          if not enemy.is_alive():
            print("You have dealt a critical blow to the {} and it now lies dead and bleeding at your feet.".format(enemy.name))
        else:
          print("The {} has dealt a critical blow, leaving you mortally bleeding as it poises for the final strike!\nYou watch helplessly as your death comes.".format(enemy.name))
          #game_over
      else:
        print("The {} lies dead at your feet, but you choose to strike its lifeless body for good measure.".format(enemy.name))
    else:
      enemy.hp -= (self.equipped_weapon.damage - enemy.protection if self.equipped_weapon.damage > enemy.protection else 0)
      print("You strike swiftly with your {}, dealing {} damage to the {} before it can react, but its tough skin blocks {} of it.".format(self.equipped_weapon.name, self.equipped_weapon.damage, enemy.name, enemy.protection))
      if random.randint(0,9) < 2:
        self.equipped_weapon.weardown(self)
      if not enemy.is_alive():
        print("You have dealt a critical blow to the {} and it now lies dead and bleeding at your feet.".format(enemy.name))
      else:
        self.hp -= (enemy.damage - self.equipped_armour.protection if enemy.damage > self.equipped_armour.protection else 0)
        print("The {} strikes back in retaliation, dealing {} damage to you as you fail to duck out of the way, but your {} manages to block {} of it.".format(enemy.name, enemy.damage, self.equipped_armour.name, self.equipped_armour.protection))
        if not self.is_alive():
          print("The {} has dealt a critical blow, leaving you mortally bleeding as it poises for the final strike!\nYou watch helplessly as your death comes.".format(enemy.name))
          #game over

  def use_item(self):
    __input_text = "Select the item to use:\n"
    for i in range(len(self.inventory)):
      if isinstance(self.inventory[i], items.UsableItem):
        __input_text += "{}:  {}\n".format(i, self.inventory[i].name)
    __input_text += "x: Cancel\n"
    __item = input(__input_text)
    __valid = False
    while not __valid:
      if __item.lower() == "x":
        __valid = True
        break
      elif __item.isdigit():
        if int(__item) >= 0 and int(__item) < len(self.inventory):
          __valid = True
          break
      __item = input("Invalid selection.  Please select from the list below.\n" + __input_text)
    if __item.lower() == "x":
      pass
    else:
      __usable = self.inventory.pop(int(__item))
      __usable.use(self)

  def add_loot(self, _items):
    for item in _items:
      if isinstance(item, items.Gold):
        self.gold += item
      else:
        self.inventory.append(item)

  def repair(self):
    __input_text = "Select item to repair:\nw: {} (equipped, Quality: {}/{})\na: {} (equipped, Quality: {}/{})\n".format(self.equipped_weapon.name, self.equipped_weapon.quality, self.equipped_weapon.max_quality, self.equipped_armour.name, self.equipped_armour.quality, self.equipped_armour.max_quality)
    for i in range(len(self.inventory)):
      item = self.inventory[i]
      if isinstance(item, items.Weapon) or isinstance(item, items.Armour):
        __input_text += "{}: {} (Quality: {}/{})\n".format(i, item.name, item.quality, item.max_quality)
    __input_test += "x: Cancel \n"
    __item = input(__input_text)
    __valid = False
    while not __valid:
      if __item.lower() in ["a", "w", "x"]:
        __valid = True
        break
      elif __item.isdigit():
        if int(__item) >= 0 and int(__item) < len(self.inventory):
          __valid = True
          break
      __item = input("Invalid input.  Please select from the list below.\n" + __input_text)
    if __item.lower() == "x":
      pass
    elif __item.lower() == "a":
      self.equipped_armour.repair(self)
    elif __item.lower() == "w":
      self.equipped_weapon.repair(self)
    else:
      self.inventory[int(__item)].repair(self)
  
  def equip_weapon(self):
    __input_text = "Select:\nw: {} (equipped, Quality: {}/{})\n".format(self.equipped_weapon.name, self.equipped_weapon.quality, self.equipped_weapon.max_quality)
    for i in range(len(self.inventory)):
      item = self.inventory[i]
      if isinstance(item, items.Weapon):
        __input_text += "{}: {} (Quality: {}/{})\n".format(i, item.name, item.quality, item.max_quality)
    __input_text += "x: Cancel \n"
    __item = input(__input_text)
    __valid = False
    while not __valid:
      if __item.lower() in ["x","w"]:
        __valid = True
        break
      elif __item.isdigit():
        if int(__item) >= 0 and int(__item) < len(self.inventory):
          __valid = True
          break
      __item = input("Invalid input.  Please select from the list below.\n" + __input_text)
    if __item.lower() in ["x","w"]:
      pass
    else:
      __chosen_weapon = self.inventory.pop(int(__item))
      self.inventory.append(self.equipped_weapon)
      self.equipped_weapon = __chosen_weapon
  
  def equip_armour(self):
    __input_text = "Select:\na: {} (equipped, Quality: {}/{})\n".format(self.equipped_armour.name, self.equipped_armour.quality, self.equipped_armour.max_quality)
    for i in range(len(self.inventory)):
      item = self.inventory[i]
      if isinstance(item, items.Armour):
        __input_text += "{}: {} (Quality: {}/{})\n".format(i, item.name, item.quality, item.max_quality)
    __input_text += "x: Cancel \n"
    __item = input(__input_text)
    __valid = False
    while not __valid:
      if __item.lower() in ["x","a"]:
        __valid = True
        break
      elif __item.isdigit():
        if int(__item) >= 0 and int(__item) < len(self.inventory):
          __valid = True
          break
      __item = input("Invalid input.  Please select from the list below.\n" + __input_text)
    if __item.lower() in ["x","a"]:
      pass
    else:
      __chosen_armour = self.inventory.pop(int(__item))
      self.inventory.append(self.equipped_armour)
      self.equipped_armour = __chosen_armour
  

  def sell_loot(self):
    __input_text = "Select item to sell:\n"
    for i in range(len(self.inventory)):
      __input_text += "{}: {} ({} gold)".format(i, self.inventory[i].name, self.inventory[i].value)
    __item = input(__input_text)
    __valid = False
    while not __valid:
      if __item.lower() == "x":
        __valid = True
        break
      elif __item.isdigit():
        if int(__item) >= 0 and int(__item) < len(self.inventory):
          __valid = True
          break
      __item = input("Invalid selection.  Please select from the list below.\n" + __input_text)
    if __item.lower() == "x":
      pass
    else:
      __sell = self.inventory.pop(int(__item))
      self.gold += items.Gold(__sell.value)
      
  def do_action(self, action, **kwargs):
    __action_method = getattr(self, action.method.__name__)
    if __action_method:
      __action_method(**kwargs)
