'''
    What: Advent of Code 2023 - Day 5
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
def __get_val(seed, mappings):
    '''
    Helper function for task 1 - map a seed value to it's next value given mapping
    '''
    for mapping in mappings:
        if (mapping[1] <= seed < mapping[1]+mapping[2]):
            return mapping[0] + (seed - mapping[1])
        
    return seed

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):

    # Get the seeds and then skip to the first map
    seeds = [int(x) for x in inputs[0].split(': ')[1].split(' ')]
    inputs.append('')

    # Iterate through our file 'til we're done!
    i = 2
    while (i < len(inputs)):
        assert 'map' in inputs[i]

        # mapping = {}
        mappings = []

        # Increment lines of our input file until we've reached a blank line, meaning new "layer"
        i+=1
        while len(inputs[i]) > 0:
            line = inputs[i]

            # Add this row to our mapping dictionary
            mappings.append([int(x) for x in line.split(' ')])
            i+=1

        # Now map our seeds through the next "layer"
        seeds = [__get_val(seed, mappings) for seed in seeds]
        i+=1

    return min(seeds)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_val2(seed, mappings):
    '''
    Helper function for task 2: return a tuple where...
        first index is the output location of a seed
        second index is the "buffer" until you hit another discontinuity
    '''

    # If our current value is within one of the mapping ranges, return as soon as that's found
    for mapping in mappings:
        if (mapping[1] <= seed < mapping[1]+mapping[2]):
            return mapping[0] + (seed - mapping[1]), abs(mapping[2] - ((seed - mapping[1])))
        

    # If we've gotten this far, our return value is just our input value. However
    # we also need to calculate the "buffer" to the nearest mapping range.
    min_dist = 1e20
    for mapping in mappings:
        compare = mapping[1]
        if (compare - seed) > 0 and (compare - seed) < min_dist:
            min_dist = compare - seed

    return seed, min_dist

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __f(seed, total_map):
    '''
    Helper function for task 2: calculate y = f(x) where x = seed and y = location
    '''

    buffers = []
    for mappings in total_map:
        seed, buffer = __get_val2(seed, mappings)
        buffers.append(buffer)
        
    return seed, min(buffers)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_map(inputs):
    '''
    Helper function for task 2 for getting our mappings between locations
    '''

    total_map = []
    mappings = []

    # Iterate through our file 'til we're done!
    i = 2
    while (i < len(inputs)):
        assert 'map' in inputs[i]

        # mapping = {}
        mappings = []

        # Increment lines of our input file until we've reached a blank line, meaning new "layer"
        i+=1
        while len(inputs[i]) > 0:
            line = inputs[i]

            # Add this row to our mapping dictionary
            mappings.append([int(x) for x in line.split(' ')])
            i+=1

        # Now map our seeds through the next "layer"
        total_map.append(mappings)
        i+=1
    
    return total_map

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    General idea is that we can't (quickly) brute force looking through all the
    ranges of seed values. However, since we know that output locations will be 
    monotonically increasing for some range of input seeds, we can be smart about
    calling only inputs seeds that will be on the "boundaries" of changed behavior.
    '''

    # Get our total_map that'll be used to calculate location = f(seed) for each seed
    inputs.append('')
    total_map = __get_map(inputs)

    # Let's just make a 2d array of our starting/ending seed ranges to look through
    first_line = [int(x) for x in inputs[0].split(': ')[1].split(' ')]
    seed_ranges = [[first_line[i], first_line[i]+first_line[i+1]-1] for i in range(0, len(first_line), 2)]

    # Now iterate through each of the individual seed ranges
    visited_seeds = []
    visited_outs = []
    for seed_range in seed_ranges:

        # Starting/stopping seed values to potentially look through
        seed = seed_range[0]
        end_val = seed_range[1]

        # Keep looking through seed range while we're less than our end value
        while (seed <= end_val):
            out, out_buffer = __f(seed, total_map)
            visited_seeds.append(seed)
            visited_outs.append(out)
            seed += out_buffer

    # Finally, return the minimum of all of our output locations
    return min(visited_outs)

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
