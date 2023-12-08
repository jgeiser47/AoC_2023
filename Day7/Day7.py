'''
    What: Advent of Code 2023 - Day 7
    Who: Josh Geiser
'''

from pathlib import Path

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_input(inputs):
    '''
    Helper function for parts 1 and 2 to parse our input into two lists
    '''

    hands = []
    bids = []
    for input in inputs:
        input = input.split(' ')
        hands.append(input[0])
        bids.append(int(input[1]))

    return hands, bids


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __hand_strength(hand):
    '''
    Helper function for part 1 to determine the "strength" of a hand
    Returns a list where the first index is a numeric value for the "ranking" of 
    the hand (e.g. four-of-a-kind, two-pair, etc.), and the following values are
    the "rankings" of the individual cards (e.g., 'A' = 14, '9' = 9, etc.)
    '''

    # Get the number of occurences of each card
    mapping = {}
    for char in hand:
        if char in mapping:
            mapping[char] += 1
        else:
            mapping[char] = 1

    # Now map the hand to it's order of strength - 7 = 5-of-a-kind, 6 = 4-of-a-kind, etc.
    vals = mapping.values()
    if 5 in vals:
        first_val = 7
    elif 4 in vals:
        first_val = 6
    elif 3 in vals and 2 in vals:
        first_val = 5
    elif 3 in vals:
        first_val = 4
    elif 2 in vals and len(vals) == 3:
        first_val = 3
    elif 2 in vals and len(vals) == 4:
        first_val = 2
    else:
        first_val = 1
    
    # Now also add to the list all of the "tie-breakers" based on order of cards in hand
    str_mapping = {
        'T':10,
        'J':11,
        'Q':12,
        'K':13,
        'A':14
    }
    second_vals = [int(char) if char.isdigit() else str_mapping[char] for char in hand]

    # Return a list of values to compare chronologically to determine which hand is "higher"
    return [first_val] + second_vals

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __is_first_greater(list1, list2):
    '''
    Helper function for parts 1 and 2 to compare two lists for use in sorting algorithm
    '''

    for i in range(len(list1)):
        if list1[i] > list2[i]:
            return True
        elif list1[i] < list2[i]:
            return False
        else:
            continue

    return False

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):

    # Parse our input
    hands, bids = __parse_input(inputs)

    # Make a list "combined" that has tuples of (int bid, list of ranking of hand)
    combined = []
    for i,hand in enumerate(hands):
        combined.append((bids[i],__hand_strength(hand)))

    # Just do a simple O(n^2) sorting algorithm because I don't feel like coding
    # up mergesort right now
    for i in range(0, len(combined)-1):
        for j in range(i+1, len(combined)):
            if __is_first_greater(combined[i][1], combined[j][1]):
                temp = combined[j]
                combined[j] = combined[i]
                combined[i] = temp

    # Now calculate the output
    out = 0
    for i,vals in enumerate(combined):
        out += (i+1) * vals[0]
    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __hand_strength_v2(hand):
    '''
    Helper function for part 2 to determine the "strength" of a hand
    Returns a list where the first index is a numeric value for the "ranking" of 
    the hand (e.g. four-of-a-kind, two-pair, etc.), and the following values are
    the "rankings" of the individual cards (e.g., 'A' = 14, '9' = 9, etc.)
    '''

    # Get the number of occurences of each card
    mapping = {}
    for char in hand:
        if char in mapping:
            mapping[char] += 1
        else:
            mapping[char] = 1

    # If we have any Jokers, count the number of them
    numJack = 0 
    if 'J' in mapping:
        numJack = mapping['J']
        del mapping['J']

    # Now get the quantities of each card, and adjust for Jokers
    vals = list(mapping.values())
    if numJack > 0:

        # Edge case for if our hand is all Jokers, otherwise add our Jokers to our max instances of other card
        if (len(mapping) == 0):
            vals = [5]
        else:
            vals[vals.index(max(vals))] += numJack

    # Now map the hand to it's order of strength - 7 = 5-of-a-kind, 6 = 4-of-a-kind, etc.
    if 5 in vals:
        first_val = 7
    elif 4 in vals:
        first_val = 6
    elif 3 in vals and 2 in vals:
        first_val = 5
    elif 3 in vals:
        first_val = 4
    elif 2 in vals and len(vals) == 3:
        first_val = 3
    elif 2 in vals and len(vals) == 4:
        first_val = 2
    else:
        first_val = 1
    
    # Now also add to the list all of the "tie-breakers" based on order of cards in hand
    str_mapping = {
        'T':10,
        'J':1,
        'Q':12,
        'K':13,
        'A':14
    }
    second_vals = [int(char) if char.isdigit() else str_mapping[char] for char in hand]

    # Return a list of values to compare chronologically to determine which hand is "higher"
    return [first_val] + second_vals

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    
    # Parse our input
    hands, bids = __parse_input(inputs)

    # Make a list "combined" that has tuples of (int bid, list of ranking of hand)
    combined = []
    for i,hand in enumerate(hands):
        combined.append((bids[i],__hand_strength_v2(hand)))

    # Just do a simple O(n^2) sorting algorithm because I don't feel like coding
    # up mergesort right now
    for i in range(0, len(combined)-1):
        for j in range(i+1, len(combined)):
            if __is_first_greater(combined[i][1], combined[j][1]):
                temp = combined[j]
                combined[j] = combined[i]
                combined[i] = temp

    # Now calculate the output
    out = 0
    for i,vals in enumerate(combined):
        out += (i+1) * vals[0]
    return out

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
