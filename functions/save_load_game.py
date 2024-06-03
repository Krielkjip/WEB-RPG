import json
import random
from map_gen.world_map_gen import run_world_gen
from .create_state import create_player_state, create_map


def save_game(save_location, map_data, player_state, mobs_data):
    """
    Saves the game data to a JSON file.

    Args:
        save_location (str): The location where the game data will be saved.
        map_data (dict): The map data.
        player_state (dict): The player's state.
        mobs_data (dict): The data for the mobs in the game.

    Returns:
        None
    """

    # Check if the save location has a .json extension. If not, add it.
    if save_location[-5:] == ".json":
        file_location = "save_data/" + save_location
    else:
        file_location = "save_data/" + save_location + ".json"

    # Open the file in write mode and create a JSON file.
    with open(file_location, 'w') as json_file:
        # Dump the game data into the JSON file.
        json.dump([map_data, mobs_data, player_state], json_file)
        print("SAVED DATA")


def load_game(command, save_location, map_size, region_map_size, map_data, player_state, mobs_data):
    """
    Loads the game data from a JSON file.

    Args:
        command (str): The command to load the game. Can be "load current", "load fresh", or any other command.
        save_location (str): The location of the save file.
        map_size (int): The size of the map.
        region_map_size (int): The size of the region map.
        map_data (dict): The map data.
        player_state (dict): The player's state.
        mobs_data (dict): The data for the mobs in the game.

    Returns:
        tuple: A tuple containing the loaded map data, player state,
        mobs data, and a boolean indicating whether the load was successful.
    """

    # Check the command to determine what to do.
    if command == "load current":
        # Return the current game data.
        return map_data, player_state, mobs_data, False
    elif command == "load fresh":
        # Reset the game data.
        player_state = create_player_state()
        mobs_data = {}
        mob_id = 0
        for x in range(map_size):
            for y in range(map_size):
                random_x = random.randint(0, region_map_size - 1)
                random_y = random.randint(0, region_map_size - 1)
                mobs_data[mob_id] = {"name": "Chicken", "location": [x, y], "region_location": [random_x, random_y]}
                mob_id += 1
        print(mobs_data)
        map_data = create_map()
        map_data["world_map"] = run_world_gen(map_size, map_size)
        return map_data, player_state, mobs_data, False
    else:
        try:
            # Check if the save location has a .json extension. If not, add it.
            if save_location[-5:] == ".json":
                file_location = "save_data/" + save_location
            else:
                file_location = "save_data/" + save_location + ".json"

            # Open the file in read mode and load the JSON data.
            with open(file_location, 'r') as json_file:
                data = json.load(json_file)
                map_data = data[0]
                player_state = data[2]
                mobs_data = data[1]
                return map_data, player_state, mobs_data, False
        except FileNotFoundError:
            # Return the current game data if the file is not found.
            return map_data, player_state, mobs_data, True
