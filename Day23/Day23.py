'''
    What: Advent of Code 2023 - Day 23
    Who: Josh Geiser
'''

from pathlib import Path
from copy import deepcopy
import sys
sys.setrecursionlimit(10000)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_neighs(grid, visited, curr):
    '''
    Helper function for part 1 - get the neighbors of given "curr" position/node
    '''

    # Directions to visit our potential neighbors, as well as valid markings
    dirs = {
        (0, +1) : {'.', '>'},
        (-1, 0) : {'.'},
        (0, -1) : {'.'},
        (+1, 0) : {'.' , 'v'}
    }

    # For each of these potential neighbors, get the coordinates...
    neighs_out = []
    for dir, valid_markings in dirs.items():
        neigh = (curr[0] + dir[0], curr[1] + dir[1])

        # If we haven't visited this neighbor and it's valid, add to output list
        if neigh not in visited and grid[neigh[0]][neigh[1]] in valid_markings:
            neighs_out.append(neigh)

    # Sanity check: should only have 1 to 2 valid neighbors at each location
    assert 1 <= len(neighs_out) <= 2
    return neighs_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_paths(grid, visited, curr, out_paths):
    '''
    Helper function for part 1 - use recursive logic to get all potential paths
    to target node
    '''

    # Base Case - we're at our endpoint
    if curr == (len(grid)-1, len(grid[0])-2):
        out_paths.append(len(visited))
        return

    # Recursive Case - get all of our neighbors and make more recursive calls
    neighs = __get_neighs(grid, visited, curr)
    visited.add(curr)

    # If we're at a node where we can go 2 separate directions - make a copy of our
    # visited nodes and make one recursive call taking that direction
    if len(neighs) == 2:
        new_visited = deepcopy(visited)
        __get_paths(grid, new_visited, neighs[0], out_paths)

    # Take our only (remaining) direction
    __get_paths(grid, visited, neighs[-1], out_paths)

    return out_paths

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - use recursive logic to get a list of all of the lengths
    of possible paths "outpaths".
    '''
    visited = {(0,1)}
    outpaths = __get_paths(inputs, visited, (1,1), [])
    return max(outpaths)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_neighs_v2(grid, visited, curr, last):
    '''
    Helper function for part 2 - get the neighbors of given "curr" position/node
    '''

    # Directions to visit our potential neighbors, as well as valid markings
    dirs = {
        (0, +1) : {'.', 'v', '>'},
        (-1, 0) : {'.', 'v', '>'},
        (0, -1) : {'.', 'v', '>'},
        (+1, 0) : {'.', 'v', '>'}
    }

    # For each of these potential neighbors, get the coordinates...
    neighs_out = []
    for dir, valid_markings in dirs.items():
        neigh = (curr[0] + dir[0], curr[1] + dir[1])

        # If we haven't visited this neighbor and it's valid, add to output list
        if neigh not in visited and neigh != last and grid[neigh[0]][neigh[1]] in valid_markings:
            neighs_out.append(neigh)

    # Sanity check: should have 0 to 3 valid neighbors at each location
    assert 0 <= len(neighs_out) <= 3, f'{len(neighs_out)}'
    return neighs_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_paths_v2(grid, visited, curr, last, steps_so_far, out_paths):
    '''
    Helper function for part 2 - use recursive logic to get all potential paths
    to target node. Note that deepcopy's take a long time, so now rather than 
    storing all of the visited nodes in "visited", we're only storing nodes that
    are at "splits" in the maze, that way we have much smaller sets to deepcopy 
    (we also now make use of another variable "last" which was our most recent
    visited node). 
    '''

    # Base Case - if we're at the end node, let's print how many steps this path took
    if curr == (len(grid)-1, len(grid[0])-2):
        out_paths.add(steps_so_far)
        print(max(out_paths))
        del visited
        return

    # Recursive Case - get all of our neighbors and make more recursive calls
    neighs = __get_neighs_v2(grid, visited, curr, last)
    steps_so_far += 1

    # If we're at a "split", add the current node to our set of visited nodes
    if len(neighs) > 1:
        visited.add(curr)

    # Make deepcopys of our "visited" nodes and make recursive calls with each subdirection
    for i in range(len(neighs)-1):
        new_visited = deepcopy(visited)
        __get_paths_v2(grid, new_visited, neighs[i], curr, steps_so_far, out_paths)

    # We can avoid at least one deepcopy by just using the existing "visited" nodes
    if len(neighs) > 0:
        __get_paths_v2(grid, visited, neighs[-1], curr, steps_so_far, out_paths)

    return out_paths

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - note that as written, this takes method takes hours to 
    run :( but by printing out the outputs as we go we're able to see the longest
    path anyways. Maybe I'll get around to rewriting this at some point to be 
    better...
    '''
    visited = set()
    steps_so_far = 1
    curr = (1,1)
    last = (0,1)
    outpaths = __get_paths_v2(inputs, visited, curr, last, steps_so_far, set())
    return max(outpaths)
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    infile = Path(__file__).parent / 'input.txt'

    inputs = read_input(infile)
    print(task_1(inputs))

    # inputs = read_input(infile)
    # print(task_2(inputs))

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()
