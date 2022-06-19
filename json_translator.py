import json

from pokete_data import *


def translate():
    data = [weathers, achievements, pokes, types,
            map_data, stations, items, npcs, attacks, maps]

    json_files = ['weather.json', 'achievements.json', 'poketes.json', 'types.json',
                  'map_data.json', 'stations.json', 'items.json', 'npcs.json', 'attacks.json', 'maps.json']

    files = zip(data, json_files)
    for data, file in files:
        with open('pokete_data/json_data/' + file, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    print("\033[31;1mUpdating data in JSON files!\033[0m")
    translate()
