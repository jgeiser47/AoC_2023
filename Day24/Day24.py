'''
    What: Advent of Code 2023 - Day 24
    Who: Josh Geiser
'''

from pathlib import Path
from scipy.optimize import fsolve 
import numpy as np

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_inputs(inputs):
    '''
    Helper function for parts 1 and 2 - parse inputs into position and velocity lists
    '''

    # List of position lists and list of velocity lists
    poss = []
    vels = []

    # Iterate through each hailstone, adding it's pos/vel to corresponding list
    for input in inputs:
        pos, vel = input.split(' @ ')
        pos = [int(x) for x in pos.split(', ')]
        vel = [int(x) for x in vel.split(', ')]
        poss.append(pos)
        vels.append(vel)

    return poss, vels

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __more_parsing(poss, vels):
    '''
    Helper function for part 1 - get a list of 5-tuples (a,b,c,d,e) of coefficients
    describing the trajectory of each hailstone over time
    '''

    # Output "coeffs" is a list of 5-tuples (a,b,c,d,e) of coefficients describing
    # the trajectory of each hailstone
    coeffs = []

    # Iterate through each hailstone, grabbing it's position and velocity
    for i in range(len(poss)):
        pos = poss[i]
        vel = vels[i]

        # Renaming for slope numerator, slope denominator, x0 position, and y0 position
        m_num = vel[1]
        m_den = vel[0]
        x0 = pos[0]
        y0 = pos[1]

        # Equation for our line y = f(x) ---------------> ax + by + c = 0
        a = m_num
        b = m_den * -1
        c = (m_num * -1 * x0) + (m_den * y0)

        # Equation for our point on line t = f(x) ------> x = dt + e
        d = vel[0]
        e = pos[0]

        # Add 5-tuple to output list
        coeffs.append((a,b,c,d,e))

    return coeffs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_collisions(coeffs):
    '''
    Helper function for part 1 - iterate though each combination of hailstones
    while summing up the total number of collisions
    '''

    # If we're using the actual input, our boxes are quite big (otherwise test input)
    if len(coeffs) > 10:
        box_min = 200000000000000
        box_max = 400000000000000
    else:
        box_min = 7
        box_max = 27

    # Iterate through each combination of hailstones
    num_out = 0
    for i in range(len(coeffs)-1):
        for j in range(i+1, len(coeffs)):

            # If this combination of hailstones leads to a collision, increment
            collision = __get_collision(coeffs[i], coeffs[j], box_min=box_min, box_max=box_max)
            if collision:
                num_out += 1

    return num_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __get_collision(vec1, vec2, box_min=200000000000000, box_max=400000000000000):
    '''
    Helper function for part 1 - determine if we have a future collision between
    two given hailstones. Inputs vec1 and vec2 are 5-tuples of coefficients that
    characterize the hailstone's movement over time. 
    '''

    # Unpack vectors (that are actually 5-tuples)
    a1, b1, c1, d1, e1 = vec1
    a2, b2, c2, d2, e2 = vec2

    # If parallel lines, return False immediately to protect from division by 0
    if (a1*b2 - a2*b1) == 0:
        return False

    # If not parallel, then find the intersection point (x_col, y_col)
    x_col = (b1*c2 - b2*c1) / (a1*b2 - a2*b1)
    y_col = (a2*c1 - a1*c2) / (a1*b2 - a2*b1)

    # Also find the times t1 and t2 that each hailstone reaches this collision point
    t1 = (x_col - e1) / d1
    t2 = (x_col - e2) / d2

    # If collision point is within bounds of box and both times are in the future, return true!
    if (box_min <= x_col <= box_max) and (box_min <= y_col <= box_max) and (t1 >= 0) and (t2 >= 0):
        return True
    else:
        return False

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - get coefficients describing each hailstone's path over 
    time and then check each pair of hailstones for collisions, summing up number
    of collisions as we go
    '''
    poss, vels = __parse_inputs(inputs)
    coeffs = __more_parsing(poss, vels)
    num_out = __get_collisions(coeffs)
    return num_out

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __f(x, poss, vels):
    '''
    Solver function for part 2

    Let's say our rock has position and velocity p0 and v0, and each hailstone has 
    pos/vel p[i] and v[i].

    We then can say:
        ->  p0 + t[i]*v0 == p[i] + t[i]*v[i]
        ->  (p0 - p[i]) == -t[i] * (v[0] - v[i])

    Since t[i] is a scalar, we know that the two above vectors are parallel, thus 
    the cross-product between them is 0:
        -> (p0 - p[i]) x (v0 - v[i]) == 0
        -> (p0 x v0) - (p[i] x v0) - (p0 x v[i]) + (p[i] x v[i]) == 0
        -> (p0 x v0) == (p[i] x v0) + (p0 x v[i]) - (p[i] x v[i])

    The (p0 x v0) term is common to every hailstone, so we can use that to equate
    two different pairs of indices. I'll change my notation now to use i,j,k to
    refer to 3 different hailstones:
        -> (p[i] x v0) + (p0 x v[i]) - (p[i] x v[i]) == (p[j] x v0) + (p0 x v[j]) - (p[j] x v[j])
        -> p0 x (v[i] - v[j]) + v0 x (p[j] - p[i]) == (p[i] x v[i]) - (p[j] x v[j])

    The above represents 3 constraint equations. We can do the same between i,k to
    get our other 3 constraint equations. We therefore have 6 variables given by
    our vectors p0 and v0, and 6 equations given by:
        -> p0 x (v[i] - v[j]) + v0 x (p[j] - p[i]) - ((p[i] x v[i]) - (p[j] x v[j]))
        -> p0 x (v[i] - v[k]) + v0 x (p[k] - p[i]) - ((p[i] x v[i]) - (p[k] x v[k]))

    We could simplify this down some more and do a matrix inversion to solve, but
    just throwing this into a nonlinear solver at this point is much easier... :)
    '''

    # Rename our x vector (free variables) into p0 and v0 of our rock
    p0 = np.array([x[0], x[1], x[2]])
    v0 = np.array([x[3], x[4], x[5]])

    # Positions/velocities of our chosen 3 hailstones
    p1 = np.array(poss[0])
    v1 = np.array(vels[0])
    p2 = np.array(poss[1])
    v2 = np.array(vels[1])
    p3 = np.array(poss[2])
    v3 = np.array(vels[2])

    # Some fancy math to get our constraints
    eq1 = (np.cross(p0, v1-v2) + np.cross(v0, p2-p1)) - (np.cross(p1,v1) - np.cross(p2,v2))
    eq2 = (np.cross(p0, v1-v3) + np.cross(v0, p3-p1)) - (np.cross(p1,v1) - np.cross(p3,v3))

    # Repackage our constraints before returning
    return [eq1[0], eq1[1], eq1[2], eq2[0], eq2[1], eq2[2]]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - I tried unsuccessfully for awhile at deriving my own
    system of equations to plug into a solver before finally turning to the AoC
    reddit page for inspiration. Thanks to "evouga" from the AoC 2023 reddit page 
    for the methodology I use here.
    '''

    # Only need to get positions/velocities of 3 hailstones - we'll just pick the first 3
    poss, vels = __parse_inputs(inputs)
    poss = poss[0:3]
    vels = vels[0:3]

    # Use our root solver to find our position/velocity of our rock
    x0 = [1,1,1,1,1,1]
    root = fsolve(__f, x0, args=(poss, vels), xtol=1e-14)

    # Since we've got big numbers, do some rounding to make sure we have exact integer
    # values before calculating and returning our answer
    rounded_pos_vel = [int(round(x)) for x in list(root)]
    out = sum(rounded_pos_vel[0:3])
    return out
    
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
