from battle import commander
unit_client = commander.Client()

##useful methods
## finds edge tower and highest damage tower of the edge ones
def find_edge_tower(data=None, *args, **kawargs):
    towers = unit_client.ask_towers()
    #towers = unit_client.ask_buildings()
    maxDamage = 0
    target = None

    if towers:
        seq = [x['coordinates'][0] for x in towers]
        largestCordinate = [max(seq),0]

        for item in towers:
            if item["coordinates"][0] == largestCordinate[0]:
                if maxDamage <= item["damage_per_shot"]*item["rate_of_fire"]:
                    maxDamage = item["damage_per_shot"]*item["rate_of_fire"]
                    target = item
                    #largestCordinate[0] = item["coordinates"][0]

    return target

def search_and_destroy(data=None, *args, **kawargs):
    enemy = unit_client.ask_nearest_enemy()
    unit_client.do_attack(enemy['id'])
    unit_client.when_item_destroyed(enemy['id'], search_and_destroy)

def find_friendly_units_by_action(*args, **kawargs):
    units = unit_client.ask_units()
    result = []
    for unit in units:
        if unit["action"] in args:
            result.append(unit)
    return result

def move_to_unit(unit, *args, **kawargs):
    if unit_client.ask_my_info()[coordinates]!=unit["coordinates"]:
        unit_client.do_move(unit["coordinates"])

##Battle plan

##landing party
##destroy targets in range and assist any troops under attack
def destroy_enemy_in_range(*args, **kawargs):
    data = unit_client.ask_my_range_enemy_items()
    if len(data)>0:
        target = 0
        unit_client.do_attack(data[target]["id"])
        unit_client.when_item_destroyed(data[target]["id"], destroy_enemy_in_range)
    else:
        friendly = find_friendly_units_by_action("attack")
        if len(friendly)>0:
            target = 0
            unit_client.do_move(friendly[target][coordinates])
            when_in_area(friendly[target][coordinates], 3, destroy_enemy_in_range)
        else:
            destroy_edge_towers()

## regroup

## avoid turrets if centre is not covered by them
## this may need to map out ranges of turrets and damages for each square on grid

## find edge towers and destroy them together
def destroy_edge_towers(*args, **kawargs):
    tower = find_edge_tower()
    if (tower):
        unit_client.do_attack(tower["id"])
        unit_client.when_item_destroyed(tower["id"], destroy_edge_towers)
    else:
        attack_center()

## destroy center
def attack_center(*args, **kawargs):
    center = unit_client.ask_center()
    unit_client.do_attack(center['id'])
##
destroy_enemy_in_range()


'''if __name__ == '__main__':
    # Unit Tests
    assert  find_friendly_units_by_action("move")[0]["role"]=="unit", "Does not return any units"
    assert  find_friendly_units_by_action("random") == [], "Does not return empty array"
    assert  find_edge_tower()["role"] == "tower", "Does not return any towers"
    assert  find_edge_tower() == find_edge_tower(), "Failed Basic"
    assert  destroy_edge_towers() ==  destroy_edge_towers(), "Failed Basic"
    print("Heath Check passed")
    '''
   #'''
