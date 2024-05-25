import json
import random
from world_map_gen import run_world_gen
from .create_state import create_player_state, create_map


def save_game(save_location, map, player_state, mobs_data):
    if save_location[-5:] == ".json":
        file_location = "save_data/" + save_location
    else:
        file_location = "save_data/" + save_location + ".json"
    with open(file_location, 'w') as json_file:
        json.dump([map, mobs_data, player_state], json_file)
        print("SAVED DATA")


def load_game(command, save_location, map_size, region_map_size, map, player_state, mobs_data):
    if command == "load current":
        return map, player_state, mobs_data, False
    elif command == "load fresh":
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
        map = create_map()
        map["world_map"] = run_world_gen(map_size, map_size)
        # for x in range(map_size):
        #     for y in range(map_size):
        #         current_biome = map["world_map"][x][y]
        #         current_region = run_region_gen(map_size, map_size, current_biome)
        #         map["region_map"][f"{x}_{y}"] = current_region
        return map, player_state, mobs_data, False
    else:
        try:
            if save_location[-5:] == ".json":
                file_location = "save_data/" + save_location
            else:
                file_location = "save_data/" + save_location + ".json"
            print(file_location)
            with open(file_location, 'r') as json_file:
                data = json.load(json_file)
                map = data[0]
                player_state = data[2]
                mobs_data = data[1]
                return map, player_state, mobs_data, False
        except FileNotFoundError:
            return map, player_state, mobs_data, True
