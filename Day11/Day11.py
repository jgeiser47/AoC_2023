'''
    What: Advent of Code 2023 - Day 11
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
def __get_galaxies(inputs):
    '''
    Helper function for parts 1 and 2 to get the coordinates of all of our galaxies
    '''

    # Grid dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Get coordinates of all of our galaxies as a list of (row, col) tuples
    out = []
    for i in range(m):
        for j in range(n):
            if inputs[i][j] == '#':
                out.append((i,j))

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_rowscols_to_add(inputs, galaxies):
    '''
    Helper fucnction for parts 1 and 2 for getting "empty" rows and columns
    '''

    # Grid dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Iterate through each galaxy, removing its row/col from the set of "empty" rows/cols
    rows_to_add = set(range(m))
    cols_to_add = set(range(n))
    for galaxy in galaxies:
        if galaxy[0] in rows_to_add:
            rows_to_add.remove(galaxy[0])
        if galaxy[1] in cols_to_add:
            cols_to_add.remove(galaxy[1])

    return rows_to_add, cols_to_add

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __update_grid(inputs, galaxies):
    '''
    Helper function for part 1 for updating our grid of coordinates
    '''

    # Grid dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Get rows and columns to add multiples to
    rows_to_add, cols_to_add = __get_rowscols_to_add(inputs, galaxies)

    # Turn these into lists in descending order
    cols_to_add = list(cols_to_add)
    cols_to_add.sort(reverse=True)
    rows_to_add = list(rows_to_add)
    rows_to_add.sort(reverse=True)

    # Add columns
    for row in range(m):
        for col_to_add in cols_to_add:
            inputs[row] = inputs[row][:col_to_add] + '.' + inputs[row][col_to_add:]

    # Now add rows
    for row_to_add in rows_to_add:
        inputs.insert(row_to_add, len(inputs[0])*'.')


    return inputs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_L1_norm(galaxy1, galaxy2):
    return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Part 1 main method
    '''

    # Get our initial set of galaxies, update our map, then get the new coordinates
    galaxies_initial = __get_galaxies(inputs)
    inputs = __update_grid(inputs, galaxies_initial)
    galaxies = __get_galaxies(inputs)

    # Iterate through each pair exactly once, adding distances to our sum
    sum_out = 0
    num_galaxies = len(galaxies)
    for i in range(0, num_galaxies-1):
        for j in range(i+1, num_galaxies):
            sum_out += __get_L1_norm(galaxies[i], galaxies[j])

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_fancy_L1_norm(galaxy1, galaxy2, empt_rows, empt_cols, mult_fact=1000000):
    '''
    Helper function for part 2 for getting our "modified" L1 norms 
    '''

    # Helper variables to make this easier
    row1 = galaxy1[0]
    col1 = galaxy1[1]
    row2 = galaxy2[0]
    col2 = galaxy2[1]

    # For every empty row that we cross, add out multiplication factor 
    row_dist = abs(row1 - row2)
    for empt_row in empt_rows:
        if row1 < row2 and row1 < empt_row < row2:
            row_dist += mult_fact - 1
        elif row2 < row1 and row2 < empt_row < row1:
            row_dist += mult_fact - 1

    # For every empty column that we cross, add out multiplication factor 
    col_dist = abs(col1 - col2)
    for empt_col in empt_cols:
        if col1 < col2 and col1 < empt_col < col2:
            col_dist += mult_fact - 1
        elif col2 < col1 and col2 < empt_col < col1:
            col_dist += mult_fact - 1

    # Now return the "modified" L1 norm
    return row_dist + col_dist

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Part 2 main method
    '''

    # Get our galaxy coordinates and also coordinates to empty rows/cols
    galaxies = __get_galaxies(inputs)
    empt_rows, empt_cols = __get_rowscols_to_add(inputs, galaxies)

    # Iterate through each pair exactly once, adding distances to our sum
    sum_out = 0
    num_galaxies = len(galaxies)
    for i in range(0, num_galaxies-1):
        for j in range(i+1, num_galaxies):
            sum_out += __get_fancy_L1_norm(galaxies[i], galaxies[j], empt_rows, empt_cols)

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
