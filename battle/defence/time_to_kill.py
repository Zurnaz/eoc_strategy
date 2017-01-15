'''
Tower defence script.
Logic hierarchy:
Fire at unit with lowest time to kill
Fire at highest dps
Fire at closest
First in list
'''
from battle import commander
from functools import partial
tower_client = commander.Client()

def find_targets():
    '''
    finds all targets within range
    '''
    targets = tower_client.ask_my_range_enemy_items()
    targets = target_priority(targets)
    if len(targets) > 0:
        tower_client.do_attack(targets[0]['id'])
        ##find/create event for per shot
        tower_client.when_idle(find_targets)
    else:
        tower_client.when_enemy_in_range(find_targets)
    return targets

def target_priority(data):
    '''
    gets a list of targets and filters the list down
    '''
    targets = data
    if len(targets) > 1:
        targets = find_enemy_lowest_time_to_kill(targets)
    elif len(targets) > 1:
        targets = find_enemys_with_highest_dps(targets)
    elif len(targets) > 1:
        targets = find_neatest_enemys_from_list(targets)
    return targets

def point_inside_circle(point_coord, circle_coord, circle_radius):
    '''
    Checks if a coordinate is inside a circle
    useful for ideniftying if a tower can hit a unit
    '''
    x, y = point_coord
    circle_x, circle_y = circle_coord
    result = (x - circle_x)**2 + (y - circle_y)**2 <= circle_radius**2
    return result

def time_to_kill(unit,tower):
    result = unit["hit_points"] / (tower["damage_per_shot"] * tower["rate_of_fire"])
    return result

def find_enemy_lowest_time_to_kill(data):
    targets = data
    towers = tower_client.ask_towers()
    UnitsTimeToKill = []
    for unit in targets:
        for tower in towers:
            if point_inside_circle(unit["coordinates"],tower["coordinates"],tower["firing_range"]):
                UnitsTimeToKill.append([time_to_kill(unit,tower), unit["coordinates"]])
    if len(UnitsTimeToKill) > 0:
        lowestScoreCoord = UnitsTimeToKill[UnitsTimeToKill.index(min(UnitsTimeToKill))][1]
        targets = [target for target in targets if target["coordinates"]==lowestScoreCoord]
    return targets

def find_enemys_with_highest_dps(targets):
    '''
    calculate damge per second for each target and select the ones with the highest
    '''
    result = []
    largestThreat = 0
    if targets:
        seqDps = [x['damage_per_shot'] for x in targets]
        seqRof = [x['rate_of_fire'] for x in targets]
        largestThreat = max(seqDps)*max(seqRof)
    for unit in targets:
        threat = unit.get("damage_per_shot", 0) * unit.get("rate_of_fire", 0)
        if threat >= largestThreat:
            result.append(unit)
    return result

def find_neatest_enemys_from_list(targets):
    '''
    finds the nearist targets from a list and returns a list as targets could
    be standing on the same spot together
    '''
    if len(targets)>1:
        coord = tower_client.ask_my_info()["coordinates"]
        a = [x['coordinates'] for x in targets]
        dist=lambda s,d: (s[0]-d[0])**2+(s[1]-d[1])**2
        closestCoord = min(a, key=partial(dist, coord))
        targets = [target for target in targets if target["coordinates"]==closestCoord]
    return targets

find_targets()
'''
if __name__ == '__main__':
    # Unit Tests
    print("Running health check")
    #Warning: ask_my_info() points to ask_units()[0]
    #These cause a lot of loop to occur so it can take a bit to run, comment out sections to speed it up
    mockUnits = tower_client.ask_units()
    #assert  find_targets() == find_targets(), "Failed find target basic"
    assert target_priority([]) == target_priority([]), "Failed priority empty"
    assert target_priority(mockUnits) == target_priority(mockUnits), "Failed priority multiple same"
    assert target_priority([mockUnits[0]]) == target_priority([mockUnits[0]]), "Failed priority single"
    assert  find_enemy_lowest_time_to_kill([]) == find_enemy_lowest_time_to_kill([]), "Failed LTK Empty"
    assert  find_enemy_lowest_time_to_kill(mockUnits) == find_enemy_lowest_time_to_kill(mockUnits), "Failed LTK Many Same"
    inputTTK = mockUnits
    inputTTK[0]["hit_points"]  = 10
    inputTTK[0]["coordinates"]  = [25, 16]
    assert  find_enemy_lowest_time_to_kill(inputTTK) == find_enemy_lowest_time_to_kill([inputTTK[0]]), "Failed LTK on lowest"
    assert  find_enemys_with_highest_dps([]) == find_enemys_with_highest_dps([]), "Failed DPS Empty"
    inputHighestDps = mockUnits
    inputHighestDps[0]["rate_of_fire"] = 10
    assert  find_enemys_with_highest_dps(inputHighestDps) == find_enemys_with_highest_dps([inputHighestDps[0]]), "Failed DPS one strong target"
    assert  find_enemys_with_highest_dps(mockUnits) == find_enemys_with_highest_dps(mockUnits), "Failed DPS multiple strong targets"
    assert  find_neatest_enemys_from_list([]) == find_neatest_enemys_from_list([]), "Failed nearest ememy empty"
    assert  find_neatest_enemys_from_list(mockUnits) == find_neatest_enemys_from_list(mockUnits), "Failed nearest multiple enemys"
    inputNearest = mockUnits
    inputNearest[1]["coordinates"]=[10,40]
    assert  find_neatest_enemys_from_list(inputNearest) == find_neatest_enemys_from_list([inputNearest[0]]), "Failed nearest single enemy"
    print("Heath check passed")
    '''
   #'''
