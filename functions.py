import json
from world_map_gen import run_world_gen


def create_player_state():
    return {"location": [0, 0], "inventory": {"logs_amount": 0, "rocks_amount": 0}}


def save_game(command, map, player_state):
    file_location = "save_data/" + command[5:] + ".json"
    with open(file_location, 'w') as json_file:
        json.dump([map, player_state], json_file)
        print("SAVED DATA")


def load_game(command, map_size, map, player_state):
    if command == "load current":
        return map, player_state, False
    elif command == "load fresh":
        map = run_world_gen(map_size, map_size)
        player_state = create_player_state()
        return map, player_state, False
    else:
        try:
            if command[-5:] == ".json":
                file_location = "save_data/" + command[5:]
            else:
                file_location = "save_data/" + command[5:] + ".json"
            print(file_location)
            with open(file_location, 'r') as json_file:
                data = json.load(json_file)
                map = data[0]
                player_state = data[1]
                return map, player_state, False
        except FileNotFoundError:
            return map, player_state, True


def process_command(command, map_size, map, player_state):
    player_state = move_player(command, map_size, player_state, "World")
    state = {"command_len": len(command)}
    if command[:4].lower() == "save":
        save_game(command, map, player_state)
        print("Saving")
    elif command[:4].lower() == "load":
        map, player_state, file_not_found = load_game(command, map_size, map, player_state)
        if file_not_found:
            state["file_not_found"] = True
        print("Loading")
    if command == "":
        state['error_msg'] = "Please enter a command"
    state['command'] = command
    print(state)
    return state, map, player_state


def move_player(move, map_size, player_state, where):
    move = move.lower()
    if where == "World":
        location = player_state['location']
    else:
        location = player_state['region_location']
    if move == "down":
        print("Moving down")
        if location[1] < map_size - 1:
            location[1] += 1
    elif move == "up":
        print("Moving up")
        if location[1] > 0:
            location[1] -= 1
    elif move == "right":
        print("Moving right")
        if location[0] < map_size - 1:
            location[0] += 1
    elif move == "left":
        print("Moving left")
        if location[0] > 0:
            location[0] -= 1
    if where == "World":
        player_state["location"] = location
    else:
        player_state["region_location"] = location
    return player_state


def collect_resource(interact, player_state, region_map):
    if interact == "Cut Tree":
        player_state["inventory"]["logs_amount"] += 1
        region_map[player_state["region_location"][0]][player_state["region_location"][1]] = "Grass"
    elif interact == "Mine Rock":
        player_state["inventory"]["rocks_amount"] += 1
        region_map[player_state["region_location"][0]][player_state["region_location"][1]] = "Dirt"
    return player_state, region_map


def get_tile_text(current_tile):
    biome_descriptions = {
        "Taiga Forest": ["Taiga Forest", "You are in a Taiga Forest",
                         "A vast expanse of cold coniferous forest, primarily spruce, fir, and pine, blanketed in snow with frozen lakes and occasional clearings. Home to wolves, foxes, and polar bears adapted to the harsh northern wilderness.",
                         ["Wolves", "Foxes", "Polar Bears"],
                         ["Tree", "Grass"]],
        "Taiga": ["Taiga", "You are in a Taiga",
                  "A cold, snowy landscape dotted with coniferous trees like spruce, fir, and pine. The ground is often covered in snow, with occasional clearings and frozen lakes.",
                  ["Wolves", "Foxes", "Polar Bears"],
                  ["Tree", "Grass"]],
        "Rainforest": ["Rainforest", "You are in a Rainforest",
                       "Lush and dense vegetation with towering trees, vibrant foliage, and a diverse array of wildlife. The air is humid, and sunlight filters through the thick canopy, creating dappled shadows on the forest floor.",
                       ["Jaguars", "Toucans", "Anacondas"],
                       ["Tree", "Grass"]],
        "Grassland": ["Grassland", "You are in the Grasslands",
                      "Wide expanses of rolling grasses, occasionally interspersed with low shrubs and scattered trees. The terrain is relatively flat, with open skies and a sense of vastness.",
                      ["Bison", "Lions", "Hawks"],
                      ["Grass"]],
        "Mountain": ["Mountain", "You are on a Mountain",
                     "Towering peaks, rocky slopes, and rugged terrain. Snow-capped summits, deep valleys, and alpine meadows characterize this biome, with breathtaking views and challenging landscapes.",
                     ["Mountain Goats", "Eagles", "Snow Leopards"],
                     ["Rock", "Snow"]],
        "Forest": ["Forest", "You are in a Forest",
                   "Dense growth of trees, both deciduous and coniferous, with a rich underbrush of shrubs, ferns, and mosses. Sunlight filters through the canopy, casting a greenish hue on the forest floor.",
                   ["Deer", "Bears", "Wolves"],
                   ["Tree", "Grass"]],
        "Volcano": ["Volcano", "You are inside a Volcano",
                    "A dramatic landscape dominated by the presence of a volcano, with steaming vents, rugged lava fields, and occasional eruptions. The air is often filled with ash and the ground may be hot to the touch in some areas.",
                    ["Fire Elementals", "Lava Slimes", "Magma Golems"],
                    ["Lava"]],
        "Desert": ["Desert", "You are in a Desert",
                   "Arid expanses of sand dunes, rocky outcrops, and sparse vegetation adapted to extreme dryness. The landscape is characterized by intense sunlight, high temperatures during the day, and cold nights.",
                   ["Scorpions", "Vultures", "Camels"],
                   ["Sand"]],
        "Ocean": ["Ocean", "You are in a Ocean",
                  "Vast stretches of open water, with varying depths, currents, and marine life. Waves crash against rocky cliffs or gently lap against sandy shores, while seabirds soar overhead and marine mammals swim beneath the surface.",
                  ["Sharks", "Dolphins", "Sea Turtles"],
                  ["Water"]],
        "Temperate Forest": ["Temperate Forest", "You are in a Temperate Forest",
                             "Similar to a forest biome but with a more moderate climate, characterized by a mix of deciduous and evergreen trees. The ground may be covered in a carpet of fallen leaves, and there are clear seasonal changes in foliage color.",
                             ["Squirrels", "Owls", "Raccoons"],
                             ["Tree"]],
        "Tundra": ["Tundra", "You are in a Tundra",
                   "A cold and treeless biome with vast expanses of low-lying vegetation, such as mosses, lichens, and hardy grasses. Permafrost underlies much of the landscape, and there are few trees due to the harsh conditions.",
                   ["Polar Bears", "Arctic Foxes", "Caribou"],
                   ["Snow"]],
        "Savanna": ["Savanna", "You are in a Savanna",
                    "Open grasslands dotted with scattered trees and shrubs, characterized by a dry climate with seasonal rainfall. The landscape may include occasional rocky outcrops and grazing herds of animals like zebras and antelope.",
                    ["Lions", "Giraffes", "Elephants"],
                    ["Grass"]]
    }

    return biome_descriptions.get(current_tile, None)
