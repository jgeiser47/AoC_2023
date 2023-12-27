'''
    What: Advent of Code 2023 - Day 20
    Who: Josh Geiser
'''

from pathlib import Path
from queue import Queue
import math

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(infile):
    with open(infile, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class broadcaster():
    '''
    Helper class for the broadcaster module
    '''
    def __init__(self):
        self.to_send = 'low'    # broadcaster always sends "low" pulse

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class flip():
    '''
    Helper class for the flip-flop module
    '''
    def __init__(self):
        self.on = False         # Flip-flop can be "off" or "on"
        self.to_send = 'low'    # Flip-flop can send "low" or "high" pulse

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def process(self, from_node:str, pulse:str):
        '''
        Flip-flops do nothing if they receive a high pulse. If low pulse and off,
        turn on and send high pulse. If low pulse and on, send low  and turn off.
        '''
        if pulse == 'high':
            return False
        elif pulse == 'low' and not self.on:
            self.on = True
            self.to_send = 'high'
        elif pulse == 'low' and self.on:
            self.on = False
            self.to_send = 'low'

        return True

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class conj():
    '''
    Helper class for the conjunction module
    '''
    def __init__(self):
        self.ins = {}           # Conjunction module must keep track of its inputs
        self.to_send = 'low'    # Conjunction can send "low" or "high" pulse

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def process(self, from_node:str, pulse:str):
        '''
        If all modules last sent a high pulse, send a low pulse. Otherwise, send 
        a high pulse.
        '''
        self.ins[from_node] = pulse
        if all([v == 'high' for v in self.ins.values()]):
            self.to_send = 'low'
        else:
            self.to_send = 'high'

        return True

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __parse_inputs(inputs):
    '''
    Helper function for parts 1 and 2 - parse our input file into two helpful 
    hashmaps. "obj" will contain a mapping of string names to instances of that
    object. "commands" will contain a mapping of input string module names to 
    output string module names.
    '''

    # Variables we will output
    obj = {}
    commands = {}

    # Iterate through each line, parsing it into its input and output(s)
    for line in inputs:
        ins, outs = line.split(' -> ')
        outs = outs.split(', ')

        # For the input, add an object of the specified type to our "obj" hashmap
        if ins == 'broadcaster':
            obj[ins] = broadcaster()
        elif ins[0] == '%':
            obj[ins[1:]] = flip()
        else:
            obj[ins[1:]] = conj()

        # Now add a mapping of (inputs -> outputs) to our "commands" hashmap
        ins = ins.replace('%', '').replace('&', '')
        commands[ins] = outs

    # Now we need to do a second pass to make sure all the conjunction modules
    # know where they'll be receiving signals from
    for line in inputs:
        ins, outs = line.split(' -> ')
        ins = ins.replace('%', '').replace('&', '')
        outs = outs.split(', ')

        # By default, set each last received input to "low"
        for out in outs:
            if out in obj and type(obj[out]) == conj:
                obj[out].ins[ins] = 'low'
        
    return obj, commands

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def __sim_single(obj, commands, click=None, final_feeders:dict=None):
    '''
    Helper function for parts 1 and 2 - simulate a single button press and all the
    pulses that will be sent from it. Function also includes two kwargs (used in
    part 2) for determining what button press number we're on and when the final
    "feeder" conjunction modules send high pulses. 
    '''

    # We automatically send one low pulse to the broadcaster on each button press
    num_low = 1
    num_high = 0

    # Start our queue with a low pulse sent to the broadcaster
    q = Queue()
    q.put('broadcaster')

    # Iterate until queue is empty (i.e., "all pulses delivered")
    while q.qsize() > 0:

        # Get our current module, type of pulse ("low" or "high") it'll send,
        # and that module's output modules
        curr = q.get()
        pulse = obj[curr].to_send
        outs = commands[curr]

        # For each output module...
        for out in outs:

            # ONLY for part 2 - if we notice a high pulse coming from one of 
            # our "final_feeder" conjunction modules that feeds our output,
            # note what button click number this occured on
            if click and pulse == 'high' and curr in final_feeders.keys():
                if final_feeders[curr] is None:
                    final_feeders[curr] = click

            # Update low/high pulse counts accordingly
            if pulse == 'low':
                num_low += 1
            else:
                num_high += 1

            # If the output module in question is also an input module and we have 
            # another pulse to send, add to queue
            if out in obj:
                add_to_q = obj[out].process(curr, pulse)
                if add_to_q:
                    q.put(out)

    # Return counts
    return (num_low, num_high)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_1(inputs):
    '''
    Task 1 main method - just simulate results using helpful OO programming. 
    '''

    # Get some helpful hashmaps
    obj, commands = __parse_inputs(inputs)

    # Number of low and high pulses that are sent
    num_low_total = 0
    num_high_total = 0

    # Simulate 1000 button presses!
    for i in range(1000):
        num_low, num_high = __sim_single(obj, commands)
        num_low_total += num_low
        num_high_total += num_high

    # Calculate and return our output
    return num_low_total * num_high_total

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def task_2(inputs):
    '''
    Task 2 main method - Simulation takes too long to brute force, so we must find
    another way. There are basically 4 different "branches" of our dependency tree,
    each with its own end conjunction module "final_feeder". The final module gets
    a low pulse when all 4 of the final feeders simultaneously send high pulses. 
    Rather than simulating to this point, we can just simulate the number of clicks
    required for each to send a high pulse, and then take the least-common-multiple
    (LCM) of those 4 numbers. 
    '''

    # Task 2 doesn't exist for the small sample input, so just return if we're 
    # not doing the real deal
    if len(inputs) < 50:
        return

    # Get our helpful hashmaps again
    obj, commands = __parse_inputs(inputs)

    # We have one final conjunction module ("rx" in my case). That final module
    # is fed by one "penultimate" conjunction module. That penultimate module is
    # fed by 4 "final feeder" conjunction modules that we care about.
    final = 'rx'
    penultimate = [k for k,v in commands.items() if final in v][0]
    final_feeders = {k:None for k,v in commands.items() if penultimate in v}

    # Just simulate for a long time...
    for click in range(1, 10000):
        out = __sim_single(obj, commands, click=click, final_feeders=final_feeders)

        # If we've seen all of our "final feeder" conjunction modules send at 
        # least one "high" pulse, then yay, we're done! We simply just need to 
        # return the LCM of the button press numbers required for each.  
        if all({v is not None for v in final_feeders.values()}):
            return math.prod(final_feeders.values())

    # Hopefully we don't get here...
    raise SystemError()
    
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
