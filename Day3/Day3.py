'''
    What: Advent of Code 2023 - Day 3
    Who: Josh Geiser
'''

from pathlib import Path

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):

    with open(infile, 'r') as f:
        x = f.readlines()
    return x

def __isValidNum(inputs, num):
    '''
    Helper function for part 1
    '''

    # Array dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Start and end indices of our number in question
    i = num[1][0]
    j_start = num[1][1]
    j_end = num[1][1] + len(str(num[0])) - 1

    # Get tuples of all of our neighbor indices
    neighbor_inds = [(i, j_start-1), (i, j_end+1)]
    for j in range(j_start-1, j_end+2):
        neighbor_inds.append((i-1, j))
        neighbor_inds.append((i+1, j))

    # Check all of our neighbor indices, if any are a symbol return True, otherwise False
    bool_arr = [True if (0<=neigh[0]<m and 0<=neigh[1]<n and inputs[neigh[0]][neigh[1]] is not '.') else False for neigh in neighbor_inds]
    return any(bool_arr)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):

    # Make a 2d character array out of our input
    inputs = [input.strip() for input in inputs]

    # nums will contain tuples of the form (number, number_starting_index)
    nums = []

    # Iterate through rows...
    for i,input in enumerate(inputs):

        # Boolean to tell us if we're actively building a number
        buildingNum = False

        # Iterate through columns...
        for j,ch in enumerate(input):

            # If we're not in the middle of a number and we encounter a numeric digit, number starts here
            if (ch.isdigit() and not buildingNum):
                numStartInd = (i,j)
                buildingNum = True

            # Otherwise if we were building a number and we encounter something non-numeric, this is the end of the number
            elif (not ch.isdigit() and buildingNum):
                nums.append((int(input[numStartInd[1]:j]), numStartInd))
                buildingNum = False

        # If a number reached the end of a line, make sure to add this case as well
        if (buildingNum):
            nums.append((int(input[numStartInd[1]:]), numStartInd))

    # Check each of the neighbors and only add valid numbers to here
    nums = [num[0] for num in nums if __isValidNum(inputs, num)]

    return sum(nums)

def __getNum(inputs, neigh, visited):
    '''
    Helper function for part 2
    '''

    # Array dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Start and end indices for the number in question
    i = neigh[0]
    j_st = neigh[1]
    j_end = neigh[1]

    # Iterate the starting column index (j_st) to the left while we still can
    while(0<=j_st-1<n and inputs[i][j_st-1].isdigit()):
        j_st -= 1
        visited.add((i,j_st))

    # Iterate the end column index (j_end) to the right while we still can
    while(0<=j_end+1<n and inputs[i][j_end+1].isdigit()):
        j_end += 1
        visited.add((i,j_end))

    # Return our number
    return int(inputs[i][j_st:j_end+1])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):

    # Make a 2d character array out of our input
    inputs = [input.strip() for input in inputs]

    # Array dimensions
    m = len(inputs)
    n = len(inputs[0])

    # Other helpers
    dirs = [(-1,-1), (+0,-1), (+1,-1), (+1,+0), (+1,+1), (+0,+1), (-1,+1), (-1,+0)]
    out = 0

    # Iterate through rows...
    for i,input in enumerate(inputs):

        # Iterate through columns...
        for j,ch in enumerate(input):

            # If we've found ourselves a '*' symbol
            if (ch == '*'):
                
                # For this instance of '*' make a list of the nearby nums and a set of visited indices (to avoid duplicates)
                nearbyNums = []
                visited = set()

                # For each neighboring direction...
                for dir in dirs:

                    # If we haven't visited this neighbor yet, this neighbor is a valid index, and this neighbor is a digit, get its number
                    neigh = (i+dir[0], j+dir[1])
                    if (neigh not in visited and 0<=neigh[0]<m and 0<=neigh[1]<n and inputs[neigh[0]][neigh[1]].isdigit()):
                        visited.add(neigh)
                        num = __getNum(inputs, neigh, visited)
                        nearbyNums.append(num)

                # If, for this instance of '*', we have exactly two neighboring numbers, add to our output
                if len(nearbyNums) == 2:
                    out += nearbyNums[0] * nearbyNums[1]

    return out

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