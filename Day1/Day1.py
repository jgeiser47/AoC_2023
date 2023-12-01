'''
    What: Advent of Code 2023 - Day 1
    Who: Josh Geiser
'''

from pathlib import Path

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        x = f.readlines()
    return x

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):

    sum = 0
    for input in inputs:
        row = [int(x) for x in input if x.isdigit()]
        sum += row[0]*10 + row[-1]

    return sum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):

    mapping = {
        'zero' : 0,
        'one'  : 1,
        'two'  : 2,
        'three': 3,
        'four' : 4,
        'five' : 5,
        'six'  : 6,
        'seven': 7,
        'eight': 8,
        'nine' : 9,
        '0'    : 0,
        '1'    : 1,
        '2'    : 2,
        '3'    : 3,
        '4'    : 4,
        '5'    : 5,
        '6'    : 6,
        '7'    : 7,
        '8'    : 8,
        '9'    : 9,
    }

    sum = 0
    for input in inputs:
        input = input.strip()

        row = []
        for i in range(len(input)):
            for k,v in mapping.items():
                if input[i:i+len(k)] == k:
                    row.append(v)

        newval = row[0]*10 + row[-1]
        sum += newval

    return sum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    # Read in our input file
    here = Path(__file__).parent
    infile = here / 'input.txt'
    inputs = read_input(infile)

    # Get our first star!
    answer_1 = task_1(inputs)
    print(answer_1)

    # Now get our second!
    answer_2 = task_2(inputs)
    print(answer_2)

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()