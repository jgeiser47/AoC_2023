'''
    What: Advent of Code 2023 - Day 15
    Who: Josh Geiser
'''

from pathlib import Path
import numpy as np

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip().split(',') for x in data][0]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __hash(string):
    '''
    Helper function for parts 1 and 2 to determine the hash of a string
    '''

    # Follow the steps listed in the procedure
    str_out = 0
    for char in string:
        str_out += ord(char)
        str_out *= 17
        str_out %= 256 

    return str_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method
    '''
    
    # Iterate through each string and sum the individual hashes
    curr_val = 0
    for string in inputs:
        curr_val += __hash(string)

    return curr_val

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __process(string, hashmap):
    '''
    Helper function for part 2 for updating our hashmap with each new entry
    '''

    # True if operation char is a dash, false if it's an equals sign
    dash = '-' in string

    # Dash
    if dash:

        # Get our current label, box number, and all of the labels in that box
        label = string.split('-')[0]
        box = __hash(label)
        box_keys = [x[0] for x in hashmap[box]]

        # If this label already exists in this box, delete it (if not, do nothing)
        if label in box_keys:
            del hashmap[box][box_keys.index(label)]

    # Equals
    else:

        # Get our current label, box number, and all of the labels in that box
        label, focal_length = string.split('=')
        box = __hash(label)
        box_keys = [x[0] for x in hashmap[box]]

        # If this label already exists in this box, update the focal length
        if label in box_keys:
            hashmap[box][box_keys.index(label)] = (label, focal_length)

        # If this label does not already exist, add it
        else:
            hashmap[box].append((label, focal_length))

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __calc_out(hashmap):
    '''
    Helper function for part 2 for summing up our output hashmap
    '''

    # Follow the procedure for calculating our output sum
    sum_out = 0
    for box_num, box_items in hashmap.items():
        for slot, item in enumerate(box_items):
            sum_out += (1+box_num) * (1+slot) * (int(item[1]))

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method
    '''

    # Initialize our hashmap
    hashmap = {}
    for i in range(256):
        hashmap[i] = []

    # Update our hashmap with each string
    for string in inputs:
        __process(string, hashmap)

    # Calculate hashmap "value" and output
    output = __calc_out(hashmap)
    return output
    
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
