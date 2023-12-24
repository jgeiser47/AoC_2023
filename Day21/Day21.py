'''
    What: Advent of Code 2023 - Day 21
    Who: Josh Geiser
'''

from pathlib import Path
from queue import Queue
import numpy as np

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __find_S(grid):
    '''
    Helper function for parts 1 and 2 to identify the location of the starting "S"
    '''
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                return (i, j) 
    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_neighs(grid, curr):
    '''
    Helper function for part 1 - get the neighbors of our current node assuming 
    that we can't extend pass the dimensions of a single grid.
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Directions to visit our potential neighbors
    dirs = [(0, +1), (-1, 0), (0, -1), (+1, 0)]

    # Iterate through each potential neighbor direction...
    neighs = []
    for dir in dirs:
        neigh_row, neigh_col = curr[0] + dir[0], curr[1] + dir[1]

        # If this neighbor is within grid dimensions and not blocked, add it to valid list
        if (0 <= neigh_row < m) and (0 <= neigh_col < n) and grid[neigh_row][neigh_col] != '#':
            neighs.append((neigh_row, neigh_col))

    return neighs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __BFS(grid, start, part1=True, numSteps=64):
    '''
    Helper function for parts 1 and 2 - perform breadth-first-search (BFS) on our
    grid for an input number of steps
    '''

    # Boolean indicating if we're taking an even or odd # of steps (init "sum_out" accordingly)
    even = (numSteps % 2 == 0)
    sum_out = 1 if even else 0

    # Other variables we'll use
    visited = set()
    q = Queue()

    # Add start point to the queue
    q.put(start)
    visited.add(start)

    # BFS: Iterate until queue is empty
    steps = 0
    while (steps < numSteps):

        # Increment our step
        steps += 1

        # Iterate through the current distance away
        size = q.qsize()
        for i in range(size):

            # Pop out our current node
            curr = q.get()

            # Get neighbors of curr node
            neighs = __get_neighs(grid, curr) if part1 else __get_neighs_v2(grid, curr)
            for neigh in neighs:

                # If we haven't visited this node yet, add to queue and add to visited set
                if neigh not in visited:
                    q.put(neigh)
                    visited.add(neigh)

                    # Update our output value (depending if we have an even or odd # of steps)
                    if even and steps % 2 == 0:
                        sum_out += 1
                    elif not even and steps % 2 == 1:
                        sum_out += 1
                
    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - use BFS to simulate how many garden plots we can reach
    in our allocated 64 steps
    '''
    start = __find_S(inputs)
    out = __BFS(inputs, start)
    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_neighs_v2(grid, curr):
    '''
    Helper function for part 2 - get the neighbors of our current node assuming 
    that we now CAN extend pass the dimensions of a single grid.
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Directions to visit our potential neighbors
    dirs = [(0, +1), (-1, 0), (0, -1), (+1, 0)]

    # Iterate through each potential neighbor direction...
    neighs = []
    for dir in dirs:
        neigh_row, neigh_col = curr[0] + dir[0], curr[1] + dir[1]

        # Do some fancy math to find the corresponding location of the original grid
        corresponding_row = (neigh_row + (1000*m)) % m
        corresponding_col = (neigh_col + (1000*n)) % n

        # If the corresponding grid point is not blocked, add the neighbor point to valid list
        if grid[corresponding_row][corresponding_col] != '#':
            neighs.append((neigh_row, neigh_col))

    return neighs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - I definitely got some inspiration on approach from other
    sources online. The main idea is that we have WAY too many steps to feasibly
    still BFS this, so we have to come up with a less brute force approach. Luckily,
    our input file has some important geometrical considerations: the grid is square,
    S is in the center, there's a clear path of '.'s between S and the middle of each
    edge, and a clear diamond-shaped path of '.'s exists between the middle of each
    edge. 

    The number of steps we take just so happens to get us perfectly to the edge of a
    grid many many steps away. Rather than simulate all of this, we can just simulate
    steps for multiples of the first few number of grids (X) and save off the output 
    number of garden plots reached (Y). Number of garden plots increases quadratically
    with the number of grids we pass, so we'll fit a quadratic polynomial to our small
    dataset, and then use that to calculate number of garden plots for our actual number
    of steps taken. 
    '''
    
    # Input for part 2 - that's a lot of steps!
    numSteps = 26501365

    # Get index of S (center of square grid with an open path  of '.'s to each edge)
    start = __find_S(inputs)

    # Grid dimensions - square grid with length 131
    M = len(inputs)
    N = len(inputs[0])

    # Independent variable "X" will be number of full grid lengths we traverse 
    # Dependent variable "Y" will be number of reachable garden plots
    Xs = []
    Ys = []
    
    # Just iterate through a few small values of "X" (i.e., a few small full grids-worth)
    for x in range(0, 4):
        y = __BFS(inputs, start, part1=False, numSteps=start[0]+x*M) 
        Xs.append(x)
        Ys.append(y)

    # Convert all but the last data point to numpy arrays and fit to a quadratic 
    Xs_np = np.array(Xs[:-1])
    Ys_np = np.array(Ys[:-1])
    p = np.polyfit(Xs_np, Ys_np, 2)

    # This polynomial should have r^2 = 1, convert coefficients to integers to be exact
    # Our formula is Y = a*X^2 + b*X + c 
    p = np.poly1d(np.array([int(round(x)) for x in p]))

    # Sanity check: make sure our polynomial is actually correctly calculating our last data point
    assert p(Xs[-1]) == Ys[-1], f"Polynomial/quadratic fit isn't exact: {p(Xs[-1])} != {Ys[-1]}"

    # Now that we're confident in our polynomial fit, calculate the real deal!
    x_out = (numSteps - start[0]) / M
    out = p(int(x_out))
    return out
    
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
