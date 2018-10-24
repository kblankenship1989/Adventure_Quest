from collections import OrderedDict
from player import Player
import world
import enemies
import items
import npc

# def play():
  # world.load_tiles('level_1')
  # player_name = input("Enter player name: ")
  # difficulty = input("Enter difficulty [easy / medium / hard]:  ")
  # p = Player(player_name, difficulty)
  # while p.is_alive() and not player.victory:
    # room = world.get_tile(player.location_x, player.location_y)
    # room.enter_room(player)
    # start_x = player.location_x
    # start_y = player.location_y
    # while p.is_alive() and not player.victory:
      # input_text = "Choose an Action:\n"
      # available_actions = room.available_actions()
      # input_text += "\n".join([str(x) for x in available_actions]) + "\n\nAction:"
      # user_action = input(input_text)
      # while user_action.lower() not in [x.hotkey for x in available_actions]:
        # user_action = input("Invalid action, please choose from the list below.\n\n" + input_text)
      # for action in available_actions:
        # if action.hotkey == user_action.lower():
          # player.do_action(action, **action.kwargs)
          # break
      # if player.location_x != start_x or player.location_y != start_y:
        # break
    # world.set_tile(start_x, start_y, room)

def play(level, p):
  world.load_tiles(level)
  
  world.parse_world_dsl()
  while p.is_alive() and not p.victory:
	room = world.tile_at(p.location_x, p.location_y)
	room.enter_room(p)
	choose_action(room, p)


def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")

def get_available_actions(room, player):
    actions = OrderedDict()
    print("Choose an action: ")
	action_adder(actions, 'm', player.print_map, "Show map")
	action_adder(actions, 'hp', player.print_health, "Show health")
	action_adder(actions, 'ew', player.equip_weapon, "Equip weapon")
	action.adder(actions, 'ea', player.equip_armour, "Equip armour")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "Print inventory")
		
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'f', player.attack, "Fight")
		action_adder(actions, 'r', player.flee, "Run back")
    else:
	    if isinstance(room, world.EnemyTile):
		  action_adder(actions, 'x', player.examine_enemy, "Examine body")
	    action_adder(actions, 'r', player.repair, "Repair Equipment")
        if world.tile_at(room.x, room.y - 1):
		  if world.tile_at(room.x, room.y-1).is_hidden:
		    action_adder(actions, 'sw', player.search_north, "Search north wall")
		  else:
		    action_adder(actions, 'w', player.move_north, "Go north")
        if world.tile_at(room.x, room.y + 1):
 		  if world.tile_at(room.x, room.y+1).is_hidden:
		    action_adder(actions, 'ss', player.search_north, "Search south wall")
		  else:
           action_adder(actions, 's', player.move_south, "Go south")
        if world.tile_at(room.x + 1, room.y):
		  if world.tile_at(room.x+1, room.y).is_hidden:
		    action_adder(actions, 'sd', player.search_north, "Search east wall")
		  else:
            action_adder(actions, 'd', player.move_east, "Go east")
        if world.tile_at(room.x - 1, room.y):
		  if world.tile_at(room.x-1, room.y).is_hidden:
		    action_adder(actions, 'sa', player.search_north, "Search west wall")
		  else:
            action_adder(actions, 'a', player.move_west, "Go west")
    if player.hp < player.max_hp:
        action_adder(actions, 'h', player.use_item, "Heal")

    return actions
	
def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))

if __name__ == '__main__':
  quit = False:
  while not quit:
    player_name = input("Enter player name: ")
    difficulty = input("Enter difficulty [easy / medium / hard]:  ")
    p = Player(player_name, difficulty)
	lvls = sorted(world.levels.keys())
	level = None
	while level is None:
	  print("Please select Level to Play")
	  for i in range(len(lvls)):
	    print("{}: {}".format(i,lvls[i]))
      lvl_input = input("Level:")
	  if lvls[lvl_input]:
	    level = lvls[lvl_input]
	  else:
	    print("Invalid level")
	play(level, p)
