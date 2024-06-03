from .tile_text import get_tile_text
from map_gen.region_map_gen import run_region_gen
from .move import move_player, move_mobs
from .collect_resource import collect_resource


def process_interact(interact, region_map_size, map_size, region_map, maps, player_state, mobs_data):
    """
    Process an interaction command and update the game state accordingly.

    Args:
        interact (str): The interaction command (e.g. "Interact Get Region")
        region_map_size (int): The size of the region map
        map_size (int): The size of the game map
        region_map (list): The current region map
        maps (dict): The game maps
        player_state (dict): The current player state
        mobs_data (dict): The current mob data

    Returns:
        writable_map (list): The updated region map with mob information
        region_map (list): The updated region map
        player_state (dict): The updated player state
        biome_data (str): The biome data for the current location
        message (str): A success message if the interaction was successful
        fail_message (str): An error message if the interaction failed
    """
    message = ""
    fail_message = ""
    current_biome = maps["world_map"][player_state["location"][0]][player_state["location"][1]]
    biome_data = get_tile_text(current_biome)
    print(biome_data)
    print(interact)
    print(player_state["location"])

    if interact == "Interact Get Region":
        # Get the region map for the current location
        try:
            region_map = maps["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"]
        except KeyError:
            # Generate a new region map if it doesn't exist
            current_biome = maps["world_map"][player_state["location"][0]][player_state["location"][1]]
            region_map = run_region_gen(region_map_size, region_map_size, current_biome)
        player_state["region_location"] = [0, 0]

    elif interact[:4].lower() == "move":
        # Move the player to a new location
        player_state, world_change = move_player(interact, map_size, region_map_size, player_state, "Region")
        if world_change:
            # Update the biome data and region map if the player moved to a new location
            try:
                current_biome = maps["world_map"][player_state["location"][0]][player_state["location"][1]]
                biome_data = get_tile_text(current_biome)
                region_map = maps["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"]
            except KeyError:
                current_biome = maps["world_map"][player_state["location"][0]][player_state["location"][1]]
                biome_data = get_tile_text(current_biome)
                region_map = run_region_gen(region_map_size, region_map_size, current_biome)
        # Move mobs to new locations
        mobs_data = move_mobs(mobs_data, region_map_size, map_size)

    else:
        # Collect resources at the current location
        player_state, region_map, message, fail_message = collect_resource(interact, player_state, region_map)

    # Update the region map and player state
    maps["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"] = region_map
    writable_map = []
    for y in range(len(region_map)):
        writable_map_row = []
        for x in range(len(region_map[y])):
            tile = region_map[y][x]
            mob = False
            mob_name = None
            for item in mobs_data:
                data = mobs_data[item]
                if data["location"][0] == player_state["location"][0] and data["location"][1] == \
                        player_state["location"][1]:
                    if data["region_location"][0] == x and data["region_location"][1] == y:
                        mob = True
                        mob_name = data["name"]
                        break
            if mob:
                writable_map_row.append([tile, True, mob_name])
            else:
                writable_map_row.append([tile, False, None])
        writable_map.append(writable_map_row)

    return writable_map, region_map, player_state, biome_data, message, fail_message
