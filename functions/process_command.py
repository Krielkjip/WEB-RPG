from .save_load_game import load_game, save_game
from .move import move_player
from .sanitize_filename import sanitize_filename


def process_command(command, map_size, region_map_size, maps, player_state, mobs_data, save_location):
    """
    Process a user command and update the game state accordingly.

    Args:
        command (str): The user's input command
        map_size (int): The size of the game map
        region_map_size (int): The size of the region map
        maps (dict): The current game maps
        player_state (dict): The current player state
        mobs_data (dict): The current mob data
        save_location (str): The current save location

    Returns:
        state (dict): The updated game state
        maps (dict): The updated game maps
        player_state (dict): The updated player state
        mobs_data (dict): The updated mob data
        save_location (str): The updated save location
    """
    # Convert the command to lowercase and strip any whitespace
    command = command.lower()
    command = command.strip()

    # Move the player based on the command
    player_state, world_change = move_player(command, map_size, region_map_size, player_state, "World")

    # Initialize the game state dictionary
    state = {"command_len": len(command)}

    # Handle save commands
    if command[:4] == "save":
        # Check if a save name was provided
        if command[5:].strip() == "":
            state["error_msg"] = "Please enter save name"
        else:
            # Sanitize the save name and save the game
            save_location = command[5:]
            save_location = sanitize_filename(save_location)
            save_game(save_location, maps, player_state, mobs_data)
            print("Saving")

    # Handle load commands
    elif command[:4].lower() == "load":
        # Check if the user wants to load a current or fresh game
        if command == "load current":
            pass
        elif command == "load fresh":
            save_location = ""
        else:
            # Sanitize the load name and load the game
            save_location = command[5:]
            save_location = sanitize_filename(save_location)
        maps, player_state, mobs_data, file_not_found = load_game(command, save_location, map_size, region_map_size,
                                                                  maps,
                                                                  player_state,
                                                                  mobs_data)
        if file_not_found:
            state["file_not_found"] = True
        print("Loading")

    # Handle empty commands
    if command == "":
        state['error_msg'] = "Please enter a command"

    # Store the original command in the state dictionary
    state['command'] = command

    # Print the updated state for debugging purposes
    print(state)

    # Return the updated game state and data
    return state, maps, player_state, mobs_data, save_location
