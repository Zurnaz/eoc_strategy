'''
Mock for unit testing
'''
import json
'''

'''
import os
JSON_FILE = os.path.dirname(os.path.realpath(__file__))+"\\data.json"

class Client:
    def __init__(self):
        with open(JSON_FILE) as data_file:
            data = json.load(data_file)
        self.item = data["towers"] + data["buildings"] + data["units"] + data["center"]
        self.towers = data["towers"]
        self.buildings = data["buildings"]
        self.center = data["center"]
        self.units = data["units"]
        self.current = data["units"][0]
        self.max_callbacks = 1
        self.current_callbacks = 0
    def ask_my_info(self):
        return self.current

    def ask_item_info(self, item_id):
        result = [item for item in self.item if item_id == self.item["id"]][0]
        return result

    def ask_enemy_items(self):
        enemy_player_id = 1
        result = [item for item in self.item if enemy_player_id == self.item["player_id"]][0]
        return result

    def ask_buildings(self):
        return self.buildings

    def ask_towers(self):
        return self.towers

    def ask_center(self):
        return self.center

    def ask_units(self):
        return self.units

    def ask_nearest_enemy(self):
        result = self.current
        return result

    def ask_my_range_enemy_items(self):
        result = self.current
        return result

    def ask_cur_time(self):
        result = self.current
        return result

    def when_idle(self, method):
        if self.current_callbacks < self.max_callbacks:
            self.current_callbacks = self.current_callbacks + 1
            print(str(self.current["id"])+" is idle.:")
            method()

    def do_move(self, move_point):
        if self.current_callbacks < self.max_callbacks:
            self.current_callbacks = self.current_callbacks + 1
            print(str(self.current["id"])+" moving:" + str(move_point))

    def do_attack(self, target_id):
        if self.current_callbacks < self.max_callbacks:
            self.current_callbacks = self.current_callbacks + 1
            print(str(self.current["id"])+" attacking:" + str(target_id))
