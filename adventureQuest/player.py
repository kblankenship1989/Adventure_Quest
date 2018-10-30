import  items
import  random
import  enemies
import  world
import math

class Player:
  def __init__(self, name, difficulty):
    self.name = name
    print("Welcome to THE DUNGEON, " + name)
    if difficulty.lower() == "easy":
      self.hp = 100
      self.max_hp = 100
      self.repair_skill = 3
      self.search_skill = 3
      self.initiative = 10
      self.gold = 50
      self.inventory = [items.MinorHealthPotion(), items.MinorHealthPotion()]
      self.equipped_weapon = items.Sword()
      self.equipped_armour = items.LightArmour()
    elif difficulty.lower() == "medium":
      self.hp = 75
      self.max_hp = 75
      self.repair_skill = 2
      self.search_skill = 2
      self.initiative = 5
      self.gold = 25
      self.inventory = [items.MinorHealthPotion()]
      self.equipped_weapon = items.Dagger()
      self.equipped_armour = items.LightArmour()
    else:
      self.hp = 50
      self.max_hp = 50
      self.repair_skill = 1
      self.search_skill = 1
      self.initiative = 3
      self.gold = 15
      self.inventory = []
      self.equipped_weapon = items.Dagger()
      self.equipped_armour = items.Cloth()
    self.location_x, self.location_y = world.starting_position
    self.prev_location_x = self.location_x
    self.prev_location_y = self.location_y
    self.victory = False  
    self.quit = False
    self.xp = 0
    self.level = 1
    self.hp_per_lvl = 10
    self.repair_skill_per_lvl = 1
    self.search_skill_per_lvl = 1
    self.initiative_per_lvl = 2
    
  def quit_game(self):
    self.quit = True
    
  def xp_gain(self, xp):
    self.xp += xp
    if self.xp > round(self.level*math.log10(self.level)*50,0):
      self.level_up()
    
  def level_up(self):
    print("You leveled up! You are now level {}".format(self.level))
    self.max_hp += self.hp_per_lvl
    self.hp += self.hp_per_lvl
    self.initiative += self.initiative_per_lvl
    self.repair_skill += self.repair_skill_per_lvl
    self.search_skill += self.search_skill_per_lvl
    self.level += 1
  
  def is_alive(self):
    return self.hp > 0

  def print_health(self):
    print("Current HP:  {} of {}".format(self.hp, self.max_hp))
  
  def print_inventory(self):
    print("Current inventory:\n\nEquipped Weapon: "
          + str(self.equipped_weapon)
          + "\n\nEquipped Armour: "
          + str(self.equipped_armour)
          + "\n\n"
          + "\n\n".join([str(x) for x in self.inventory])
          + "\n\nGold: " + str(self.gold) + "\n")
    
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
        elif world.tile_at(x,y):
          if world.tile_at(x,y).visited:
            map_print += world.tile_at(x,y).map_symbol
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
    dx = 0
    dy = -1
    self.move(dx, dy)

  def move_east(self):
    dx = 1
    dy = 0
    self.move(dx, dy)

  def move_south(self):
    dx = 0
    dy = 1
    self.move(dx, dy)

  def move_west(self):
    dx = -1
    dy = 0
    self.move(dx, dy)
  
  def search(self, dx, dy):
    tile = world.tile_at(self.location_x + dx, self.location_y + dy)
    tile.search(self)    

  def search_north(self):
    dx = 0
    dy = -1
    self.search(dx, dy)

  def search_east(self):
    dx = 1
    dy = 0
    self.search(dx, dy)

  def search_south(self):
    dx = 0
    dy = 1
    self.search(dx, dy)

  def search_west(self):
    dx = -1
    dy = 0
    self.search(dx, dy)

  def flee(self):
    enemy = world.tile_at(self.location_x, self.location_y).enemy
    player_initiative = self.initiative - self.equipped_weapon.weapon_penalty - self.equipped_armour.armour_penalty
    if enemy.initiative > player_initiative:
      print("As you attempt to flee, the {} is too quick for you and strikes one last time.\n{} deals {} damage to you, but your {} manages to block {} of it.".format(enemy.name, enemy.name, enemy.damage, self.equipped_armour.name, self.equipped_armour.protection))
      self.hp -= (enemy.damage - self.equipped_armour.protection if enemy.damage > self.equipped_armour.protection else 0)
    if self.is_alive():
      print("You manage to escape back the way you came, but the {} will be waiting when you return....".format(enemy.name))
      self.location_x = self.prev_location_x
      self.location_y = self.prev_location_y
    else:
      print("The {} has dealt a critical blow, leaving you mortally bleeding as it poises for the final strike!\nYou watch helplessly as your death comes.".format(enemy.name))
         #game_over
      
  def attack(self):
    enemy = world.tile_at(self.location_x, self.location_y).enemy
    player_initiative = self.initiative - self.equipped_weapon.weapon_penalty - self.equipped_armour.armour_penalty
    if enemy.initiative > player_initiative:
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
            self.xp_gain(enemy.xp)
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
        self.xp_gain(enemy.xp)
      else:
        self.hp -= (enemy.damage - self.equipped_armour.protection if enemy.damage > self.equipped_armour.protection else 0)
        print("The {} strikes back in retaliation, dealing {} damage to you as you fail to duck out of the way, but your {} manages to block {} of it.".format(enemy.name, enemy.damage, self.equipped_armour.name, self.equipped_armour.protection))
        if not self.is_alive():
          print("The {} has dealt a critical blow, leaving you mortally bleeding as it poises for the final strike!\nYou watch helplessly as your death comes.".format(enemy.name))
          #game over

  def heal(self):
    input_text = "Select the item to use:\n"
    for i in range(len(self.inventory)):
      if isinstance(self.inventory[i], items.Healing):
        input_text += "{}:  {}\n".format(i, self.inventory[i].name)
    input_text += "x: Cancel\n"
    item = input(input_text)
    valid = False
    while not valid:
      if item.lower() == "x":
        valid = True
        break
      elif item.isdigit():
        if int(item) >= 0 and int(item) < len(self.inventory):
          valid = True
          break
      item = input("Invalid selection.  Please select from the list below.\n" + input_text)
    if item.lower() == "x":
      pass
    else:
      usable = self.inventory.pop(int(item))
      usable.use(self)

  def add_loot(self, gold, loot):
    if gold > 0:
      print("{} gold\n".format(gold))
      self.gold += gold
    if len(loot) > 0:
      for item in loot:
        print(str(item)+"\n")
        if isinstance(item,items.StatIncrease):
          item.use(self)
          loot.remove(item)
      self.inventory += loot
    print("You add these items to your bag and continue on your journey")

  def repair(self):
    input_text = "Select item to repair:\nw: {} (equipped, Quality: {}/{})\na: {} (equipped, Quality: {}/{})\n".format(self.equipped_weapon.name, self.equipped_weapon.quality, self.equipped_weapon.max_quality, self.equipped_armour.name, self.equipped_armour.quality, self.equipped_armour.max_quality)
    for i in range(len(self.inventory)):
      item = self.inventory[i]
      if isinstance(item, items.Weapon) or isinstance(item, items.Armour):
        input_text += "{}: {} (Quality: {}/{})\n".format(i, item.name, item.quality, item.max_quality)
    input_text += "x: Cancel \n"
    item = input(input_text)
    valid = False
    while not valid:
      if item.lower() in ["a", "w", "x"]:
        valid = True
        break
      elif item.isdigit():
        if int(item) >= 0 and int(item) < len(self.inventory):
          valid = True
          break
      item = input("Invalid input.  Please select from the list below.\n" + input_text)
    if item.lower() == "x":
      pass
    elif item.lower() == "a":
      self.equipped_armour.repair(self)
    elif item.lower() == "w":
      self.equipped_weapon.repair(self)
    else:
      self.inventory[int(item)].repair(self)
  
  def equip_weapon(self):
    input_text = "Select:\nw: {} (equipped, Quality: {}/{})\n".format(self.equipped_weapon.name, self.equipped_weapon.quality, self.equipped_weapon.max_quality)
    for i in range(len(self.inventory)):
      item = self.inventory[i]
      if isinstance(item, items.Weapon):
        input_text += "{}: {} (Quality: {}/{})\n".format(i, item.name, item.quality, item.max_quality)
    input_text += "x: Cancel \n"
    item = input(input_text)
    valid = False
    while not valid:
      if item.lower() in ["x","w"]:
        valid = True
        break
      elif item.isdigit():
        if int(item) >= 0 and int(item) < len(self.inventory):
          valid = True
          break
      item = input("Invalid input.  Please select from the list below.\n" + input_text)
    if item.lower() in ["x","w"]:
      pass
    else:
      chosen_weapon = self.inventory.pop(int(item))
      self.inventory.append(self.equipped_weapon)
      self.equipped_weapon = chosen_weapon
  
  def equip_armour(self):
    input_text = "Select:\na: {} (equipped, Quality: {}/{})\n".format(self.equipped_armour.name, self.equipped_armour.quality, self.equipped_armour.max_quality)
    for i in range(len(self.inventory)):
      item = self.inventory[i]
      if isinstance(item, items.Armour):
        input_text += "{}: {} (Quality: {}/{})\n".format(i, item.name, item.quality, item.max_quality)
    input_text += "x: Cancel \n"
    item = input(input_text)
    valid = False
    while not valid:
      if item.lower() in ["x","a"]:
        valid = True
        break
      elif item.isdigit():
        if int(item) >= 0 and int(item) < len(self.inventory):
          valid = True
          break
      item = input("Invalid input.  Please select from the list below.\n" + input_text)
    if item.lower() in ["x","a"]:
      pass
    else:
      chosen_armour = self.inventory.pop(int(item))
      self.inventory.append(self.equipped_armour)
      self.equipped_armour = chosen_armour
  

  def sell_loot(self):
    input_text = "Select item to sell:\n"
    for i in range(len(self.inventory)):
      input_text += "{}: {} ({} gold)".format(i, self.inventory[i].name, self.inventory[i].value)
    item = input(input_text)
    valid = False
    while not valid:
      if item.lower() == "x":
        valid = True
        break
      elif item.isdigit():
        if int(item) >= 0 and int(item) < len(self.inventory):
          valid = True
          break
      item = input("Invalid selection.  Please select from the list below.\n" + input_text)
    if item.lower() == "x":
      pass
    else:
      sell = self.inventory.pop(int(item))
      self.gold += items.Gold(sell.value)
      
  def examine_enemy(self):
    enemy = world.tile_at(self.location_x, self.location_y).enemy
    if enemy.is_alive():
      if enemy.hp == enemy.max_hp:
        print("The {} doesn't seem to have a scratch on it.  It looks ready to fight!".format(enemy.name))
      else:
        print("The {} appears injured.  It has {} hp remaining but will not back down.".format(enemy.name, enemy.hp))
    else:
      if enemy.gold >0 or len(enemy.loot) > 0:
        print("You examine the lifeless body of the {} and find:\n".format(enemy.name))
        self.add_loot(enemy.gold, enemy.loot)
        enemy.gold = 0
        enemy.loot = []
      else:
        print("You examin the lifeless body of the {} and find nothing of interest.  Your journey continues".format(enemy.name))
