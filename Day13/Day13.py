'''
    What: Advent of Code 2023 - Day 13
    Who: Josh Geiser
'''

from pathlib import Path
import numpy as np

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_inputs(inputs):
    '''
    Helper function for parts 1 and 2 to parse the input into a list of grids for
    each case.
    '''

    # Get individual "grids" (list of strings) and put each into a list
    out = []
    start = 0
    for i in range(len(inputs)):
        if inputs[i] == '':
            out.append(inputs[start:i])
            start = i+1

    # Don't forget to add the last one
    out.append(inputs[start:])

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __compare(list1, list2):
    '''
    Helper function for parts 1 and 2, compare two lists (or two strings) and 
    return the number of elements (chars) that differ between the two
    '''

    diffs = 0
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            diffs += 1

    return diffs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_row(grid, i, m):
    '''
    Helper function for part 1 - determine if grid is symmetric about this given 
    row
    '''

    # Iterate in negative and positive directions around this row
    neg = i
    pos = i+1
    while neg >=0 and pos < m:
        
        # If any of the elements are different, then this isn't our mirrored row
        if __compare(grid[neg], grid[pos]) > 0:
            return None
        
        # Otherwise, keep checking mirrored entries
        else:
            neg -= 1
            pos += 1

    # Return the row number if it's the mirror, otherwise None
    return i

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_col(grid, j, n):
    '''
    Helper function for part 1 - determine if grid is symmetric about this given 
    column
    '''

    # Iterate in negative and positive directions around this column
    neg = j
    pos = j+1
    while neg >=0 and pos < n:

        # Get a specific column out of our grid
        neg_col = [row[neg] for i,row in enumerate(grid)]
        pos_col = [row[pos] for i,row in enumerate(grid)]

        # If any of the elements are different, then this isn't our mirrored row
        if __compare(neg_col, pos_col) > 0:
            return None
        
        # Otherwise, keep checking mirrored entries
        else:
            neg -= 1
            pos += 1

    # Return the column number if it's the mirror, otherwise None
    return j

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_mirror(grid):
    '''
    Helper function for part 1 - determine the mirrored row/col for a given grid
    '''

    # Grid is m by n dimension
    m = len(grid)
    n = len(grid[0])

    # First check rows (horizontal mirror)
    for i in range(m-1):
        row_out = __get_row(grid, i, m)
        if row_out is not None:
            return (row_out+1) * 100

    # Then check columns (vertical mirror)
    for j in range(n-1):
        col_out = __get_col(grid, j, n)
        if col_out is not None:
            return (col_out+1)

    # Hopefully we never get here!
    raise ValueError('Error')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    
    # Get our inputs as an array of arrays of strings
    inputs = __parse_inputs(inputs)

    # Iterate through each individual grid adding to our output sum
    sum_out = 0
    for grid in inputs:
        sum_out += __get_mirror(grid)

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_row_v2(grid, i, m):
    '''
    Helper function for part 2 - determine if grid is symmetric about this given 
    row GIVEN one "smudge"
    '''

    # If we have found our one "smudge", turn this boolean to false
    switch_left = True

    # Iterate in negative and positive directions around this row
    neg = i
    pos = i+1
    while neg >=0 and pos < m:

        # Number of differences between two lists
        diffs = __compare(grid[neg], grid[pos])

        # If we have more than 1 difference or we have 1 but have already used
        # our smudge, then this isn't our mirror
        if diffs > 1 or (diffs == 1 and not switch_left):
            return None
        
        # If we haven't used our smudge and only have 1 difference, this may be 
        # our smudge!
        elif diffs == 1:
            switch_left = False

        # Decrement/increment indices accordingly
        neg -= 1
        pos += 1

    # If we had exactly 1 smudge and got here, this is our new mirror!
    return i if not switch_left else None

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_col_v2(grid, j, n):
    '''
    Helper function for part 2 - determine if grid is symmetric about this given 
    column GIVEN one "smudge"
    '''

    # If we have found our one "smudge", turn this boolean to false
    switch_left = True

    # Iterate in negative and positive directions around this row
    neg = j
    pos = j+1
    while neg >=0 and pos < n:

        # Get a specific column out of our grid
        neg_col = [row[neg] for i,row in enumerate(grid)]
        pos_col = [row[pos] for i,row in enumerate(grid)]

        # Number of differences between two lists
        diffs = __compare(neg_col, pos_col)

        # If we have more than 1 difference or we have 1 but have already used
        # our smudge, then this isn't our mirror
        if diffs > 1 or (diffs == 1 and not switch_left):
            return None
        
        # If we haven't used our smudge and only have 1 difference, this may be 
        # our smudge!
        elif diffs == 1:
            switch_left = False

        # Decrement/increment indices accordingly 
        neg -= 1
        pos += 1

    # If we had exactly 1 smudge and got here, this is our new mirror!
    return j if not switch_left else None

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_mirror_v2(grid):
    '''
    Helper function for part 2 - determine the mirrored row/col for a given grid
    GIVEN that there is exactly one "smudge"
    '''

    # Grid is m by n dimension
    m = len(grid)
    n = len(grid[0])

    # First check rows (horizontal mirror)
    for i in range(m-1):
        row_out = __get_row_v2(grid, i, m)
        if row_out is not None:
            return (row_out+1) * 100

    # Then check columns (vertical mirror)
    for j in range(n-1):
        col_out = __get_col_v2(grid, j, n)
        if col_out is not None:
            return (col_out+1)

    # Hopefully we never get here!
    raise ValueError('Error')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):

    # Get our inputs as an array of arrays of strings
    inputs = __parse_inputs(inputs)

    # Iterate through each individual grid adding to our output sum
    sum_out = 0
    for grid in inputs:
        sum_out += __get_mirror_v2(grid)

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
