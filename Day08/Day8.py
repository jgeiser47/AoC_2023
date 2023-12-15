'''
    What: Advent of Code 2023 - Day 8
    Who: Josh Geiser
'''

from pathlib import Path
import math

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_input(inputs):
    '''
    Helper function for parts 1 and 2
    '''

    # Get our first line as a strings of 0's (left) and 1's (right)
    first_line = inputs[0]
    first_line = first_line.replace('L', '0').replace('R', '1')

    # Now get the rest of the datafile as a map of strings -> tuples of strings
    mapping = {}
    for i in range(2,len(inputs)):
        line = inputs[i]
        k, v = line.split(' = ')
        v = v.replace('(', '').replace(')', '').replace(' ', '').split(',')
        mapping[k] = v

    return first_line, mapping

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):

    # Parse input
    first_line, mapping = __parse_input(inputs)

    # Starting point
    curr = 'AAA'
    i = 0

    # Iterate forever (until we return)
    N = len(first_line)
    while (True):

        # Use modulo to keep re-covering the first line of directions
        dir = first_line[i % N]
        curr = mapping[curr][int(dir)]
        i += 1

        # If we've got a match, return!
        if curr == 'ZZZ':
            return i 

    return -1 


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    
    # Parse input
    first_line, mapping = __parse_input(inputs)

    # Starting points
    currs = [x for x in mapping.keys() if x[-1] == 'A']

    # Iterate through each of our starting points until we find its corresponding 'Z' endpoint
    N = len(first_line)
    first_instances = []
    for curr in currs:

        # Iterate until we're at a node that ends in 'Z'
        i = 0
        while (True):

            # Use modulo to keep re-covering the first line of directions
            dir = first_line[i % N]
            curr = mapping[curr][int(dir)]
            i += 1

            # If we've got a match, add to our least-common-multiples list
            if curr[-1] == 'Z':
                first_instances.append(i)
                break

    # Now we can just return the least-common-multiple of our list
    return math.lcm(*first_instances)

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
