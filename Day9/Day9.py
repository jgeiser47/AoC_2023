'''
    What: Advent of Code 2023 - Day 9
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
    
    out = [x.split(' ') for x in inputs]
    out = []
    for input in inputs:
        line = input.split(' ')
        out.append([int(x) for x in line])

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_updated_list(line):
    '''
    Helper function for part 1
    '''

    # Base case
    if (all(x == 0 for x in line)):
        return line + [0]
    
    # Recursive case
    new_line = []
    for i in range(len(line)-1):
        new_line.append(line[i+1] - line[i])

    # Append to end of list
    updated_new_line = __get_updated_list(new_line)
    line.append(line[-1] + updated_new_line[-1])

    return line

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):

    # Parse input
    inputs = __parse_input(inputs)

    # Iterate through each row making recursive calls and adding to sum
    sum = 0
    for line in inputs:
        new_line = __get_updated_list(line)
        sum += new_line[-1]

    return sum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_updated_list_v2(line):
    '''
    Helper function for part 2
    '''

    # Base case
    if (all(x == 0 for x in line)):
        return line + [0]
    
    # Recursive case
    new_line = []
    for i in range(len(line)-1):
        new_line.append(line[i+1] - line[i])

    # Prepend to front of list
    updated_new_line = __get_updated_list_v2(new_line)
    line.insert(0, line[0] - updated_new_line[0])

    return line

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):

    # Parse input
    inputs = __parse_input(inputs)

    # Iterate through each row making recursive calls and adding to sum
    sum = 0
    for line in inputs:
        new_line = __get_updated_list_v2(line)
        sum += new_line[0]

    return sum

    return
    

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
