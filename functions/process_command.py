from .save_load_game import load_game, save_game
from .move import move_player
from .sanitize_filename import sanitize_filename


def process_command(command, map_size, region_map_size, maps, player_state, mobs_data, save_location):
    command = command.lower()
    command = command.strip()
    player_state, world_change = move_player(command, map_size, region_map_size, player_state, "World")
    state = {"command_len": len(command)}
    if command[:4] == "save":
        if command[5:].strip() == "":
            state["error_msg"] = "Please enter save name"
        else:
            save_location = command[5:]
            save_location = sanitize_filename(save_location)
            save_game(save_location, maps, player_state, mobs_data)
            print("Saving")
    elif command[:4].lower() == "load":
        if command == "load current":
            pass
        elif command == "load fresh":
            save_location = ""
        else:
            save_location = command[5:]
            save_location = sanitize_filename(save_location)
        maps, player_state, mobs_data, file_not_found = load_game(command, save_location, map_size, region_map_size,
                                                                  maps,
                                                                  player_state,
                                                                  mobs_data)
        if file_not_found:
            state["file_not_found"] = True
        print("Loading")
    if command == "":
        state['error_msg'] = "Please enter a command"
    state['command'] = command
    print(state)
    return state, maps, player_state, mobs_data, save_location
