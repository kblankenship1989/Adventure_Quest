import player as p
import actions
import tiles
import world
import enemies
import items

def play():
  world.load_tiles('level_1')
  player_name = input("Enter player name: ")
  difficulty = input("Enter difficulty [easy / medium / hard]:  ")
  player = p.Player(player_name, difficulty)
  while player.is_alive() and not player.victory:
    room = world.get_tile(player.location_x, player.location_y)
    room.enter_room(player)
    start_x = player.location_x
    start_y = player.location_y
    while player.is_alive() and not player.victory:
      input_text = "Choose an Action:\n"
      available_actions = room.available_actions()
      input_text += "\n".join([str(x) for x in available_actions]) + "\n\nAction:"
      user_action = input(input_text)
      while user_action.lower() not in [x.hotkey for x in available_actions]:
        user_action = input("Invalid action, please choose from the list below.\n\n" + input_text)
      for action in available_actions:
        if action.hotkey == user_action.lower():
          player.do_action(action, **action.kwargs)
          break
      if player.location_x != start_x or player.location_y != start_y:
        break
    world.set_tile(start_x, start_y, room)

if __name__ == '__main__':
  play()
