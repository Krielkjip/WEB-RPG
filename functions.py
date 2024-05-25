import json
import random
import re

from world_map_gen import run_world_gen
from region_map_gen import run_region_gen


def sanitize_filename(filename: str, replacement: str = '_') -> str:
    # Define a regular expression pattern for invalid filename characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'

    # Remove invalid characters using the regular expression
    sanitized = re.sub(invalid_chars, '', filename)

    # Replace spaces with the specified replacement character
    sanitized = re.sub(r'\s+', replacement, sanitized)

    # Return the sanitized filename
    return sanitized


def create_player_state():
    return {"location": [0, 0], "region_location": [0, 0],
            "inventory": {"logs_amount": 100, "rocks_amount": 100, "planks_amount": 0, "sticks_amount": 0,
                          "wooden_pickaxe_uses": 10, "wooden_axe_uses": 10, "stone_pickaxe_uses": 0,
                          "stone_axe_uses": 0}}


def process_craft(craft, player_state):
    print(craft)
    craft = craft.lower()
    craft = craft[6:]
    message = ""
    fail_message = ""
    print(craft)

    if craft == "planks":
        if player_state["inventory"]["logs_amount"] > 0:
            player_state["inventory"]["logs_amount"] -= 1
            player_state["inventory"]["planks_amount"] += 4
            message = "You crafted 4 planks"
        else:
            fail_message = "You didn't have a log to craft planks"

    elif craft == "sticks":
        if player_state["inventory"]["planks_amount"] > 1:
            player_state["inventory"]["planks_amount"] -= 2
            player_state["inventory"]["sticks_amount"] += 4
            message = "You crafted 4 sticks"
        else:
            fail_message = "You didn't have planks to craft sticks"

    elif craft == "wooden pickaxe uses":
        has_enough_planks = player_state["inventory"]["planks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_planks and has_enough_sticks:
            player_state["inventory"]["planks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["wooden_pickaxe_uses"] += 10
            message = "You crafted 10 wooden pickaxe uses"
        elif not has_enough_planks and not has_enough_sticks:
            fail_message = "You didn't have enough planks and sticks to craft a wooden pickaxe"
        elif not has_enough_planks:
            fail_message = "You didn't have enough planks to craft a wooden pickaxe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a wooden pickaxe"

    elif craft == "wooden axe uses":
        has_enough_planks = player_state["inventory"]["planks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_planks and has_enough_sticks:
            player_state["inventory"]["planks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["wooden_axe_uses"] += 10
            message = "You crafted 10 wooden axe uses"
        elif not has_enough_planks and not has_enough_sticks:
            fail_message = "You didn't have enough planks and sticks to craft a wooden axe"
        elif not has_enough_planks:
            fail_message = "You didn't have enough planks to craft a wooden axe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a wooden axe"

    elif craft == "stone pickaxe uses":
        has_enough_rocks = player_state["inventory"]["rocks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_rocks and has_enough_sticks:
            player_state["inventory"]["rocks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["stone_pickaxe_uses"] += 20
            message = "You crafted 20 stone pickaxe uses"
        elif not has_enough_rocks and not has_enough_sticks:
            fail_message = "You didn't have enough rocks and sticks to craft a stone pickaxe"
        elif not has_enough_rocks:
            fail_message = "You didn't have enough rocks to craft a stone pickaxe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a stone pickaxe"

    elif craft == "stone axe uses":
        has_enough_rocks = player_state["inventory"]["rocks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_rocks and has_enough_sticks:
            player_state["inventory"]["rocks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["stone_axe_uses"] += 20
            message = "You crafted 20 stone axe uses"
        elif not has_enough_rocks and not has_enough_sticks:
            fail_message = "You didn't have enough rocks and sticks to craft a stone axe"
        elif not has_enough_rocks:
            fail_message = "You didn't have enough rocks to craft a stone axe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a stone axe"

    return player_state, message, fail_message


def create_map():
    return {"world_map": [], "region_map": {}}


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


def process_command(command, map_size, region_map_size, map, player_state, mobs_data, save_location):
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
            save_game(save_location, map, player_state, mobs_data)
            print("Saving")
    elif command[:4].lower() == "load":
        if command == "load current":
            pass
        elif command == "load fresh":
            save_location = ""
        else:
            save_location = command[5:]
            save_location = sanitize_filename(save_location)
        map, player_state, mobs_data, file_not_found = load_game(command, save_location, map_size, region_map_size, map,
                                                                 player_state,
                                                                 mobs_data)
        if file_not_found:
            state["file_not_found"] = True
        print("Loading")
    if command == "":
        state['error_msg'] = "Please enter a command"
    state['command'] = command
    print(state)
    return state, map, player_state, mobs_data, save_location


def process_interact(interact, region_map_size, map_size, region_map, map, player_state, mobs_data):
    current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
    biome_data = get_tile_text(current_biome)
    print(biome_data)
    print(interact)
    print(player_state["location"])
    if interact == "Interact Get Region":
        try:
            region_map = map["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"]
        except KeyError:
            current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
            region_map = run_region_gen(region_map_size, region_map_size, current_biome)
            # map["region_map"][f"{player_state["location"][0]}_{player_state["location"][1]}"] = region_map

        # print(region_map)
        # region_map = run_region_gen(region_map_size, region_map_size, current_biome)
        # print("Gen Region Map")
        player_state["region_location"] = [0, 0]
    elif interact[:4].lower() == "move":
        player_state, world_change = move_player(interact, map_size, region_map_size, player_state, "Region")
        if world_change:
            try:
                current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
                biome_data = get_tile_text(current_biome)
                region_map = map["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"]
            except KeyError:
                current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
                biome_data = get_tile_text(current_biome)
                region_map = run_region_gen(region_map_size, region_map_size, current_biome)
        mobs_data = move_mobs(mobs_data, region_map_size, map_size)
    else:
        player_state, region_map = collect_resource(interact, player_state, region_map)
    map["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"] = region_map
    # make writable map
    writable_map = []
    for y in range(len(region_map)):
        writable_map_row = []
        for x in range(len(region_map[y])):
            tile = region_map[y][x]
            mob = False
            # print(mobs_data)
            for item in mobs_data:
                data = mobs_data[item]
                if data["location"][0] == player_state["location"][0] and data["location"][1] == \
                        player_state["location"][1]:
                    if data["region_location"][0] == x and data["region_location"][1] == y:
                        # print(data)
                        mob = True
                        mob_name = data["name"]
                        break
            if mob:
                writable_map_row.append([tile, True, mob_name])
            else:
                writable_map_row.append([tile, False, None])
        writable_map.append(writable_map_row)
    # print(writable_map)

    return writable_map, region_map, player_state, biome_data


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


def collect_resource(interact, player_state, region_map):
    if interact == "Cut Tree":
        player_state["inventory"]["logs_amount"] += 1
        region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Grass"
    elif interact == "Mine Rock":
        player_state["inventory"]["rocks_amount"] += 1
        region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Dirt"
    return player_state, region_map


def get_tile_text(current_tile):
    biome_descriptions = {
        "Taiga Forest": ["Taiga Forest", "You are in a Taiga Forest",
                         "A vast expanse of cold coniferous forest, primarily spruce, fir, and pine, blanketed in snow with frozen lakes and occasional clearings. Home to wolves, foxes, and polar bears adapted to the harsh northern wilderness.",
                         ["Wolves", "Foxes", "Polar Bears"]],
        "Taiga": ["Taiga", "You are in a Taiga",
                  "A cold, snowy landscape dotted with coniferous trees like spruce, fir, and pine. The ground is often covered in snow, with occasional clearings and frozen lakes.",
                  ["Wolves", "Foxes", "Polar Bears"]],
        "Rainforest": ["Rainforest", "You are in a Rainforest",
                       "Lush and dense vegetation with towering trees, vibrant foliage, and a diverse array of wildlife. The air is humid, and sunlight filters through the thick canopy, creating dappled shadows on the forest floor.",
                       ["Jaguars", "Toucans", "Anacondas"]],
        "Grassland": ["Grassland", "You are in the Grasslands",
                      "Wide expanses of rolling grasses, occasionally interspersed with low shrubs and scattered trees. The terrain is relatively flat, with open skies and a sense of vastness.",
                      ["Bison", "Lions", "Hawks"]],
        "Mountain": ["Mountain", "You are on a Mountain",
                     "Towering peaks, rocky slopes, and rugged terrain. Snow-capped summits, deep valleys, and alpine meadows characterize this biome, with breathtaking views and challenging landscapes.",
                     ["Mountain Goats", "Eagles", "Snow Leopards"]],
        "Forest": ["Forest", "You are in a Forest",
                   "Dense growth of trees, both deciduous and coniferous, with a rich underbrush of shrubs, ferns, and mosses. Sunlight filters through the canopy, casting a greenish hue on the forest floor.",
                   ["Deer", "Bears", "Wolves"]],
        "Volcano": ["Volcano", "You are inside a Volcano",
                    "A dramatic landscape dominated by the presence of a volcano, with steaming vents, rugged lava fields, and occasional eruptions. The air is often filled with ash and the ground may be hot to the touch in some areas.",
                    ["Fire Elementals", "Lava Slimes", "Magma Golems"]],
        "Desert": ["Desert", "You are in a Desert",
                   "Arid expanses of sand dunes, rocky outcrops, and sparse vegetation adapted to extreme dryness. The landscape is characterized by intense sunlight, high temperatures during the day, and cold nights.",
                   ["Scorpions", "Vultures", "Camels"]],
        "Ocean": ["Ocean", "You are in a Ocean",
                  "Vast stretches of open water, with varying depths, currents, and marine life. Waves crash against rocky cliffs or gently lap against sandy shores, while seabirds soar overhead and marine mammals swim beneath the surface.",
                  ["Sharks", "Dolphins", "Sea Turtles"]],
        "Temperate Forest": ["Temperate Forest", "You are in a Temperate Forest",
                             "Similar to a forest biome but with a more moderate climate, characterized by a mix of deciduous and evergreen trees. The ground may be covered in a carpet of fallen leaves, and there are clear seasonal changes in foliage color.",
                             ["Squirrels", "Owls", "Raccoons"]],
        "Tundra": ["Tundra", "You are in a Tundra",
                   "A cold and treeless biome with vast expanses of low-lying vegetation, such as mosses, lichens, and hardy grasses. Permafrost underlies much of the landscape, and there are few trees due to the harsh conditions.",
                   ["Polar Bears", "Arctic Foxes", "Caribou"],
                   ["Snow"]],
        "Savanna": ["Savanna", "You are in a Savanna",
                    "Open grasslands dotted with scattered trees and shrubs, characterized by a dry climate with seasonal rainfall. The landscape may include occasional rocky outcrops and grazing herds of animals like zebras and antelope.",
                    ["Lions", "Giraffes", "Elephants"]]
    }

    return biome_descriptions.get(current_tile, None)
