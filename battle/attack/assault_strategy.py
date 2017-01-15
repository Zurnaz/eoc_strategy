'''
Assualt strategy based on a weighted graph with addtional path finding applied to it
'''
'''
imports for testing only
''
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)).rsplit('\\', 2)[0])
#'''
'''
General imports
'''
from functools import partial
import heapq
#from implementation import
'''
custom EOC imports
'''
from battle import commander
from attack import implementation_refactoed




def point_inside_circle(point_coord, circle_coord, circle_radius):
    '''
    Checks if a coordinate is inside a circle
    useful for ideniftying if a tower can hit a unit
    '''
    x, y = point_coord
    circle_x, circle_y = circle_coord
    result = (x - circle_x)**2 + (y - circle_y)**2 <= circle_radius**2
    return result

def find_all_points_inside_circle(circle_coord, radius, graph):
    '''
    finds all the points inside a circle, it is a multiple version of point_inside_circle
    '''
    result = []
    circle_x = circle_coord[0]
    circle_y = circle_coord[1]
    min_x = 20
    min_y = 0
    max_x = graph.width
    max_y = graph.height
    x = circle_x - radius
    y = circle_y - radius
    while x <= circle_x:
        while y <= circle_y:
            if (x - circle_x)**2 + (y - circle_y)**2 <= radius**2:
                x_sym = circle_x - (x - circle_x)
                y_sym = circle_y - (y - circle_y)
                if x >= min_x and y >= min_y and x <= max_x and y <= max_y:
                    result.append([x, y])
                if x_sym >= min_x and y_sym >= min_y and x_sym <= max_x and y_sym <= max_y:
                    result.append([x_sym, y_sym])
            y += 1
        x += 1
        y = 0

    return result

def create_data_for_coordinates(towers, graph):
    '''
    creates the weightings for the graph based on tower range, damage and rate of fire
    '''
    result = {}
    min_x = 20
    min_y = 0
    max_x = graph.width
    max_y = graph.height
    coordinate_tower_data = {}
    for tower in towers:
        circle_x = tower["coordinates"][0]
        circle_y = tower["coordinates"][1]
        radius = tower["firing_range"]
        x = circle_x - radius
        y = circle_y - radius
        while x <= circle_x:
            while y <= circle_y:
                if (x- circle_x)**2 + (y - circle_y)**2 <= radius**2:
                    tower_weighting = tower["damage_per_shot"] * tower["rate_of_fire"]
                    x_sym = circle_x - (x - circle_x)
                    y_sym = circle_y - (y - circle_y)
                    if x >= min_x and y >= min_y and x <= max_x and y <= max_y:
                        key = tuple([x, y])
                        if key not in result:
                            result[key] = tower_weighting
                            coordinate_tower_data[key] = [tower["id"]]
                        else:
                            result[key] = result[key] + tower_weighting
                            coordinate_tower_data[key].append(tower["id"])
                    if x_sym >= min_x and y_sym >= min_y and x_sym <= max_x and y_sym <= max_y:
                        key = tuple([x_sym, y_sym])
                        if key not in result:
                            result[key] = tower_weighting
                            coordinate_tower_data[key] = [tower["id"]]
                        else:
                            result[key] = result[key] + tower_weighting
                            coordinate_tower_data[key].append(tower["id"])
                y += 1
            x += 1
            y = 0
    return result, coordinate_tower_data


