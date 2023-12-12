'''
    What: Advent of Code 2023 - Day 10
    Who: Josh Geiser
'''

from pathlib import Path
from queue import Queue

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __find_S(inputs):

    # Grid dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Just iterate until we find S
    for i in range(m):
        for j in range(n):
            if (inputs[i][j] == 'S'):
                return (i,j)

    # Hopefully we never get here...
    return None

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __add_neigh(neigh, direction, inputs, visited):

    # Grid dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Mapping of what direction we came from to valid pipes for that direction
    mapping = {
        'west': {'-', 'J', '7'},
        'south': {'|', '7', 'F'},
        'east': {'-', 'F', 'L'},
        'north': {'|', 'L', 'J'}
    }

    # If this neighbor is within dimensions, we haven't visited yet, and the pipe is the right direction, then Trues
    if ((0 <= neigh[0] < m) and 
        (0 <= neigh[1] < n) and
        (neigh not in visited) and 
        inputs[neigh[0]][neigh[1]] in mapping[direction]):
        return True
    else:
        return False

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs, for_part_2:bool=False):
    '''
    Main method for part 1, uses BFS to find main loop
    '''

    # First find where S is
    curr = __find_S(inputs)

    # Directions to visit our potential neighbors
    dirs = [(0, +1, 'west'), (-1, 0, 'south'), (0, -1, 'east'), (+1, 0, 'north')]

    # Other variables we'll use in BFS
    visited = set()
    q = Queue()

    # Add "S" to the queue
    q.put(curr)
    visited.add(curr)

    # BFS: Iterate until queue is empty
    steps = 0
    while (not q.empty()):

        # Iterate through the current distance away
        size = q.qsize()
        for i in range(size):

            # Get neighbors of curr
            curr = q.get()
            for dir in dirs:
                neigh = (curr[0] + dir[0], curr[1] + dir[1])

                # If we haven't visited this neighbor yet and it's a valid pipe, add it to queue
                if __add_neigh(neigh, dir[2], inputs, visited):
                    q.put(neigh)
                    visited.add(neigh)

        # Increment our step
        steps += 1

    # For part 2, return all the coordinates of the main loop
    # For part 1, return steps-1 since we went an extra iteration at the end
    if for_part_2:
        return visited
    else:
        return steps-1

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_next_dir(inputs, curr, prev_dir):
    '''
    Helper function for part 2 to determine the next node and next direction we 
    should go given the type of 'pipe' at our current node. I highly dislike how 
    I wrote this function but oh well it works
    '''

    # north->north or south->south
    if inputs[curr[0]][curr[1]] == '|':
        if prev_dir == 'north':
            return (curr[0]-1, curr[1]), prev_dir
        else: # south
            return (curr[0]+1, curr[1]), prev_dir
        
    # east->east or west->west
    elif inputs[curr[0]][curr[1]] == '-':
        if prev_dir == 'east':
            return (curr[0], curr[1]+1), prev_dir
        else: # west
            return (curr[0], curr[1]-1), prev_dir
        
    # south->east or west->north
    elif inputs[curr[0]][curr[1]] == 'L':
        if prev_dir == 'south':
            return (curr[0], curr[1]+1), 'east'
        else: # west
            return (curr[0]-1, curr[1]), 'north'
        
    # south->west or east->north
    elif inputs[curr[0]][curr[1]] == 'J':
        if prev_dir == 'south':
            return (curr[0], curr[1]-1), 'west'
        else: # east
            return (curr[0]-1, curr[1]), 'north'
        
    # north->west or east->south
    elif inputs[curr[0]][curr[1]] == '7':
        if prev_dir == 'north':
            return (curr[0], curr[1]-1), 'west'
        else: # east
            return (curr[0]+1, curr[1]), 'south'
        
    # north->east or west->south
    elif inputs[curr[0]][curr[1]] == 'F':
        if prev_dir == 'north':
            return (curr[0], curr[1]+1), 'east'
        else: # west
            return (curr[0]+1, curr[1]), 'south'
        
    return None

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __in_map(curr, m, n):
    return (0 <= curr[0] < m) and (0 <= curr[1] < n)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __is_inside_loop(curr, main_loop_map):
    '''
    Helper function for part 2 to determine if the current node in question is
    inside the main loop or not
    '''

    # Keep traveling west until we've either hit the western edge of the map or we've hit the main loop
    curr_neigh = (curr[0], curr[1]-1)
    while curr_neigh not in main_loop_map.keys() and curr_neigh[1] > 0:
        curr_neigh = (curr_neigh[0], curr_neigh[1]-1)

    # If we've hit the western edge of the map, then we definitely aren't in the main loop
    if curr_neigh[1] == 0:
        return False
    
    # Otherwise, depending on the direction of our main loop, we may be inside or outside the
    # main loop depending on the direction of the current node to the west of us
    elif 'south' in main_loop_map[curr_neigh]: # (north or south depending on CW or CCW)
        return True
    else:
        return False

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_main_loop_map(inputs, init_dir:bool=True):
    '''
    Helper function for part 2 to get a map mapping main loop nodes to their 
    corresponding "directions" given a CW or CCW loop (overall direction of main
    loop is set by "init_dir" kwarg)
    '''

    # Grid dimensions
    m = len(inputs)
    n = len(inputs[0])

    # First find where S is
    S = __find_S(inputs)

    # Helper variable for finding 2 starting neighbors of S
    dirs = [(0, +1, 'east',  {'-','J','7'}), 
            (-1, 0, 'north', {'|','7','F'}),
            (0, -1, 'west',  {'-','F','L'}),
            (+1, 0, 'south', {'|','L', 'J'})]

    # Another helper variable for finding 2 starting neighbors of S
    opposites = {
        'east':'west',
        'west':'east',
        'north':'south',
        'south':'north'
    }

    # Now actually get the 2 starting neighbors of S in "neighs" variable
    neighs = []
    for dir in dirs:
        neigh = (S[0] + dir[0], S[1] + dir[1])
        if __in_map(neigh, m, n) and inputs[neigh[0]][neigh[1]] in dir[3]:
            neighs.append((neigh[0], neigh[1], dir[2]))

    # There should only be two neighbors to S in the main loop...
    assert len(neighs) == 2

    # Here we inadvertantly either pick going clockwise (CW) or counter-clockwise (CCW) around the loop
    # This depends on if we choose neighs[0] or neighs[1] as our starting "direction"
    if init_dir:
        start = neighs[0]
        end = neighs[1]
    else:
        start = neighs[1]
        end = neighs[0]

    # Map of main loop coordinates to their directions
    main_loop_map = {}

    # Add first value to map
    main_loop_map[S] = {start[2], opposites[end[2]]}
    curr = start[0:2]
    prev_dir = start[2]

    # Now iterate, adding more k/v pairs to the map until we've gone through the whole main loop and are back at S
    while curr != S:
        next_val, next_dir = __get_next_dir(inputs, curr, prev_dir)
        main_loop_map[curr] = {prev_dir, next_dir}
        curr = next_val
        prev_dir = next_dir

    return main_loop_map

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Main method for part 2. Associates each pipe in the main loop with a "direction"
    that can be used to determine if a given node is inside or outside the main loop
    depending on the location of that node wrt the main loop and the direction of the 
    main loop at that point
    '''

    # Grid dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Get a map of:
    #   keys = coordinates of all the pipes/positions in the main loop
    #   values = "directions" that pipe is going (given an assumption on CW or CCW loop)
    main_loop_map = __get_main_loop_map(inputs, init_dir=True)

    # Helper variables
    inside_loop_set = set()
    outside_loop_set = set()

    # Iterate through all nodes, with the exception of the border since these will always be outside the main loop
    sum_out = 0
    for i in range(1, m-1):
        for j in range(1, n-1):
            curr = (i,j)

            # If we're at a node that's part of the main loop, just continue...
            if curr in main_loop_map:
                continue

            # Else if the current node is inside our main loop, then yay! Increment output sum
            elif __is_inside_loop(curr, main_loop_map):
                sum_out +=1
                inside_loop_set.add(curr)

            # Otherwise, node in question is outside of the main loop
            else:
                outside_loop_set.add(curr)

    return sum_out
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    here = Path(__file__).parent
    infile = here / 'input.txt'

    inputs = read_input(infile)
    answer_1 = task_1(inputs)
    print(answer_1)

    inputs = read_input(infile)
    answer_2 = task_2(inputs)
    print(answer_2)

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()
