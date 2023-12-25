'''
    What: Advent of Code 2023 - Day 22
    Who: Josh Geiser
'''

from pathlib import Path
from queue import Queue, PriorityQueue

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_locs(endpoints, only_bottom_z=False):
    '''
    Helper function for parts 1 and 2 - get list of all 3-tuple coordinates of a 
    block given its endpoints (a list of two tuples). Also a flag to only return
    the bottom coordinate for vertical blocks. 
    '''

    # Get differences between start and endpoint in each dimension
    start, end = endpoints
    diffs = [end[0]-start[0], end[1]-start[1], end[2]-start[2]]

    # If a vertical block and we only want to test the bottom node of it
    if only_bottom_z and diffs[2] > 0:
        return [(start[0], start[1], __min_z(endpoints))]

    # Ugh, this sucks... get all points contained by block as a list of 3-tuple coodinates
    out = []
    for i in range(min(start[0],end[0]), max(start[0],end[0])+1):
        for j in range(min(start[1],end[1]), max(start[1],end[1])+1):
            for k in range(min(start[2],end[2]), max(start[2],end[2])+1):
                out.append((i,j,k))
    
    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __min_z(endpoints):
    '''
    Helper function for parts 1 and 2 - return minimum z coordinate of a block
    '''
    return min(endpoints[0][2], endpoints[1][2])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __move_down(endpoints, num):
    '''
    Helper function for parts 1 and 2 - move endpoints a distance "num" DOWN in Z
    '''
    return (
        [endpoints[0][0], endpoints[0][1], endpoints[0][2]-num], 
        [endpoints[1][0], endpoints[1][1], endpoints[1][2]-num]
    )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_inputs(inputs):
    '''
    Helper function for parts 1 and 2 - parse our input file and return two helpful
    hashmaps we'll use throughout. "objs" contains a mapping of brick id's to brick 
    endpoints, and "locs_all" contains a mapping of any "filled" point to its 
    corresponding brick.
    '''

    # Hashmaps we will populate and output
    objs = {}
    locs_all = {}

    # Iterate through each line in input file
    # Brick id is equal to the (1-indexed) row number in the input file
    for id,input in enumerate(inputs):

        # Start and endpoints of object as a tuple of lists (I'm not the most
        # consistent in this script with my usage of tuples vs lists whoops)
        start,end = input.split('~')
        start = [int(x) for x in start.split(',')]
        end = [int(x) for x in end.split(',')]

        # "objs" contains a mapping of brick id's to brick endpoints
        objs[id+1] = (start, end)

        # "locs_all" contains a mapping of any "filled" point to its corresponding brick
        locs = __get_locs((start, end))
        for loc in locs:
            locs_all[loc] = id+1

    return objs, locs_all 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __move_helper(objs, locs_all, id, from_endpoints, new_endpoints):
    '''
    Helper function for parts 1 and 2 - move a brick from "from_endpoints" to 
    "new_endpoints" and update our hashmaps accordingly.
    '''

    # First we need to "empty" out all of points previously contained by our brick
    for endpoint in __get_locs(from_endpoints):
        del locs_all[endpoint]

    # Now we need to add in the new set of points contained by our moved brick
    for endpoint in __get_locs(new_endpoints):
        locs_all[endpoint] = id

    # Update endpoints accordingly
    objs[id] = new_endpoints

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __settle(objs, locs_all):
    '''
    Helper function for parts 1 and 2 - "settle" all of our bricks by using a 
    priority queue to settle them based on current z coordinates. 
    '''

    # Add all bricks to priority queue
    pq = PriorityQueue()
    for id,endpoints in objs.items():
        z_val = __min_z(endpoints)
        pq.put((z_val, id))

    # Remove all bricks from priority queue
    while (not pq.empty()):

        # Current brick id
        _, id = pq.get()

        # If we're already on the floor, do nothing
        endpoints = objs[id]
        if __min_z(endpoints) == 1:
            continue

        # Otherwise keep moving down until we're on the floor or on top of another brick
        to_move = 0
        new_endpoints = __move_down(endpoints, 1)
        while (all([loc not in locs_all for loc in __get_locs(new_endpoints, only_bottom_z=True)]) 
               and __min_z(new_endpoints) >= 1):
            to_move += 1
            new_endpoints[0][2] -= 1
            new_endpoints[1][2] -= 1

        # (We should be just above another brick or just above floor) 
        new_endpoints[0][2] += 1
        new_endpoints[1][2] += 1

        # If we need to move this brick any amount, call our move helper function
        if to_move > 0:
            __move_helper(objs, locs_all, id, endpoints, new_endpoints)
        
    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_deps(objs, locs_all):
    '''
    Helper function for parts 1 and 2 - get dependency maps for bricks directly 
    above a current brick "deps_above", as well as bricks directly below a current
    brick "deps_below". Each is returned as a hashmap of (brick id) -> (set of ids)
    '''

    # Initialize output variables
    deps_above = {k:set() for k in objs.keys()}
    deps_below = {k:set() for k in objs.keys()}

    # Iterate through each brick id
    for id,endpoints in objs.items():

        # Get all of the dependencies below
        endpoints_below = __move_down(endpoints, 1)
        for endpoint_below in __get_locs(endpoints_below):
            if endpoint_below in locs_all and locs_all[endpoint_below] != id:
                deps_below[id].add(locs_all[endpoint_below])

        # Get all of the dependencies above
        endpoints_above = __move_down(endpoints, -1)
        for endpoint_above in __get_locs(endpoints_above):
            if endpoint_above in locs_all and locs_all[endpoint_above] != id:
                deps_above[id].add(locs_all[endpoint_above])

    return deps_below, deps_above

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - main idea is to settle all of our bricks, and then check
    each brick individually to see if it is solely responsible for holding up any
    bricks above it
    '''

    # Get all of our inputs, settle our bricks, and get dependency tree(s)
    objs, locs_all = __parse_inputs(inputs)
    __settle(objs, locs_all)
    deps_below, deps_above = __get_deps(objs, locs_all)

    # Iterate through each brick in our stack
    sum_out = 0
    for id in objs.keys():
        curr_deps_above = deps_above[id]

        # If we're on top of the stack, we can disintegrate
        if len(curr_deps_above) == 0:
            sum_out += 1
        
        # If all the bricks above us are resting on at least 2 bricks below, we can disintegrate
        elif all([len(deps_below[curr_dep_above]) > 1 for curr_dep_above in curr_deps_above]):
            sum_out += 1

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __topple(deps_above, deps_below, brick):
    '''
    Helper function for part 2 - takes awhile to run :( (a few minutes), but uses
    a queue and a set of "toppled" bricks to determine the number that would topple
    for a given pulled brick.
    '''

    # Add brick to set of "toppled" bricks
    toppled_set = {brick}

    # Add all of the bricks directly above it to queue
    q = Queue()
    for dep_above in deps_above[brick]:
        q.put(dep_above)

    # While our queue isn't empty...
    while not q.empty():

        # If all the bricks below this brick have been toppled, it will be toppled too
        brick = q.get()
        if all([dep in toppled_set for dep in deps_below[brick]]):
            toppled_set.add(brick)

            # Add all of the bricks above our newly toppled brick to the queue
            for dep_above in deps_above[brick]:
                q.put(dep_above)

    return len(toppled_set) - 1

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - not my best work and takes awhile to run, but oh well...
    '''

    # Get all of our inputs, settle our bricks, and get dependency tree(s)
    objs, locs_all = __parse_inputs(inputs)
    __settle(objs, locs_all)
    deps_below, deps_above = __get_deps(objs, locs_all)

    # Iterate through each brick in our stack, getting our set of non-disintegratable bricks
    bricks_to_check = set()
    for id in objs.keys():
        curr_aboves = deps_above[id]

        # If at a non-disintegratable brick, add to set of bricks to check
        if len(curr_aboves) > 0 and any([len(deps_below[curr_above]) <= 1 for curr_above in curr_aboves]):
            bricks_to_check.add(id)
        
    # Now, iterate through each brick and see how many others it causes to topple
    num_out = 0
    for brick in bricks_to_check:
        num_out += __topple(deps_above, deps_below, brick)
        print(brick)

    return num_out
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    infile = Path(__file__).parent / 'input.txt'

    inputs = read_input(infile)
    print(task_1(inputs))

    inputs = read_input(infile)
    print(task_2(inputs))

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()
