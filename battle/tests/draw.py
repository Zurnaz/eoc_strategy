'''
Drawing methods to give a visual representation of paths
http://www.redblobgames.com/pathfinding/a-star/implementation.html
Refactored*
'''
def draw_tile(graph, identifier, style, width):
    '''
    This picks the icon to display when generating paths
    Has 3 styles: path, point_to, number
    Originally it used unicode arrows but they were not working so they were
    swapped to similar keyboard keys and orignals were commented out
    '''
    result = "."
    if 'number' in style and identifier in style['number']:
        result = "%d" % style['number'][identifier]
    if 'point_to' in style and style['point_to'].get(identifier, None) is not None:
        (x_1, y_1) = identifier
        (x_2, y_2) = style['point_to'][identifier]
        if x_2 == x_1 + 1:
            #'\u2192'
            result = '>'
        if x_2 == x_1 - 1:
            #'\u2190'
            result = '<'
        if y_2 == y_1 + 1:
            #'\u2193'
            result = 'v'
        if y_2 == y_1 - 1:
            #\u2191'
            result = "^"
    if 'start' in style and identifier == style['start']:
        result = "A"
    if 'goal' in style and identifier == style['goal']:
        result = "Z"
    if 'path' in style and identifier in style['path']:
        result = "@"
    if identifier in graph.walls:
        result = "#" * width
    return result

def draw_grid(graph, width=2, **style):
    '''
    draws the grid in 3 styles: path, point_to, number
    '''
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print("")
