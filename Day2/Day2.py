'''
    What: Advent of Code 2023 - Day 2
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

    maxVals = {
        'red' : 12,
        'green': 13,
        'blue' : 14
    }

    sum = 0
    for input in inputs:

        isRowValid = True
        input = input.strip()
        id = int(input.partition(':')[0].rpartition(' ')[2])

        sets = input.partition(':')[2].strip()
        for set in sets.split(';'):
            for single in set.strip().split(','):
                num, col = single.strip().split(' ')
                if (int(num) > maxVals[col]):
                    isRowValid = False
                    break

        if isRowValid:
            sum += id

    return sum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):

    sum = 0
    for input in inputs:

        minVals = {
            'red' : 0,
            'green': 0,
            'blue' : 0
        }
        sets = input.partition(':')[2].strip()
        for set in sets.split(';'):
            for single in set.strip().split(','):
                num, col = single.strip().split(' ')
                if (int(num) > minVals[col]):
                    minVals[col] = int(num)

        sum += minVals['red'] * minVals['green'] * minVals['blue']

    return sum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    here = Path(__file__).parent
    infile = here / 'input.txt'
    inputs = read_input(infile)

    answer_1 = task_1(inputs)
    print(answer_1)

    answer_2 = task_2(inputs)
    print(answer_2)

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()