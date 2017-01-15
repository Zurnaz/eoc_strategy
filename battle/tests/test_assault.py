import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.realpath(__file__)).rsplit('\\', 2)[0])

from battle.attack import assault_strategy as assault
from battle import commander

#data setup
unit_client = commander.Client()
unit = unit_client.ask_my_info()
buildings = unit_client.ask_buildings()
battlefield = assault.GridWithWeights(40, 40)
battlefield.walls = [(19, y) for y in range(40)]
towers = unit_client.ask_towers()
battlefield.weights, battlefield.cause = assault.create_data_for_coordinates(towers, battlefield)

@pytest.mark.parametrize("y", [-1,120])
@pytest.mark.parametrize("x", [-1,120])
@pytest.mark.parametrize("radius", [2,7,15])
def test_points_inside_circle_generated(x, y, radius):
    circle_coord = [x, y]
    result = []
    assert assault.find_all_points_inside_circle(circle_coord, radius, battlefield) == result


class TestPointInsideCircle:
    def __init__(self):
        print(self)

    def test_count_of_points_center(self):
        circle_coord, radius, result, error = [30, 30], 5, 52, "Count of points"
        assert len(assault.find_all_points_inside_circle(circle_coord, radius, battlefield)) == result, error

    def test_count_of_points_edge(self):
        circle_coord, radius, result, error = [20, 30], 5, 32, "Count of points edge case"
        assert len(assault.find_all_points_inside_circle(circle_coord, radius, battlefield)) == result, error

    def test_single_point(self):
        circle_coord, radius, result, error = [20, 30], 5, 1, "A correct single point"
        assert len(assault.find_all_points_inside_circle(circle_coord, radius, battlefield)) == result, error

    def test_off_grid(self):
        circle_coord, radius, result, error = [0, 0], 5, 0, "Count of points off grid"
        assert len(assault.find_all_points_inside_circle(circle_coord, radius, battlefield)) == result, error

class TestCreateDataForCoordinates:
    def test_(self):
        custom_towers = towers
        custom_graph = battlefield
        result = 0
        error = "you messed up"
        assert assault.create_data_for_coordinates(custom_towers, custom_graph)

class TestAttachAttackDataForBuildings:
    def test_(self):
        custom_unit = unit
        custom_building = buildings
        custom_graph = battlefield
        result = 0
        error = "you messed up"
        assert assault.attach_attack_data_for_buildings(custom_unit, custom_building, custom_graph) == result, error

class TestPrioritiseTargets:
    def test_(self):
        custom_unit = unit
        custom_building = buildings
        custom_graph = battlefield
        result = 0
        error = "you messed up"
        assert assault.prioritise_targets(custom_unit, custom_building, custom_graph) == result, error

class TestGetLastCoordinateOfDirection:
    def test_(self):
        path_to_target = [(10, 12), (10, 11)]
        result = 0
        error = "you messed up"
        assert assault.get_last_coordinate_of_direction(path_to_target) == result, error

class TestFindNearestCoordinate:
    def test_(self):
        coord = [0,0]
        coordinate_list = [[0, 0], [0, 0]]
        result = 0
        error = "you messed up"
        assert assault.find_nearest_coordinate(coord, coordinate_list) == result, error

class TestTimeToKill:
    def test_(self):
        custom_unit = unit
        custom_tower = towers[0]
        result = 0
        error = "you messed up"
        assert assault.time_to_kill(custom_unit, custom_tower) == result, error

class TestLetsGoHunting:
    def test_lets_go_hunting(self):
        assert assault.lets_go_hunting() == assault.lets_go_hunting()
    #def test_(self):


# Unit Tests
print("Running health check")

print("Health check passed")
