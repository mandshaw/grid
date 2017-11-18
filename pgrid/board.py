import csv
import os
from collections import defaultdict, deque
import operator
from random import shuffle

import yaml
from pgrid.engine import dijsktra

from pgrid.cities import City
from pgrid.components import component_path
from pgrid.powerplant import PowerPlant, ResourceType


class CityNotFound(BaseException):
    pass

class ConnectionNotFound(BaseException):
    pass

class Board(object):
    def __init__(self):
        self.cities = {}
        self.connections = defaultdict(list)
        self.connection_costs = {}
        self.power_plants = []

        with open(os.path.join(component_path, 'cities.yaml'), 'r') as cities_file:
            cities = yaml.load(stream=cities_file)
            for region, cities in cities.items():
                for city in cities:
                    self.register(City(city))
        with open(os.path.join(component_path, 'connections.csv'), 'r') as connections_file:
            connections = csv.reader(connections_file, delimiter=',')
            for connection in connections:
                from_city = connection[0]
                to_city = connection[1]
                cost = connection[2]
                self.add_connection(from_city, to_city, int(cost))

        with open(os.path.join(component_path, 'powerplants.yaml')) as power_plants_file:
            power_plants = yaml.load(stream=power_plants_file)
            for power_plant in power_plants['powerplants']:
                self.power_plants.append(PowerPlant(power_plant['Type'], power_plant['Efficiency'], power_plant['Power'], power_plant['Cost']))


        self.optimal_connection_map = {city: dijsktra(self, city) for city in self.cities.keys()}

    def add_connection(self, from_city, to_city, cost):
        self.connections[from_city].append(to_city)
        self.connections[to_city].append(from_city)
        self.connection_costs[(from_city, to_city)] = cost
        self.connection_costs[(to_city, from_city)] = cost

    def register(self, city):
        self.cities[city.name] = city

    def find(self, name):
        if name in self.cities:
            return self.cities[name]
        else:
            raise CityNotFound('Could not find {city} on board'.format(city=name))

    def get_connection_cost(self, from_city, to_city):
        return self.optimal_connection_map[from_city][to_city]

    def shuffle_power_plants(self):
        power_plants = deque(self.power_plants)
        core = [power_plants.popleft() for i in range(8)]
        # find the Green Power Plant for cost 13. That should be the first card
        for i in range(len(power_plants)):
            if power_plants[i].type == ResourceType.GREEN and power_plants[i].cost == 13:
                first_card = power_plants[i]
                del power_plants[i]
                break
        shuffle(power_plants)
        self.power_plants = list(core) + [first_card] + list(power_plants) + [None]


