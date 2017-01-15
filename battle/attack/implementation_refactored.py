'''
Refactored*
START OF EXTERNAL CODE
NOTICE
# Sample code from http://www.redblobgames.com/pathfinding/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

Refactored: changes to variable names, other changes specified in code
'''

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, identifier):
        (x, y) = identifier
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, identifier):
        return identifier not in self.walls

    def neighbors(self, identifier):
        '''
        returns the possible nodes you can go to from the current node
        results determine the number of links a node has, currently 4,
        this means only horizontal and verticle movement, but increase it to
        8 and it will allow diagonal movement but increases cpu usage
        Changed filter into a list comprehension
        '''
        (x, y) = identifier
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            # aesthetics
            results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        #results = [identifier for identifier in results if  identifier == self.in_bounds]
        #results = [identifier for identifier in results if  identifier == self.passable]
        return results


class GridWithWeights(SquareGrid):
    '''
    generates weighting for a square grid
    modified to have the cause of the weighting also included
    '''
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}
        self.cause = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                frontier.put(next_node, priority)
                came_from[next_node] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far
'''
END OF EXTERNAL CODE
'''
