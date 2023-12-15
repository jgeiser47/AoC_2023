'''
    What: Advent of Code 2023 - Day 6
    Who: Josh Geiser
'''

from pathlib import Path
from math import floor

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_input(inputs):
    times = [int(x) for x in inputs[0].split(':')[1].split(' ') if len(x) > 0]
    distances = [int(x) for x in inputs[1].split(':')[1].split(' ') if len(x) > 0]
    return times, distances

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __f(hold_time, time):
    moving_time = time - hold_time
    return moving_time * hold_time

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):

    # Parse input into two arrays
    times, distances = __parse_input(inputs)

    # Iterate through each time/distance pair
    out = 1
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]

        # Calculate all of the potential distances we can go for different hold times
        distances_out = []
        for j in range(1,time):
            distances_out.append(__f(j, time))
        
        # Calculate number of those distances that beat the record and update output
        numWays = len([x for x in distances_out if x > distance])
        out *= numWays

    return out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_input_2(inputs):
    time = int(inputs[0].split(':')[1].strip().replace(' ', ''))
    distance = int(inputs[1].split(':')[1].strip().replace(' ', ''))
    return time, distance

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __binary_search_lower(start_range, end_range, total_time, distance_to_beat):

    # Keep iterating until our start_range and end_range are right next to eachother
    while ((end_range - start_range) > 1):

        # Calculate how far we go
        hold_time = floor((end_range + start_range) / 2)
        distance = __f(hold_time, total_time)

        # Adjust the endpoints of our binary search accordingly based on if we're 
        # looking for a lower or upper bound
        if (distance > distance_to_beat):
            end_range = hold_time
        else:
            start_range = hold_time

    # Return the last value that still beats the distance_to_beat
    return end_range

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __binary_search_upper(start_range, end_range, total_time, distance_to_beat):

    # Keep iterating until our start_range and end_range are right next to eachother
    while ((end_range - start_range) > 1):

        # Calculate how far we go
        hold_time = floor((end_range + start_range) / 2)
        distance = __f(hold_time, total_time)

        # Adjust the endpoints of our binary search accordingly based on if we're 
        # looking for a lower or upper bound
        if (distance > distance_to_beat):
            start_range = hold_time
        else:
            end_range = hold_time

    # Return the last value that still beats the distance_to_beat
    return start_range

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    
    # Parse input to extract our total time and distance to beat
    total_time, distance_to_beat = __parse_input_2(inputs)

    # Use binary search to find endpoints of just beating the record (could also just do this once but meh...)
    lower_edge = __binary_search_lower(1, floor(total_time/2), total_time, distance_to_beat)
    upper_edge = __binary_search_upper(floor(total_time/2)+1, total_time, total_time, distance_to_beat)
    
    # Return the range
    return upper_edge - lower_edge + 1

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