def attach_attack_data_for_buildings(unit, buildings, graph):
    '''
    using the unit as a reference point attach the ideal attack data
    such as the the areas around the building with the least amount of damage
    within the units firing range
    '''
    unit_range = unit['firing_range']
    for building in buildings:
        building_coordinates = building['coordinates']
        firing_positions = find_all_points_inside_circle(building_coordinates, unit_range, graph)
        ideal_firing_positions = []
        lowest_weighting = float('inf')

        for firing_spot in firing_positions:
            key = tuple(firing_spot)
            if key in graph.weights:
                coord_weighting = graph.weights.get(key, 0)
                if coord_weighting < lowest_weighting:
                    lowest_weighting = coord_weighting
                    ideal_firing_positions = [firing_spot]
                elif coord_weighting == lowest_weighting:
                    ideal_firing_positions.append(firing_spot)
            elif lowest_weighting == 0:
                ideal_firing_positions.append(firing_spot)
            else:
                lowest_weighting = float(0)
                ideal_firing_positions = [firing_spot]

        towers_responsible = []
        lowest_weighting = lowest_weighting if lowest_weighting != float('inf') else 0
        if lowest_weighting > 0:
            for position in ideal_firing_positions:
                towers_responsible.append(graph.cause[tuple(position)])
        building["lowest_weighting"] = lowest_weighting
        building["lowest_weighting_coordinates"] = ideal_firing_positions
        building["responsible_towers"] = towers_responsible
    return buildings

def prioritise_targets(unit, buildings, graph):
    '''
    coordinates data from various places and decides what building to attack
    '''
    ## need to filter down data for movement calculation,
    ## it is a heavy operation so get the number of buildings down to one ideally
    targets = buildings
    targets = attach_attack_data_for_buildings(unit, targets, graph)
    min_weight = min(building["lowest_weighting"] for building in targets)
    targets = [building for building in targets if building["lowest_weighting"] == min_weight]
    target = targets[0]

    ##filter coordinates down and check if unit is in correct position
    unit_coord = unit['coordinates']
    nearist_coord = find_nearest_coordinate(unit_coord, target["lowest_weighting_coordinates"])
    if unit_coord != nearist_coord:
        ## Calculate Movement
        start = tuple(unit_coord)
        end = tuple(nearist_coord)
        came_from, cost_so_far = a_star_search(graph, start, end)
        path_to_target = reconstruct_path(came_from, start=start, goal=end)
        #straight line calculator
        move_point = get_last_coordinate_of_direction(path_to_target)
        return unit_client.do_move(move_point)
    else:
        return unit_client.do_attack(target['id'])
    return None

def get_last_coordinate_of_direction(path_to_target):
    '''
    gets the coordinate before the first coordinate that deviates of a straight line path
    '''
    move_point = path_to_target[0]
    coordinate_change = (0, 0)
    for point in path_to_target:
        coordinate_change = (move_point[0] - point[0], move_point[1] - point[1])
        if coordinate_change[0] != 0  or coordinate_change[1] != 0:
            move_point = point
        else:
            break
    return move_point

def find_nearest_coordinate(coord, coordinate_list):
    '''
    finds the nearist coordinate from a list relative to another
    '''
    if len(coordinate_list) < 1:
        raise ValueError('No coordinates passed into find_nearest_coordinate')
    distance = lambda s, d: (s[0]-d[0])**2+(s[1]-d[1])**2
    closest_coord = min(coordinate_list, key=partial(distance, coord))
    return closest_coord

def time_to_kill(unit, tower):
    '''
    returns the time it takes for the tower to kill the unit
    '''
    result = unit["hit_points"] / (tower["damage_per_shot"] * tower["rate_of_fire"])
    return result

def lets_go_hunting():
    '''
    gets the latest data from the game
    creates the graph and attaches weightings with causes
    then calls the method that will determine the targets to go after
    '''
    #aka setup
    unit = unit_client.ask_my_info()
    buildings = unit_client.ask_buildings()
    battlefield = GridWithWeights(40, 40)
    #battlefield.walls = [(19, y) for y in range(40)]
    # + [tower['coordinates'] for tower in towers]
    towers = unit_client.ask_towers()
    data_weights, tower_coord_mapping = create_data_for_coordinates(towers, battlefield)
    battlefield.cause = tower_coord_mapping
    #battlefield.weights = data_weights
    prioritise_targets(unit, buildings, battlefield)
    unit_client.when_idle(lets_go_hunting)

unit_client = commander.Client()
lets_go_hunting()
