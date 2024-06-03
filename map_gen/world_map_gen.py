import random

# The number of volcanoes to generate
volcano_amount = 3

# List of biomes
biomes = ["Grassland", "Forest", "Mountain", "Ocean", "Desert", "Rainforest", "Temperate Forest", "Tundra", "Taiga",
          "Taiga Forest", "Savanna", "Volcano"]


def generate_terrain(height, width):
    """
    Generates a 2D grid of terrain types.

    Args:
        height (int): The height of the grid.
        width (int): The width of the grid.

    Returns:
        list: A 2D list of terrain types.
    """
    # Weights for each biome
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
            # Generate random terrain based on y-coordinate
            if y <= height / 4 - 1:
                row.append(random.choices(terrain_types, weights=list(terrain_weights_cold.values()))[0])
            elif y >= height / 4 * 3:
                row.append(random.choices(terrain_types, weights=list(terrain_weights_hot.values()))[0])
            else:
                row.append(random.choices(terrain_types, weights=list(terrain_weights.values()))[0])
        weighted_terrain.append(row)

    # Randomly place volcanoes
    for i in range(volcano_amount):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        weighted_terrain[x][y] = "Volcano"
    return weighted_terrain


def count(neighbors, what_biome):
    """
    Counts the number of neighbors that match a certain biome.

    Args:
        neighbors (list): A list of neighboring biomes.
        what_biome (str): The biome to count.

    Returns:
        int: The count of neighboring biomes that match what_biome.
    """
    return sum(1 for neighbor in neighbors if neighbor == what_biome)


def modify_biome(new_biome, neighbors):
    """
    Checks if a biome should be modified based on its neighbors.

    Args:
        new_biome (str): The new biome to check.
        neighbors (list): A list of neighboring biomes.

    Returns:
        bool: True if the biome should be modified, False otherwise.
    """
    percent_chance = 25
    biome_count = count(neighbors, new_biome)
    if biome_count > 0:
        probability = min(percent_chance + (percent_chance * (biome_count - 1)),
                          (percent_chance * 4))  # Adjusted probability
        random_number = random.randint(1, 100)
        if random_number <= probability:
            return True


def modify_terrain(terrain_grid, height, width):
    """
    Modifies the terrain grid based on certain conditions.

    Args:
        terrain_grid (list): The 2D list of terrain types.
        height (int): The height of the grid.
        width (int): The width of the grid.
    """
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
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[1]:
                new_biome = biomes[2]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[2]:
                new_biome = biomes[1]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[3]:
                new_biome = biomes[0]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[4]:
                new_biome = biomes[10]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[5]:
                new_biome = biomes[3]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[6]:
                new_biome = biomes[5]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[7]:
                new_biome = biomes[9]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[8]:
                new_biome = biomes[7]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[9]:
                new_biome = biomes[8]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[10]:
                new_biome = biomes[4]
                if modify_biome(new_biome, neighbors):
                    terrain_grid[x][y] = new_biome
            if current_biome == biomes[11]:
                pass

            if "Volcano" in neighbors:
                random_number = random.randint(1, 100)
                if random_number <= 100:
                    terrain_grid[x][y] = "Mountain"


# Main function to generate, modify and display terrain
def main(height, width):
    """
    Generates, modifies and displays terrain.

    Args:
        height (int): The height of the grid.
        width (int): The width of the grid.

    Returns:
        list: The modified terrain grid.
    """
    terrain_grid = generate_terrain(height, width)
    for x in range(1):
        modify_terrain(terrain_grid, height, width)

    return terrain_grid


def run_world_gen(height, width):
    """
    Runs the world generation process.

    Args:
        height (int): The height of the grid.
        width (int): The width of the grid.

    Returns:
        list: The modified terrain grid.
    """
    world_map = main(height, width)
    return world_map
