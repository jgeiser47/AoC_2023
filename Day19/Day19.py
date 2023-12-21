'''
    What: Advent of Code 2023 - Day 19
    Who: Josh Geiser
'''

from pathlib import Path
from copy import deepcopy

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_input(inputs):
    '''
    Helper function for part 1. Parse our input, returning a dictionary of 
    "workflows" and a list of "ratings"
    '''

    # Iterate through rows until we've reached the end of our "workflows"
    # value of workflows will be a comma-delimited list of string "conditions"
    workflows = {}
    for i,row in enumerate(inputs):
        if len(row) == 0:
            break

        key, val = row.split('{')
        val = val.replace('}', '').split(',')
        workflows[key] = val

    # Iterate through all of our "ratings" next
    # "ratings" will be a list of dicts with key = 'x','m','a', or 's' and
    # value = integer
    ratings = []
    for j in range(i+1, len(inputs)):
        row = inputs[j]
        row = row.replace('{', '').replace('}', '').split(',')
        row = {x.split('=')[0]:int(x.split('=')[1]) for x in row}
        ratings.append(row)

    return workflows, ratings

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __check_condition(rating, condition):
    '''
    Helper function for part 1. Given a string condition, return the next workflow
    to go to if the condition is met, otherwise return None.
    '''

    # True if we've got a greater than sign, false otherwise
    greater_than = '>' in condition

    # Greater than check
    if greater_than:
        if rating[condition[0]] > int(condition.split('>')[1].split(':')[0]):
            return condition.split(':')[1]
        else:
            return None
    
    # Less than check
    else:
        if rating[condition[0]] < int(condition.split('<')[1].split(':')[0]):
            return condition.split(':')[1]
        else:
            return None

    # Hopefully we never get here
    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __check_workflow(rating, workflows, key):
    '''
    Helper function for part 1. Checks a particular workflow, returning the next
    workflow to go to.
    '''

    # Get our conditions for the given workflow key
    conditions = workflows[key]

    # Iterate through all but the last "condition". If any condition is true, 
    # immediately return the next workflow to go to.
    for i in range(len(conditions)-1):
        condition = conditions[i]
        potential_next = __check_condition(rating, condition)

        if potential_next is not None:
            return potential_next

    # If we've got to the last condition (which isn't really a condition), go
    # to this workflow
    return conditions[-1]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __check_workflows(rating, workflows):
    '''
    Helper function for part 1. Wrapper for checking all workflows for a given
    rating until we get to one of the terminal states
    '''

    # Iterate until we hit 'R' or 'A', and return whichever it is
    next = 'in'
    while (next != 'R' and next != 'A'):
        next = __check_workflow(rating, workflows, next)
    return next

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - iterate through each of our ratings, adding to our 
    output sum if it is "accepted".
    '''
    
    # Get our dict of workflows and list of ratings
    workflows, ratings = __parse_input(inputs)

    # Now iterate through each rating
    sum_out = 0
    for rating in ratings:
        end = __check_workflows(rating, workflows)

        # If this rating has been accepted, add its sum to output
        if end == 'A':
            sum_out += sum(rating.values())

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __calc_combos(ranges:dict):
    '''
    Helper function for part 2 - calculate number of unique combinations given 
    ranges of x, m, a, and s
    '''
    ranges = [val[1] - val[0] + 1 for val in ranges.values()]
    return ranges[0] * ranges[1] * ranges[2] * ranges[3]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __condition_helper(condition):
    '''
    Helper function for part 2 - given a string "condition", parses out and 
    returns a 4-tuple of (string letter, boolean greater_than, int threshold, 
    and string next_workflow)
    '''

    # True if we've got a greater than sign, false otherwise
    greater_than = '>' in condition

    # Return 4-tuple
    if greater_than:
        return condition[0], greater_than, int(condition.split('>')[1].split(':')[0]), condition.split(':')[1]
    else:
        return condition[0], greater_than, int(condition.split('<')[1].split(':')[0]), condition.split(':')[1]

    # Hopefully we never get here
    raise SyntaxError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_combos(workflows, ranges, curr):
    '''
    Helper function for part 2 - uses recursive logic to look at subsets of ranges
    of x, m, a, and s variables for all possible "paths" through our workflows
    '''

    # Sanity check: our ranges should be such that the second value is always >= the first
    assert all([x[1] >= x[0] for x in ranges.values()])

    # BASE CASE(s) ##############################################################

    # Rejected cases
    if curr == 'R':
        return 0
    
    # Sum up all of our possible permutations of accepted cases within range(s)
    if curr == 'A': 
        return __calc_combos(ranges)
    
    # RECURSIVE CASE ############################################################

    sum_out = 0

    # Get our conditions for the given workflow key
    conditions = workflows[curr]

    # Iterate through all but the last "condition"
    for i in range(len(conditions)-1):
        letter, greater_than, threshold, potential_next = __condition_helper(conditions[i])

        # Current condition has a greater than check
        if greater_than:

            # If our min range is greater than threshold, this condition is always true
            if ranges[letter][0] > threshold:
                new_ranges = deepcopy(ranges)
                sum_out += __get_combos(workflows, new_ranges, potential_next)

            # If our max range is leq our threshold, this condition is always false
            elif ranges[letter][1] <= threshold:
                continue

            # Otherwise, if condition is in the middle of our range, we'll need to split
            else:

                # The split side that does meet the new condition
                new_ranges = deepcopy(ranges)
                new_ranges[letter][0] = threshold + 1
                sum_out += __get_combos(workflows, new_ranges, potential_next)

                # The split side that does not meet the new condition
                ranges[letter][1] = threshold

        # Current condition has a less than check
        else: 

            # If our max range is less than threshold, this condition is always true
            if ranges[letter][1] < threshold:
                new_ranges = deepcopy(ranges)
                sum_out += __get_combos(workflows, new_ranges, potential_next)

            # If our min range is geq our threshold, this condition is always false
            elif ranges[letter][0] >= threshold:
                continue

            # Otherwise, if condition is in the middle of our range, we'll need to split
            else:

                # The split side that does meet the new condition
                new_ranges = deepcopy(ranges)
                new_ranges[letter][1] = threshold - 1
                sum_out += __get_combos(workflows, new_ranges, potential_next)

                # The split side that does not meet the new condition
                ranges[letter][0] = threshold

    # Now we can't forget about the last "condition" (which isn't really a condition)
    sum_out += __get_combos(workflows, deepcopy(ranges), conditions[-1])

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - uses recursive logic to find all possible combinations
    of ranges that will traverse through all possible "paths" through workflows
    '''

    # Get our dict of workflows and list of ratings
    workflows, _ = __parse_input(inputs)

    # Start with full ranges of each variable. These will get split up into 
    # separate recursive calls as we go.
    ranges = {
        'x': [1, 4000],
        'm': [1, 4000],
        'a': [1, 4000],
        's': [1, 4000]
    }

    # Start recursive calls!
    sum_out = __get_combos(workflows, ranges, 'in')

    return sum_out
    
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
