'''
    What: Advent of Code 2023 - Day 12
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
def __parse_inputs(inputs):
    '''
    Helper function for part 1 to parse our inputs into the format we want
    '''

    # We'll output an array of strings and array of numbers
    string_arr = []
    nums_arr = []
    for input in inputs:
        string, nums = input.split(' ')
        string_arr.append(string)
        nums_arr.append([int(x) for x in nums.split(',')])

    return string_arr, nums_arr

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __is_still_possible(curr_str, given_str):
    '''
    Helper function for part 1 to determine if our current case is still possible
    '''

    for i in range(len(given_str)):
        if (given_str[i] == '.' and curr_str[i] == '#') or (given_str[i] == '#' and curr_str[i] == '.'):
            return False
        
    return True

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __num_arrangements(curr_str, given_str, nums_left):
    '''
    Recursive function for part 1
    '''

    # Base Case(s) ##############################################################

    # If no longer a possible combination, then return 0
    if not __is_still_possible(curr_str, given_str):
        return 0
    
    # Otherwise, if we've used all of our nums, we don't need to recurse anymore so this is a base case
    if len(nums_left) == 0:

        # Replace remaining question marks with '.'s, if still possible then we've found a valid arrangement
        curr_str = curr_str.replace('?', '.')
        return 1 if __is_still_possible(curr_str, given_str) else 0
    
    # Recursive Case(s) #########################################################

    sum_out = 0
    
    # Calculate what's the max amount we can shift next number over by (based on
    # quantity of numbers left) and only iterate that far to the right
    start_q = curr_str.index('?')
    max_offset =  abs((sum(nums_left) + len(nums_left) - 1) - (len(given_str) - start_q))
    for i in range(start_q, max_offset+start_q+1):

        # If we're at end of string, just add ####'s, otherwise add ####'s + .
        new_chars = '.'*(i-start_q) + '#'*nums_left[0]
        if i + nums_left[0] < len(given_str):
            new_chars += '.'

        # Build the next string and make our next recursive call
        next_str = curr_str[:start_q] + new_chars + curr_str[start_q+len(new_chars):]
        assert len(next_str) == len(curr_str)
        sum_out += __num_arrangements(next_str, given_str, nums_left[1:])

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    
    # Get our inputs
    string_arr, nums_arr = __parse_inputs(inputs)

    # Do for all the numbers!
    sum_out = 0
    for i in range(len(string_arr)):
        curr_str = '?' * len(string_arr[i])
        curr_out = __num_arrangements(curr_str, string_arr[i], nums_arr[i])
        sum_out += curr_out

    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_inputs_v2(inputs):
    '''
    Helper function for part 2 to parse the inputs into the format we want - now
    we'll have each line be 5 times as long
    '''

    # We'll output an array of strings and array of numbers
    string_arr = []
    nums_arr = []
    for input in inputs:
        string, nums = input.split(' ')
        string = (string+'?')*5
        string_arr.append(string[:-1])
        nums_arr.append([int(x) for x in nums.split(',')] * 5)

    return string_arr, nums_arr

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __to_key(curr_str, curr_nums):
    '''
    Helper function for part 2 to make a hashable key of our current "state"
    '''
    return (curr_str, str(curr_nums))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __min_spots(curr_nums):
    '''
    Helper function for part 2 to return the minimum number of spots our current
    numbers list will take up
    '''
    return sum(curr_nums) + len(curr_nums) - 1

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __can_add_num_at_ind(curr_str, curr_num, i):
    '''
    Helper function for part 2 to determine if a number can be added at an index.
    If it can be added, return the next substring, if it can't then return None
    '''

    assert curr_num <= len(curr_str)

    # We need to add a continuous string of '####'s, so make sure there's no '.'s
    if '.' in curr_str[i:i+curr_num]:
        return None

    # We also can't have skipped over andy #'s
    if '#' in curr_str[:i]:
        return None
    
    # We also want to make sure that we have one space of '.' after our '####'s
    if i+curr_num < len(curr_str) and curr_str[i+curr_num] == '#':
        return None
    
    # If we've got here, return our next substring to look at
    return curr_str[i+curr_num+1:]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __num_arrangements_v2(curr_str, curr_nums, memo):
    '''
    Recursive function with memoization for task 2
    '''

    # Memoization by making a hashable key of our current "state"
    if __to_key(curr_str, curr_nums) in memo:
        return memo[__to_key(curr_str, curr_nums)]
    
    # Base Case(s) ##############################################################
    
    if len(curr_nums) == 0 and '#' not in curr_str:
        memo[__to_key(curr_str, curr_nums)] = 1
        return 1
    
    if len(curr_nums) == 0 and '#' in curr_str:
        memo[__to_key(curr_str, curr_nums)] = 0
        return 0
    
    if len(curr_str) == 0 and len(curr_nums) > 0:
        memo[__to_key(curr_str, curr_nums)] = 0
        return 0
    
    if len(curr_str) == 0 and len(curr_nums) == 0:
        memo[__to_key(curr_str, curr_nums)] = 1
        return 1
    
    # Recursive Case(s) ########################################################

    # Figure out how far to the right we should iterate over based on numbers left
    min_spots = __min_spots(curr_nums)
    last_ind_to_check = len(curr_str) - min_spots

    # Iterate 'til we shouldn't anymore
    sum_out = 0
    for i in range(last_ind_to_check + 1):
        
        # If we can add the next number at the given index, do it and make more recursive calls!
        new_substring = __can_add_num_at_ind(curr_str, curr_nums[0], i)
        if new_substring is not None:
            num_combos = __num_arrangements_v2(new_substring, curr_nums[1:], memo)
            sum_out += num_combos

    # Memoize and return
    memo[__to_key(curr_str, curr_nums)] = sum_out
    return sum_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Dynamic programming in the form of recursion + memoization
    '''
    
    # Get our inputs
    string_arr, nums_arr = __parse_inputs_v2(inputs)

    # Do for all the numbers!
    sum_out = 0
    memo = {}
    for i in range(len(inputs)):
        curr_out = __num_arrangements_v2(string_arr[i], nums_arr[i], memo)
        sum_out += curr_out

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