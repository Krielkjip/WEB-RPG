import random


def move_mobs(mobs_data, region_map_size, map_size):
    print(mobs_data)
    for item in mobs_data:
        data = mobs_data[item]
        x_world = data["location"][0]
        y_world = data["location"][1]
        x_region = data["region_location"][0]
        y_region = data["region_location"][1]
        random_number = random.randint(0, 3)
        if random_number == 0:
            if y_region < region_map_size - 1:
                y_region += 1
            else:
                if y_world < map_size - 1:
                    y_world += 1
                    y_region = 0
        elif random_number == 1:
            if x_region < region_map_size - 1:
                x_region += 1
            else:
                if x_world < map_size - 1:
                    x_world += 1
                    x_region = 0
        elif random_number == 2:
            if x_region > 0:
                x_region -= 1
            else:
                if x_world > 0:
                    x_world -= 1
                    x_region = region_map_size - 1
        elif random_number == 3:
            if y_region > 0:
                y_region -= 1
            else:
                if y_world > 0:
                    y_world -= 1
                    y_region = region_map_size - 1
        mobs_data[item]["location"] = [x_world, y_world]
        mobs_data[item]["region_location"] = [x_region, y_region]
    print(mobs_data)
    return mobs_data


def move_player(move, map_size, region_map_size, player_state, where):
    world_change = False
    move = move.lower()
    if where == "World":
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
        location_world = player_state['location']
        location_region = player_state['region_location']
        if move == "move down":
            print("Moving down")
            if location_region[1] < region_map_size - 1:
                location_region[1] += 1
            else:
                if location_world[1] < map_size - 1:
                    location_world[1] += 1
                    location_region[1] = 0
                    world_change = True
        elif move == "move up":
            print("Moving up")
            if location_region[1] > 0:
                location_region[1] -= 1
            else:
                if location_world[1] > 0:
                    location_world[1] -= 1
                    location_region[1] = region_map_size - 1
                    world_change = True
        elif move == "move right":
            print("Moving right")
            if location_region[0] < region_map_size - 1:
                location_region[0] += 1
            else:
                if location_world[0] < map_size - 1:
                    location_world[0] += 1
                    location_region[0] = 0
                    world_change = True
        elif move == "move left":
            print("Moving left")
            if location_region[0] > 0:
                location_region[0] -= 1
            else:
                if location_world[0] > 0:
                    location_world[0] -= 1
                    location_region[0] = region_map_size - 1
                    world_change = True
        player_state["location"] = location_world
        player_state["region_location"] = location_region
    return player_state, world_change
