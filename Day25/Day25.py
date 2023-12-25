'''
    What: Advent of Code 2023 - Day 25
    Who: Josh Geiser
'''

from pathlib import Path
from queue import Queue
import random

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_inputs(inputs):
    '''
    Helper function for part 1 - parse our inputs and return a set of all of our 
    names/nodes, as well as a hashmap "full" representing edges between nodes
    '''

    # Let's just do a first pass getting all of the names/nodes as a set
    names = set()
    for line in inputs:
        ins, outs = line.split(': ')
        outs = outs.split(' ')
        names.add(ins)
        for out in outs:
            names.add(out)

    # Do a second pass, getting our hashmap of edges between nodes
    full = {name:set() for name in names}
    for line in inputs:
        ins, outs = line.split(': ')
        outs = outs.split(' ')
        for out in outs:
            full[ins].add(out)
            full[out].add(ins)

    return names, full

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __BFS_random(full, start, end):
    '''
    Helper function for part 1 - perform BFS between random start and end nodes,
    and return a list of nodes representing the shortest path between the two
    '''

    # Other variables we'll use in BFS
    visited = set()
    q = Queue()

    # Add (random) start node to the queue
    q.put([start])
    visited.add(start)

    # BFS: Iterate until queue is empty
    while (not q.empty()):

        # Get neighbors of curr
        path_list = q.get()
        curr = path_list[-1]

        for neigh in full[curr]:

            # If we're at our (random) endpoint, return our path list
            if neigh == end:
                return path_list + [end]

            # Otherwise, if we haven't visited this neighbor yet, add to queue
            if neigh not in visited:
                q.put(path_list + [neigh])
                visited.add(neigh)
    
    raise SystemError()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __edge_helper(edge1, edge2):
    '''
    Helper function for part 1 - "sort" our edge alphabetically, and return as 
    a tuple of the two nodes that the edge is between
    '''
    return (edge1, edge2) if edge1 < edge2 else (edge2, edge1)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __add_path_to_count(edge_count, min_path):
    '''
    Helper function for part 1 - given a shortest path list of nodes (from earlier
    call to __BFS_random(), get all the edges traversed and add them to our sums)
    '''

    # Iterate through each edge traversed
    for i in range(len(min_path) - 1):
        edge = __edge_helper(min_path[i], min_path[i+1])

        # Add edge to "edge_count" total
        if edge in edge_count:
            edge_count[edge] += 1
        else:
            edge_count[edge] = 1

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __BFS_with_cut(full, cut_edges, start):
    '''
    Helper function for part 1 - perform a "modified" BFS with a list of "cut_edges"
    that may not be traversed. Return the length of the output graph - if this 
    length is shorter than the number of nodes in our original graph, then we know
    we've successfully split it in two!
    '''

    # Other variables we'll use in BFS
    visited = set()
    q = Queue()

    # Add (random) start node to the queue
    q.put(start)
    visited.add(start)

    # BFS: Iterate until queue is empty
    while (not q.empty()):

        # Get neighbors of curr
        curr = q.get()
        for neigh in full[curr]:

            # If this neighbor hasn't been visited AND also is not one of our "cut" edges
            if neigh not in visited and (curr, neigh) not in cut_edges and (neigh, curr) not in cut_edges:
                q.put(neigh)
                visited.add(neigh)
    
    # Return size of spanned graph 
    return len(visited)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - again, thanks to some others online for inspiration here.
    Main idea is to build our graph and perform a bunch of BFS searchs between
    random start/end nodes, saving off the number of times each edge is traversed.

    The correct 3 edges to "cut" are generally some of the most traversed edges, so
    then it's just a matter of trying a couple different combinations of these edges
    until we find the combo that does indeed split the graph in two.

    Note that since this algorithm uses randomness, it does not always properly 
    identify the correct 3 edges to cut (and will just return None), but more often
    than not it is successful. And if it's not, it doesn't take long to re-run :)
    '''

    # Parse our inputs into some more usable variables
    names, full = __parse_inputs(inputs)
    names_list = list(names)
    numNames = len(names)

    # Perform BFS with random start/end nodes some N number of times, totaling up
    # the number of times each edge is traversed
    edge_count = {}
    for i in range(100):
        start = random.choice(names_list)
        end = random.choice(names_list)
        min_path = __BFS_random(full, start, end)
        __add_path_to_count(edge_count, min_path)

    # Sort our edges based on which are used the most
    edges_to_cut = [(v, k) for k,v in edge_count.items()]
    edges_to_cut.sort(reverse=True)

    # From playing around for awhile, I found that the two most traversed edges
    # are nearly always 2/3 of the correct ones to "cut". The third one however 
    # isn't always traversed third most frequently. So we'll have to iterate 
    # through a couple potential combinations of edges (~20) to find the correct
    # combination of 3.
    for i in range(2, 20):
        cut_edges = {edges_to_cut[0][1], edges_to_cut[1][1], edges_to_cut[i][1]}

        # If we perform BFS with a combination of "cut" edges and the length of 
        # our output graph is less than total number of nodes, then yay we've 
        # split our graph into two!
        len_graph = __BFS_with_cut(full, cut_edges, start)
        if len_graph < numNames:
            return len_graph * (numNames - len_graph)

    return SystemError()
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

    infile = Path(__file__).parent / 'input.txt'

    inputs = read_input(infile)
    print(task_1(inputs))

    return

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main()
