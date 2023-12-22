'''
    What: Advent of Code 2023 - Day 17
    Who: Josh Geiser
'''

from pathlib import Path
from queue import PriorityQueue

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __sim_paths(grid, part1=True):
    '''
    Helper function for parts 1 and 2 - use Dijkstra's algorithm to find the min
    cost path between starting point and end state!
    '''

    # Other variables we'll use
    visited = {}
    pq = PriorityQueue()

    # Add start point(s) to the priority queue
    start1 = (0, 0, '>', 0) 
    pq.put((0, start1))
    visited[start1] = 0

    # Add start point(s) to the priority queue
    start2 = (0, 0, 'v', 0)
    pq.put((0, start2))
    visited[start2] = 0

    # Dijkstra: Iterate until queue is empty
    while (not pq.empty()):

        # Get current node/state, and also its priority (cost_so_far)
        cost_so_far, curr = pq.get()

        # If this is our endpoint -> return!
        if (curr[0] == len(grid)-1) and (curr[1] == len(grid[0])-1) and (part1 or curr[3] >= 4):
            return cost_so_far

        # Otherwise, get each of this node's neighbors  
        neighs = __get_neighs(grid, curr) if part1 else __get_neighs_v2(grid, curr)

        # For each neighbor in list of neighbors...
        for neigh in neighs:

            # Calculate the new cost total cost to get to this state
            added_cost = int(grid[neigh[0]][neigh[1]])
            total_cost = cost_so_far + added_cost

            # If we haven't visited this state, add it's cost to our dict and add to pq
            if neigh not in visited:
                visited[neigh] = total_cost
                pq.put((total_cost, neigh))

            # If we have visited this state but our new path is better, update dict and add to pq
            elif neigh in visited and total_cost < visited[neigh]:
                visited[neigh] = total_cost

    # Hopefully we don't get here!
    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_neighs(grid, curr):
    '''
    Helper function for part 1 - get neighbor states of current "state".
    State represented by a 4-tuple (row, col, direction, numSteps)
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Unpack current state
    row, col, direction, numSteps = curr

    # Directions to visit our potential neighbors - order is left, straight, right
    mapping = {
        '>': [(-1, 0), (0, +1), (+1, 0)],
        'v': [(0, +1), (+1, 0), (0, -1)],
        '<': [(+1, 0), (0, -1), (-1, 0)],
        '^': [(0, -1), (-1, 0), (0, +1)]
    }
    potential_neighs = mapping[direction]

    # Adjacent directions
    left  = {'>':'^', 'v':'>', '<':'v', '^':'<'}
    right = {'>':'v', 'v':'<', '<':'^', '^':'>'}

    # Iterate through each potential neighbor to see if it's a valid neighbor to add
    out = []
    for i,potential_neigh in enumerate(potential_neighs):
        neigh_row, neigh_col = row+potential_neigh[0], col+potential_neigh[1]

        # Don't add if we're outside of dimensions
        if not ((0 <= neigh_row < m) and (0 <= neigh_col < n)):
            continue

        # Turn left
        if i == 0:
            out.append((neigh_row, neigh_col, left[direction], 1))

        # Turn right
        elif i == 2: 
            out.append((neigh_row, neigh_col, right[direction], 1))

        # Straight (and less than 3 steps)
        elif numSteps < 3:
            out.append((neigh_row, neigh_col, direction, numSteps+1))

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - use Dijkstra's algorithm
    '''
    min_heat_loss = __sim_paths(inputs)
    return  min_heat_loss

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_neighs_v2(grid, curr):
    '''
    Helper function for part 2 - get neighbor states of current "state".
    State represented by a 4-tuple (row, col, direction, numSteps)
    '''

    # Grid dimensions
    m = len(grid)
    n = len(grid[0])

    # Unpack current state
    row, col, direction, numSteps = curr

    # Directions to visit our potential neighbors - order is left, straight, right
    mapping = {
        '>': [(-1, 0), (0, +1), (+1, 0)],
        'v': [(0, +1), (+1, 0), (0, -1)],
        '<': [(+1, 0), (0, -1), (-1, 0)],
        '^': [(0, -1), (-1, 0), (0, +1)]
    }
    potential_neighs = mapping[direction]

    # Adjacent directions
    left  = {'>':'^', 'v':'>', '<':'v', '^':'<'}
    right = {'>':'v', 'v':'<', '<':'^', '^':'>'}

    # Iterate through each potential neighbor to see if it's a valid neighbor to add
    out = []
    for i,potential_neigh in enumerate(potential_neighs):
        neigh_row, neigh_col = row+potential_neigh[0], col+potential_neigh[1]

        # Don't add if we're outside of dimensions
        if not ((0 <= neigh_row < m) and (0 <= neigh_col < n)):
            continue

        # Turn left
        if i == 0:
            if numSteps >= 4:
                out.append((neigh_row, neigh_col, left[direction], 1))

        # Turn right
        elif i == 2: 
            if numSteps >= 4:
                out.append((neigh_row, neigh_col, right[direction], 1))

        # Straight
        else:
            if numSteps < 10:
                out.append((neigh_row, neigh_col, direction, numSteps+1))

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - use Dijkstra's algorithm (again!)
    '''
    min_heat_loss = __sim_paths(inputs, part1=False)
    return  min_heat_loss
    
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
