def get_tile_text(current_tile):
    biome_descriptions = {
        "Taiga Forest": ["Taiga Forest", "You are in a Taiga Forest",
                         "A vast expanse of cold coniferous forest, primarily spruce, fir, and pine, blanketed in "
                         "snow with frozen lakes and occasional clearings. Home to wolves, foxes, and polar bears "
                         "adapted to the harsh northern wilderness.",
                         ["Wolves", "Foxes", "Polar Bears"]],
        "Taiga": ["Taiga", "You are in a Taiga",
                  "A cold, snowy landscape dotted with coniferous trees like spruce, fir, and pine. The ground is "
                  "often covered in snow, with occasional clearings and frozen lakes.",
                  ["Wolves", "Foxes", "Polar Bears"]],
        "Rainforest": ["Rainforest", "You are in a Rainforest",
                       "Lush and dense vegetation with towering trees, vibrant foliage, and a diverse array of "
                       "wildlife. The air is humid, and sunlight filters through the thick canopy, creating dappled "
                       "shadows on the forest floor.",
                       ["Jaguars", "Toucans", "Anacondas"]],
        "Grassland": ["Grassland", "You are in the Grasslands",
                      "Wide expanses of rolling grasses, occasionally interspersed with low shrubs and scattered "
                      "trees. The terrain is relatively flat, with open skies and a sense of vastness.",
                      ["Bison", "Lions", "Hawks"]],
        "Mountain": ["Mountain", "You are on a Mountain",
                     "Towering peaks, rocky slopes, and rugged terrain. Snow-capped summits, deep valleys, and alpine "
                     "meadows characterize this biome, with breathtaking views and challenging landscapes.",
                     ["Mountain Goats", "Eagles", "Snow Leopards"]],
        "Forest": ["Forest", "You are in a Forest",
                   "Dense growth of trees, both deciduous and coniferous, with a rich underbrush of shrubs, ferns, "
                   "and mosses. Sunlight filters through the canopy, casting a greenish hue on the forest floor.",
                   ["Deer", "Bears", "Wolves"]],
        "Volcano": ["Volcano", "You are inside a Volcano",
                    "A dramatic landscape dominated by the presence of a volcano, with steaming vents, rugged lava "
                    "fields, and occasional eruptions. The air is often filled with ash and the ground may be hot to "
                    "the touch in some areas.",
                    ["Fire Elementals", "Lava Slimes", "Magma Golems"]],
        "Desert": ["Desert", "You are in a Desert",
                   "Arid expanses of sand dunes, rocky outcrops, and sparse vegetation adapted to extreme dryness. "
                   "The landscape is characterized by intense sunlight, high temperatures during the day, "
                   "and cold nights.",
                   ["Scorpions", "Vultures", "Camels"]],
        "Ocean": ["Ocean", "You are in a Ocean",
                  "Vast stretches of open water, with varying depths, currents, and marine life. Waves crash against "
                  "rocky cliffs or gently lap against sandy shores, while seabirds soar overhead and marine mammals "
                  "swim beneath the surface.",
                  ["Sharks", "Dolphins", "Sea Turtles"]],
        "Temperate Forest": ["Temperate Forest", "You are in a Temperate Forest",
                             "Similar to a forest biome but with a more moderate climate, characterized by a mix of "
                             "deciduous and evergreen trees. The ground may be covered in a carpet of fallen leaves, "
                             "and there are clear seasonal changes in foliage color.",
                             ["Squirrels", "Owls", "Raccoons"]],
        "Tundra": ["Tundra", "You are in a Tundra",
                   "A cold and treeless biome with vast expanses of low-lying vegetation, such as mosses, lichens, "
                   "and hardy grasses. Permafrost underlies much of the landscape, and there are few trees due to the "
                   "harsh conditions.",
                   ["Polar Bears", "Arctic Foxes", "Caribou"],
                   ["Snow"]],
        "Savanna": ["Savanna", "You are in a Savanna",
                    "Open grasslands dotted with scattered trees and shrubs, characterized by a dry climate with "
                    "seasonal rainfall. The landscape may include occasional rocky outcrops and grazing herds of "
                    "animals like zebras and antelope.",
                    ["Lions", "Giraffes", "Elephants"]]
    }

    return biome_descriptions.get(current_tile, None)
