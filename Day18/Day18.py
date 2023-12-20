'''
    What: Advent of Code 2023 - Day 18
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
def __get_row(input):
    return tuple(input.split(' '))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_exterior(inputs):
    '''
    Helper function for part 1 to get the set of all of our exterior coordinates
    '''

    # Defining some variables
    dirs = {
        'R' : (0, +1),
        'L' : (0, -1),
        'U' : (-1, 0),
        'D' : (+1, 0)
    }
    exterior = set()

    # Startpoint 
    curr_pt = (0, 0)

    # Iterate through each row of our input, getting the direction and number of steps
    for input in inputs:
        dir, numSteps, color = __get_row(input)

        # Add current point to our exterior (if it's not already in there)
        exterior.add(curr_pt)

        # Keep iterating in this direction for however many number of steps, adding points as we go
        for i in range(int(numSteps)):
            curr_pt = (curr_pt[0] + dirs[dir][0], curr_pt[1] + dirs[dir][1])
            exterior.add(curr_pt)

    return exterior

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __BFS_inside_loop(exterior):
    '''
    Helper function for part 1 to get all of our interior points using simple BFS
    '''

    # Directions to visit our potential neighbors
    dirs = [(0, +1), (-1, 0), (0, -1), (+1, 0)]

    # Other variables we'll use in BFS
    visited = set()
    q = Queue()

    # Add start point to the queue
    curr = (1, 1)
    q.put(curr)
    visited.add(curr)

    # BFS: Iterate until queue is empty
    while (not q.empty()):

        # Get neighbors of curr
        curr = q.get()
        for dir in dirs:
            neigh = (curr[0] + dir[0], curr[1] + dir[1])

            # If we haven't visited this neighbor yet and it's a valid neighbor, add it to queue
            if neigh not in exterior and neigh not in visited:
                q.put(neigh)
                visited.add(neigh)

    return visited

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - main idea is to define the exterior of our shape, and
    then use BFS to get the interior. Afterwards, sum up the size of the interior
    and exterior to get total area.
    '''
    exterior = __get_exterior(inputs)
    interior = __BFS_inside_loop(exterior)
    return len(interior) + len(exterior)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_instr(row):
    '''
    Helper function for part 2 to get the directions from a given row of our input
    file. 
    '''

    # Mapping of last digit in hex/color to direction
    dir_map = {
        '0' : 'R',
        '1' : 'D',
        '2' : 'L',
        '3' : 'U'
    }

    # Get our number of steps (in hex) and direction (as an integer)
    _, _, color = row.split(' ')
    color = color.replace('(#', '').replace(')', '')
    steps_hex, dir = color[:-1], color[-1]

    # Convert steps to decimal and convert direction to char before returning
    steps = int(steps_hex, 16)
    dir = dir_map[dir]
    return (dir, steps)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_vertices(inputs):
    '''
    Helper function for part 2. Iterate through our instructions, making a list 
    of all of the vertices of the polygon shape we're constructing. Function also 
    returns the circumference of the polygon in addition to the list of vertices. 
    '''

    # Make a list of tuples defining the vertices of our polygon
    curr = (0, 0)
    vertices = [curr]

    # We'll also be calculating our circumference of our polygon as we go
    circumference = 0

    # Iterate through each row getting the direction and appending to our list of vertices
    for input in inputs:

        # Helper function for getting our actual instruction from the current row in input file
        dir, numSteps = __get_instr(input)

        # Update the current vertex depending on what direction we're going
        if dir == 'R':
            curr = (curr[0], curr[1] + numSteps)
        elif dir == 'L':
            curr = (curr[0], curr[1] - numSteps)
        elif dir == 'U':
            curr = (curr[0] - numSteps, curr[1])
        elif dir == 'D':
            curr = (curr[0] + numSteps, curr[1])

        # Update outputs
        vertices.append(curr)
        circumference += numSteps

    return vertices, circumference

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __shoelace(vertices):
    '''
    Helper function for part 2. Thank god for the shoelace formula.
    (https://en.wikipedia.org/wiki/Shoelace_formula)
    '''

    # Get all of our x and y coordinates in two separate lists (had to do some 
    # finagling so I can visualize it in a standard cartesian axis)
    xs = [vertex[1] for vertex in vertices]
    ys = [-1*vertex[0] for vertex in vertices]

    # Do one side of our shoelace
    pluses = 0
    for i in range(len(xs) - 1):
        pluses += xs[i] * ys[i+1]

    # Now do the other side of our shoelace
    minuses = 0
    for i in range(len(ys) - 1):
        minuses += ys[i] * xs[i+1]

    # Now finish tieing our shoes!
    area = abs(pluses - minuses) / 2

    return area

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - Main idea is to get all of the vertices of our polygon
    and then use the shoelace formula to calculate the area of the enclosed shape.
    '''

    # Get our list of vertices, circumference of our polygon, and interior area
    vertices, circumference = __get_vertices(inputs)
    interior_area = __shoelace(vertices)

    # Since we have a discrete grid, need to also add half of the circumference 
    # to our output "area"
    output = interior_area + ((circumference/2) + 1)
    return int(output)
    
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
