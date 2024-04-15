import random
from colorama import Fore, Style, init

init()
volcano_amount = 3

biomes = ["Grassland", "Forest", "Mountain", "Ocean", "Desert", "Rainforest", "Temperate Forest", "Tundra", "Taiga",
          "Taiga Forest", "Savanna", "Volcano"]
# Biome characters dictionary with corresponding colors
biome_colors = {
    "Grassland": Fore.LIGHTGREEN_EX,
    "Forest": Fore.GREEN,
    "Mountain": Fore.LIGHTBLACK_EX,
    "Ocean": Fore.CYAN,
    "Desert": Fore.LIGHTYELLOW_EX,
    "Rainforest": Fore.GREEN,
    "Temperate Forest": Fore.GREEN,
    "Tundra": Fore.WHITE,
    "Taiga": Fore.WHITE,
    "Taiga Forest": Fore.WHITE,
    "Savanna": Fore.YELLOW,
    "Volcano": Fore.RED
}

# Biome characters dictionary
biome_characters = {
    "Grassland": "G",
    "Forest": "F",
    "Mountain": "M",
    "Ocean": "O",
    "Desert": "D",
    "Rainforest": "R",
    "Temperate Forest": "W",
    "Tundra": "A",
    "Taiga": "T",
    "Taiga Forest": "C",
    "Savanna": "S",
    "Volcano": "V"
}


def generate_terrain(height, width):
    terrain_weights = {
        "Grassland": 5,
        "Forest": 4,
        "Mountain": 0,
        "Ocean": 4,
        "Desert": 0,
        "Rainforest": 4,
        "Temperate Forest": 3,
        "Tundra": 0,
        "Taiga": 0,
        "Taiga Forest": 0,
        "Savanna": 0,
        "Volcano": 0
    }
    terrain_weights_cold = {
        "Grassland": 0,
        "Forest": 0,
        "Mountain": 6,
        "Ocean": 4,
        "Desert": 0,
        "Rainforest": 0,
        "Temperate Forest": 0,
        "Tundra": 3,
        "Taiga": 6,
        "Taiga Forest": 10,
        "Savanna": 0,
        "Volcano": 0
    }
    terrain_weights_hot = {
        "Grassland": 0,
        "Forest": 0,
        "Mountain": 3,
        "Ocean": 2,
        "Desert": 8,
        "Rainforest": 0,
        "Temperate Forest": 0,
        "Tundra": 0,
        "Taiga": 0,
        "Taiga Forest": 0,
        "Savanna": 4,
        "Volcano": 0
    }

    terrain_types = list(terrain_weights.keys())
    weighted_terrain = []
    for x in range(width):
        row = []
        for y in range(height):
            if y <= height / 4 - 1:
                row.append(random.choices(terrain_types, weights=terrain_weights_cold.values())[0])
            elif y >= height / 4 * 3:
                row.append(random.choices(terrain_types, weights=terrain_weights_hot.values())[0])
            else:
                row.append(random.choices(terrain_types, weights=terrain_weights.values())[0])
        weighted_terrain.append(row)

    for i in range(volcano_amount):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        weighted_terrain[x][y] = "Volcano"
    # print(weighted_terrain)
    return weighted_terrain


# Function to display the terrain grid
def display_terrain(terrain_grid, height, width):
    for y in range(height):
        for x in range(width):
            print(biome_colors[terrain_grid[x][y]] + biome_characters[terrain_grid[x][y]], end=" ")
        print(Style.RESET_ALL)


def count(neighbors, what_biome):
    return sum(1 for neighbor in neighbors if neighbor == what_biome)


def modify_biome(new_biome, neighbors, percent_chance):
    biome_count = count(neighbors, new_biome)
    if biome_count > 0:
        probability = min(percent_chance + (percent_chance * (biome_count - 1)),
                          (percent_chance * 4))  # Adjusted probability
        random_number = random.randint(1, 100)
        if random_number <= 100:
            return True


# Function to modify terrain based on certain conditions
def modify_terrain(terrain_grid, height, width):
    for x in range(width):
        for y in range(height):
            current_biome = terrain_grid[x][y]
            neighbors = [
                terrain_grid[(x + 1) % width][y],
                terrain_grid[(x - 1) % width][y],
                terrain_grid[x][(y + 1) % height],
                terrain_grid[x][(y - 1) % height]
            ]

            # Check conditions for each biome
            if current_biome == biomes[0]:
                new_biome = biomes[3]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[1]:
                new_biome = biomes[2]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[2]:
                new_biome = biomes[1]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[3]:
                new_biome = biomes[0]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[4]:
                new_biome = biomes[10]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[5]:
                new_biome = biomes[3]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[6]:
                new_biome = biomes[5]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[7]:
                new_biome = biomes[9]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[8]:
                new_biome = biomes[7]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[9]:
                new_biome = biomes[8]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[10]:
                new_biome = biomes[4]
                if modify_biome(new_biome, neighbors, 0.1):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[11]:
                pass

            if "Volcano" in neighbors:
                random_number = random.randint(1, 100)
                if random_number <= 100:
                    terrain_grid[x][y] = "Mountain"


# Main function to generate, modify and display terrain
def main(height, width):
    terrain_grid = generate_terrain(height, width)
    # display_terrain(terrain_grid)
    for x in range(1):
        modify_terrain(terrain_grid, height, width)
        # print("\nTerrain Map after Modification:")
        # display_terrain(terrain_grid, height, width)
        # print("\nTerrain Map as a List:")

    return terrain_grid


def run_world_gen(height, width):
    world_map = main(height, width)
    # print(world_map)
    return world_map
