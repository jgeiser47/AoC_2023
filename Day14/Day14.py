'''
    What: Advent of Code 2023 - Day 14
    Who: Josh Geiser
'''

from pathlib import Path
import numpy as np

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [list(x.strip()) for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_sum(grid):
    '''
    Helper function for parts 1 and 2 - get the output sum of the grid
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    sum_out = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'O':
                sum_out += m - i

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    
    # Grid dimensions
    grid = inputs
    m = len(grid)
    n = len(grid[0])

    # Iterate through each column separately
    for j in range(n):

        i = 0
        for k in range(m):
            if grid[k][j] == 'O':
                grid[k][j] = '.'
                grid[i][j] = 'O'
                i += 1
            elif grid[k][j] == '#':
                i = k + 1

    # Get sum
    sum_out = __get_sum(grid)

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __north(grid):
    '''
    Go north!
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Iterate through each column separately
    for j in range(n):

        i = 0
        for k in range(m):
            if grid[k][j] == 'O':
                grid[k][j] = '.'
                grid[i][j] = 'O'
                i += 1
            elif grid[k][j] == '#':
                i = k + 1

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __west(grid):
    '''
    Go west!
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Iterate through each row separately
    for i in range(m):

        j = 0
        for k in range(n):
            if grid[i][k] == 'O':
                grid[i][k] = '.'
                grid[i][j] = 'O'
                j += 1
            elif grid[i][k] == '#':
                j = k + 1

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __south(grid):
    '''
    Go south!
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Iterate through each column separately
    for j in range(n):

        i = m-1
        for k in range(m-1, -1, -1):
            if grid[k][j] == 'O':
                grid[k][j] = '.'
                grid[i][j] = 'O'
                i -= 1
            elif grid[k][j] == '#':
                i = k - 1

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __east(grid):
    '''
    Go east!
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Iterate through each row separately
    for i in range(m):

        j = n-1
        for k in range(n-1, -1, -1):
            if grid[i][k] == 'O':
                grid[i][k] = '.'
                grid[i][j] = 'O'
                j -= 1
            elif grid[i][k] == '#':
                j = k - 1

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __cycle(grid):
    '''
    Perform one full cycle of north -> west -> south -> east
    '''
    __north(grid)
    __west(grid)
    __south(grid)
    __east(grid)

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __to_str(grid):
    return ''.join([''.join(x) for x in grid])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):

    # Some variables
    grid = inputs
    hashmap = {}

    # Cycle to infinity! But in reality we should never have to iterate this far...
    for numCycles in range(1000000000):
        __cycle(grid)

        # Hash the grid
        grid_str = __to_str(grid)

        # If we've seen this grid before, then yay we're now in a loop! Calculate
        # how many cycles it takes to repeat this loop and then break out of it
        if grid_str in hashmap:
            numRepeats = numCycles - hashmap[grid_str]
            break

        # Otherwise, add this grid to our hashmap
        else:
            hashmap[grid_str] = numCycles

    # Calculate how many additional times we need to iterate to get to the proper
    # end configuration
    numTimesMore = (1000000000 - numCycles) % numRepeats

    # And now iterate just a few more times...
    for numCycles in range(numTimesMore-1):
        __cycle(grid)

    # Get sum
    sum_out = __get_sum(grid)

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
