import random


def move_mobs(mobs_data, region_map_size, map_size):
    """
    Moves mobs randomly in the game world.

    Args:
        mobs_data (dict): A dictionary of mobs with their locations and region locations
        region_map_size (int): The size of the region map
        map_size (int): The size of the overall game map

    Returns:
        dict: The updated mobs data with new locations
    """
    print(mobs_data)
    for item in mobs_data:
        data = mobs_data[item]
        x_world = data["location"][0]
        y_world = data["location"][1]
        x_region = data["region_location"][0]
        y_region = data["region_location"][1]

        # Randomly choose a direction to move (0: down, 1: right, 2: left, 3: up)
        random_number = random.randint(0, 3)

        if random_number == 0:
            # Move down
            if y_region < region_map_size - 1:
                y_region += 1
            else:
                if y_world < map_size - 1:
                    y_world += 1
                    y_region = 0
        elif random_number == 1:
            # Move right
            if x_region < region_map_size - 1:
                x_region += 1
            else:
                if x_world < map_size - 1:
                    x_world += 1
                    x_region = 0
        elif random_number == 2:
            # Move left
            if x_region > 0:
                x_region -= 1
            else:
                if x_world > 0:
                    x_world -= 1
                    x_region = region_map_size - 1
        elif random_number == 3:
            # Move up
            if y_region > 0:
                y_region -= 1
            else:
                if y_world > 0:
                    y_world -= 1
                    y_region = region_map_size - 1

        # Update the mob's location and region location
        mobs_data[item]["location"] = [x_world, y_world]
        mobs_data[item]["region_location"] = [x_region, y_region]

    print(mobs_data)
    return mobs_data


def move_player(move, map_size, region_map_size, player_state, where):
    """
    Moves the player in the game world.

    Args:
        move (str): The direction to move (e.g. "move down", "move up", etc.)
        map_size (int): The size of the overall game map
        region_map_size (int): The size of the region map
        player_state (dict): The player's current state
        where (str): The scope of the move (either "World" or "Region")

    Returns:
        tuple: The updated player state and a boolean indicating if the world changed
    """
    world_change = False
    move = move.lower()

    if where == "World":
        # Move the player in the world
        location = player_state['location']
        if move == "move down":
            print("Moving down")
            if location[1] < map_size - 1:
                location[1] += 1
        elif move == "move up":
            print("Moving up")
            if location[1] > 0:
                location[1] -= 1
        elif move == "move right":
            print("Moving right")
            if location[0] < map_size - 1:
                location[0] += 1
        elif move == "move left":
            print("Moving left")
            if location[0] > 0:
                location[0] -= 1
        player_state["location"] = location
    elif where == "Region":
        # Move the player in the region
        location_world = player_state['location']
        location_region = player_state['region_location']
        if move == "move down":
            print("Moving down")
            # Check if player crossed a region boarder
            if location_region[1] < region_map_size - 1:
                location_region[1] += 1
            else:
                # Wrap around to the top of the region
                if location_world[1] < map_size - 1:
                    location_world[1] += 1
                    location_region[1] = 0
                    world_change = True
        elif move == "move up":
            print("Moving up")
            # Check if player crossed a region boarder
            if location_region[1] > 0:
                location_region[1] -= 1
            else:
                # Wrap around to the bottom of the region
                if location_world[1] > 0:
                    location_world[1] -= 1
                    location_region[1] = region_map_size - 1
                    world_change = True
        elif move == "move right":
            print("Moving right")
            # Check if player crossed a region boarder
            if location_region[0] < region_map_size - 1:
                location_region[0] += 1
            else:
                # Wrap around to the left of the region
                if location_world[0] < map_size - 1:
                    location_world[0] += 1
                    location_region[0] = 0
                    world_change = True
        elif move == "move left":
            print("Moving left")
            # Check if player crossed a region boarder
            if location_region[0] > 0:
                location_region[0] -= 1
            else:
                # Wrap around to the right of the region
                if location_world[0] > 0:
                    location_world[0] -= 1
                    location_region[0] = region_map_size - 1
                    world_change = True
        # Update player location
        player_state["location"] = location_world
        player_state["region_location"] = location_region
    return player_state, world_change
