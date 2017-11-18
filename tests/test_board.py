
from unittest import TestCase

from pgrid.board import Board
from pgrid.powerplant import PowerPlant


class TestBoard(TestCase):

    def test_all_cities_connected(self):
        board = Board()
        for city in board.cities.values():
            if city not in board.connections:
                for connection_from, connection_to in board.connection_costs.keys():
                    if board.connections[(connection_from,connection_to)] != board.connections[(connection_to,connection_from)]:
                        self.fail('{name}\'s connection cost to {connected_city} is not the same'.format(name=city.name, connected_city=connected_city))
            else:
                self.fail('Orphaned City: {city}'.format(city=city.name))

    def test_expected_connections(self):
        board = Board()

        expected_connections = {
            'Salt Lake City': 5,
            'Goise': 6,
            'Jacksonville': 4,
            'Chicago': 7,
            'Cincinnati': 6,
            'Billings': 5,
            'Portland': 3,
            'Norfolk': 2,
            'Omaha': 4,
            'Savannah': 3,
            'Denver': 4,
            'Dallas': 5,
            'Boston': 1,
            'San Francisco': 5,
            'Miami': 1,
            'Memphis': 6,
            'San Diego': 3,
            'Phoenix': 3,
            'Los Angeles': 3,
            'Philadelphia': 2,
            'Buffalo': 3,
            'Birmingham': 4,
            'Atlanta': 5,
            'Cheyenne': 5,
            'Tampa': 2,
            'New York': 3,
            'Duluth': 4,
            'Seattle': 3,
            'Kansas City': 7,
            'Houston': 3,
            'Pittsburgh': 5,
            'New Orleans': 5,
            'Santa Fe': 8,
            'St. Louis': 5,
            'Detroit': 5,
            'Fargo': 3,
            'Raleigh': 5,
            'Washington D.C.': 3,
            'Knoxville': 2,
            'Minneapolis': 6,
            'Oklahoma City': 4,
            'Las Vegas': 6
        }

        for city in board.connections.keys():
            if len(board.connections[city]) != expected_connections[city]:
                self.fail('{name} expected connections {expected} does not match {actual}'.format(
                    name=city,
                    expected=expected_connections[city],
                    actual=len(board.connections[city])
                ))

    def test_get_connection_cost(self):
        board = Board()
        cost = board.get_connection_cost('Tampa', 'Santa Fe')
        self.assertEqual(cost, 45)

    def test_board_power_plants(self):
        board = Board()
        for power_plant in board.power_plants:
            self.assertIsInstance(power_plant, PowerPlant)
        self.assertEqual(len(board.power_plants), 42)

    def test_board_shuffle_power_plant(self):
        board = Board()
        board.shuffle_power_plants()
        self.assertEqual(board.power_plants[0].cost, 3)
        self.assertEqual(board.power_plants[1].cost, 4)
        self.assertEqual(board.power_plants[2].cost, 5)
        self.assertEqual(board.power_plants[3].cost, 6)
        self.assertEqual(board.power_plants[4].cost, 7)
        self.assertEqual(board.power_plants[5].cost, 8)
        self.assertEqual(board.power_plants[6].cost, 9)
        self.assertEqual(board.power_plants[7].cost, 10)
        self.assertEqual(board.power_plants[8].cost, 13)
        self.assertFalse(
            board.power_plants[9].cost == 11 and
            board.power_plants[10].cost == 12 and
            board.power_plants[11].cost == 14 and
            board.power_plants[12].cost == 15 and
            board.power_plants[13].cost == 16
        )
        self.assertEqual(board.power_plants[-1], None)
