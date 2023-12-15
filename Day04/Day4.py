'''
    What: Advent of Code 2023 - Day 4
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

    # Do everything
    sum = 0
    for input in inputs:
        left, right = input[input.index(':')+2:].split('|')
        left = [x for x in left.strip().split(' ') if len(x)>0]
        right = [x for x in right.strip().split(' ') if len(x)>0]

        numMatches = len([r for r in right if r in left])
        if numMatches > 0:
            sum += 2 ** (numMatches-1)

    return sum

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):

    # Helper variables
    inputs = [input.strip() for input in inputs]
    numCopies = {i:1 for i in list(range(1, len(inputs)+1))}

    card = 1
    for input in inputs:

        # Get number of matches
        left, right = input[input.index(':')+2:].split('|')
        left = [x for x in left.strip().split(' ') if len(x)>0]
        right = [x for x in right.strip().split(' ') if len(x)>0]
        numMatches = len([r for r in right if r in left])

        # Now figure out number of copies of below cards
        for cardToAdd in range(card+1, card+1+numMatches):
            if cardToAdd not in numCopies:
                numCopies[cardToAdd] = 1
            else:
                numCopies[cardToAdd] += numCopies[card]

        card += 1

    return sum(list(numCopies.values()))

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