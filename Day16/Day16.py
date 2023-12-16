'''
    What: Advent of Code 2023 - Day 16
    Who: Josh Geiser
'''

from pathlib import Path
from collections import deque

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_outdir(grid, curr):
    '''
    Given an input 4-tuple (row, col, input-direction, None), return a list of 
    potential 4-tuples with output direction included. Returned list should always
    be of length 1 or 2.

        Ex1: (1, 4, '>', None) --------> [(1, 4, '>', 'v')] 
        Ex2: (0, 1, '>', None) --------> [(0, 1, '>', '^'), (0, 1, '>', 'v')]
    '''

    # Unpack
    row, col, indir, outdir = curr
    assert outdir is None

    # Determine if we're dealing with a '.', '-', '|', '/', or '\'
    grid_pt = grid[row][col]

    # If our out-direction (curr[3]) is the same as our in-direction
    if (grid_pt == '.') or (grid_pt == '|' and indir in {'^','v'}) or (grid_pt == '-' and indir in {'<','>'}):
        return [(row, col, indir, indir)]

    # If we have a diagonal mirror
    mapping = {
        ('\\', '>') : 'v',
        ('\\', '^') : '<', 
        ('\\', 'v') : '>',
        ('\\', '<') : '^', 
        ('/',  '>') : '^',
        ('/',  '^') : '>', 
        ('/',  'v') : '<',
        ('/',  '<') : 'v', 
    }
    if (grid_pt, indir) in mapping:
        return [(row, col, indir, mapping[(grid_pt, indir)])]
    
    # If we need to split into two
    if (grid_pt == '|' and indir in {'>','<'}):
        return [(row, col, indir, '^'), (row, col, indir, 'v')]
    
    # Also if we need to split into two
    if (grid_pt == '-' and indir in {'^','v'}):
        return [(row, col, indir, '<'), (row, col, indir, '>')]

    raise SystemError

<<<<<<< HEAD
=======

>>>>>>> b28511fda27d0b4139d67a695989e01d75600a85
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_next(curr, m, n):
    '''
    Given a 4-tuple (row, col, input-direction, output-direction), return another 
    4-tuple (row, col, input-direction, None) for the next neighbor visited IF 
    that neighbor is within grid dimensions. Otherwise, return None

        Ex1: (0, 1, '>', '^') --------> None
        Ex2: (0, 1, '>', 'v') --------> (1, 1, 'v', None)
    '''

    # Unpack 4-tuple
    row, col, indir, outdir = curr
    assert outdir is not None

    # Figure out what our next grid cell is
    outdir_map = {
        '>' : (0, +1),
        '<' : (0, -1),
        '^' : (-1, 0),
        'v' : (+1, 0)
    }
    incr = outdir_map[outdir]
    row, col = row+incr[0], col+incr[1]

    # If our next grid cell is within the map, return our next 4-tuple to look at
    if 0 <= row < m and 0 <= col < n:
        return (row, col, outdir, None)
    
    # Otherwise if it's outside of dimension of the map, return None
    else:
        return None
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __simulate_energized(grid, start):

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Set of visited 4-tuples (excluding output-direction) so we don't loop indefinitely
    visited = set()

    # Add our starting point to the stack
    st = deque()
    st.append(start)

    # DFS: Iterate through our stack
    while (len(st) > 0):

        # Pop our next value from the stack
        curr = st.pop()
        assert type(curr) == tuple and curr[3] is None

        # If we've visited this permutation before, skip. Otherwise, add to visited
        if curr in visited:
            continue
        else:
            visited.add(curr)

        # Get a list of the potential output directions we can go
        potential_nexts = __get_outdir(grid, curr)
        assert (type(potential_nexts) == list and len(potential_nexts) <= 2)

        # For each of the potential output directions, if we haven't visited yet
        # and it's within the grid dimensions, add to our stack
        for potential_next in potential_nexts:
            next = __get_next(potential_next, m, n)
            if next is not None and next not in visited:
                st.append(next)

    # Finally, determine the amount of grid points we've visited ("energized")
    numEnergized = len(set([(curr[0],curr[1]) for curr in visited]))
    return numEnergized

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(grid):
    '''
    Task 1 main method
    '''
    start = (0, 0, '>', None)
    return __simulate_energized(grid, start)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(grid):
    '''
    Task 2 main method
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # All the different amounts of number energized we can have from different starting places
    numEnergizedArr = []

    # Top row and bottom row
    for j in range(n):
        numEnergizedArr.append(__simulate_energized(grid, (0, j, 'v', None)))
        numEnergizedArr.append(__simulate_energized(grid, (m-1, j, '^', None)))

    # Left column and bottom column
    for i in range(m):
        numEnergizedArr.append(__simulate_energized(grid, (i, 0, '>', None)))
        numEnergizedArr.append(__simulate_energized(grid, (i, n-1, '<', None)))

    # Finally return the max number of energized
    return max(numEnergizedArr)
    
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
