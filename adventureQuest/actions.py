import player

class Action():
  def __init__(self, method, name, hotkey, **kwargs):
    self.method = method
    self.name = name
    self.hotkey = hotkey
    self.kwargs = kwargs

  def __str__(self):
    return "{}: {}".format(self.hotkey, self.name)

class Attack(Action):
  def __init__(self, enemy):
    super().__init__(method = player.Player.attack, name = 'Fight', hotkey = 'f', enemy = enemy)

class MoveNorth(Action):
  def __init__(self):
    super().__init__(method = player.Player.move_north, name = 'Move North', hotkey = 'w')

class MoveSouth(Action):
  def __init__(self):
    super().__init__(method = player.Player.move_south, name = 'Move South', hotkey = 's')

class MoveEast(Action):
  def __init__(self):
    super().__init__(method = player.Player.move_east, name = 'Move East', hotkey = 'd')

class MoveWest(Action):
  def __init__(self):
    super().__init__(method = player.Player.move_west, name = 'Move West', hotkey = 'a')

class SearchNorth(Action):
  def __init__(self):
    super().__init__(method = player.Player.search_north, name = 'Search North', hotkey = 'sw')

class SearchEast(Action):
  def __init__(self):
    super().__init__(method = player.Player.search_east, name = 'Search East', hotkey = 'sa')

class SearchSouth(Action):
  def __init__(self):
    super().__init__(method = player.Player.search_south, name = 'Search South', hotkey = 'ss')

class SearchWest(Action):
  def __init__(self):
    super().__init__(method = player.Player.search_west, name = 'Search West', hotkey = 'sd')

class UseItem(Action):
  def __init__(self):
    super().__init__(method = player.Player.use_item, name = 'Use Item', hotkey = 'u')

class Repair(Action):
  def __init__(self):
    super().__init__(method = player.Player.repair, name = 'Repair Item', hotkey = 'r')

class Flee(Action):
  def __init__(self, enemy):
    super().__init__(method = player.Player.flee, name = 'Flee', hotkey = 'g', enemy = enemy)

class EquipWeapon(Action):
  def __init__(self):
    super().__init__(method = player.Player.equip_weapon, name = 'Equip Weapon', hotkey = 'ew')

class EquipArmour(Action):
  def __init__(self):
    super().__init__(method = player.Player.equip_armour, name = 'Equip Armour', hotkey = 'ea')

class ShowInventory(Action):
  def __init__(self):
    super().__init__(method = player.Player.print_inventory, name = 'Show Inventory', hotkey = 'i')

class ShowMap(Action):
  def __init__(self):
    super().__init__(method = player.Player.print_map, name = 'Show Map', hotkey = 'm')

class Examine(Action):
  def __init__(self):
    super().__init__(method = player.Player.examine_enemy, name = 'Examine Body', hotkey = 'x', enemy = enemy)

class ShowHealth(Action):
  def __init__(self):
    super().__init__(method = player.Player.print_health, name = "Show Health", hotkey = 'hp')
