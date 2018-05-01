#! /usr/bin/python3
import random
import sys
import argparse

#-------------------
# Class Definitions
#-------------------
class Dance:
    def __init__(self, dancers, title='Untitled'):
        self.dancers = set(dancers) # dancers' names
        self.title = title

    def __str__(self):
        return '{}: {}'.format(self.title, str(self.dancers))

    def pretty(self):
        return '{}: {}'.format(self.title, ', ' \
                .join(sorted(list(self.dancers))))

class DanceSequence:
    def __init__(self, dances=None, order=None, before=None, after=None):
        if not dances:
            raise ValueError('Each sequence must contain at least one dance')
        
        self.dances = dances
        self.order = int(order) if order else None
        self.before = int(before) if before else None
        self.after = int(after) if after else None

    def __str__(self):
        order_str = '{0:d} | '.format(self.order) if self.order else ''
        return order_str + ', '.join([str(dance) for dance in self.dances])

    def isect_ct(self, sequence):
        return len(self.dances[-1].dancers.intersection( \
            sequence.dances[0].dancers))

class Program:
    def __init__(self, dance_seqs = []):
        self.dance_seqs = []
        self.overlaps = 0
        self.number = 0
        for s in dance_seqs:
            self.add_seq(s)

    def __str__(self):
        return 'Program {0:d}:\n'.format(self.number) + \
                '\n'.join([str(d) for d in self.dances()])+'\n'

    def pretty(self):
        return 'Program {0:d}:\n'.format(self.number) + \
                '\n'.join([d.pretty() for d in self.dances()])+'\n'

    def set_number(self, number):
        self.number = number

    def can_add_seq(self, seq):
        print("in can add with self.isect_ct(seq)={0:d}, overlaps={1:d}, max={2:d}".format(self.isect_ct(seq), self.overlaps, Program.max_overlaps))
        return self.isect_ct(seq) + self.overlaps <= Program.max_overlaps

    def add_seq(self, seq):
        if self.can_add_seq(seq):
            self.overlaps += self.isect_ct(seq)
            self.dance_seqs.append(seq)
        else:
            raise ValueError("Can't add sequence to program " \
                    + "-- too many overlaps.")

    def isect_ct(self, seq):
        return 0 if not self.dance_seqs else self.dance_seqs[-1].isect_ct(seq)

    def dances(self):
        return [dance for seq in self.dance_seqs for dance in seq.dances]

    def allowed(seqs, position):
        if any(s.order == position for s in seqs):
            return [s for s in seqs if s.order == position]
        return [s for s in seqs if \
                (not s.order or s.order == position) and
                (not s.before or s.before > position) and 
                (not s.after or s.after < position)]

#--------
# Solver
#--------
# Generate a list of all possible programs by taking a partially 
# complete Program and a list of the remaining dance sequences to be added.
# If the current Program is complete (i.e. no more sequences to add), 
# return it wrapped in a list.
# Otherwise, call solve() recursively for any valid Programs
# formed by appending one of the sequences to a copy of the current Program,
# then merge these results into a list of programs and return this list.
def solve(cur_prog, seqs, level=1):
    programs = []
    position = len(cur_prog.dance_seqs) + 1
    if not seqs:
        return [cur_prog]
    allowed = Program.allowed(seqs, position)
    print("position is ", position, ", ", len(allowed), " allowed")
    for i, s in enumerate(allowed):
        if level == 1:
            print("Checking sequence {0:d}...".format(i+1))
        if cur_prog.can_add_seq(s):
            new_prog = Program(cur_prog.dance_seqs[:])
            new_prog.add_seq(s)
            rest = seqs[:]
            rest.remove(s)
            programs += solve(new_prog,rest, level=level+1)
    return programs

#--------------------
# Generate Test Data
#--------------------
def make_dance(dancers,ct,n):
    random.shuffle(dancers)
    return Dance(dancers[:ct], 'Dance {0:d}'.format(n))

def make_disjoint_dance_seq(dancers, cts, start_num, order=None):
    dances = []
    dancer_set = set()
    for i in range(len(cts)):
        disjoint = False
        while not disjoint:
            dance = make_dance(dancers, cts[i], start_num + i)
            if dancer_set.isdisjoint(dance.dancers):
                dancer_set = dancer_set.union(dance.dancers)
                disjoint = True
        dances.append(dance)
    return DanceSequence(dances, order=order)

def make_test_data():
    dancers = list('abcdefghigklmnopqr')
    seqs = []
    seqs.append(make_disjoint_dance_seq(dancers, [3,5,2], 1, order=1))
    seqs.append(make_disjoint_dance_seq(dancers, [4,7], 4, order=10))
    for i in range(8):
        seqs.append(make_disjoint_dance_seq(dancers,[4],i+6))
    return seqs

#-------------------
# Input file parsing
#-------------------
def parse_contents(contents):
    lines = contents.strip().split('\n')
    lines = [line for line in lines if line and line[0] != '#']
    seqs = []
    for line in lines:
        seq, order = parse_dance_sequence(line)
        seqs.append(DanceSequence(seq, order=order))
    return seqs

def parse_dance_sequence(line):
    seqinfo = line.strip().split('|')
    if len(seqinfo) == 2:
        order, dances = seqinfo
    elif len(seqinfo) == 1:
        order, dances = None, seqinfo[0]
    else: raise ValueError("Can't parse dance sequence")
    dances = dances.strip().split(';')
    seq = []
    for d in dances:
        seq.append(parse_dance(d))
    return seq, order

def parse_dance(d):
    dinfo = d.strip().split(':')
    if len(dinfo) == 2:
        title, dancers = dinfo
    elif len(dinfo) == 1:
        title, dancers = None, dinfo[0]
    else: raise ValueError("Can't parse dance")
    return Dance(dancers.strip().split(), title)

#--------------------------------
# Command line argument parsing
#--------------------------------
def parse_args():
    parser = argparse.ArgumentParser( \
            description='Compute possible programs for a recital.')
    parser.add_argument('-f', help='Sequence file path. ' \
            + 'If no file is set, random data will be used.')
    parser.add_argument('-n', type=int, default=0, 
            help='Number of allowed overlaps')
    ns = parser.parse_args(sys.argv[1:])
    return ns.f, ns.n

#-------------------
# Output Generation
#-------------------
def echo_inputs(seqs):
    output = 'maximum allowed overlaps: {0:d}\n'.format(Program.max_overlaps)
    output += 'input sequences \n'
    for s in seqs:
        output += '{0}\n'.format(s)
    print(output)

def output(programs, seqs):
    output = 'maximum allowed overlaps: {0:d}\n'.format(Program.max_overlaps)
    output += 'input sequences \n'
    for s in seqs:
        output += '{0}\n'.format(s)

    results = programs
    output += '\n{0:d} program(s) found.\n'.format(len(results))
    for i, p in enumerate(results):
        p.set_number(i+1)
        output += '{}\n'.format(p.pretty())
    print(output)
    with open('output.txt','w') as f:
        f.write(output)

# Set a default value
Program.max_overlaps = 0
#--------------
# Main Program
#--------------
if __name__ == '__main__':
    infile, max_overlaps = parse_args()
    if infile:
        with open(infile,'r') as f:
            contents = f.read()
        seqs = parse_contents(contents)
    else:
        seqs = make_test_data()

    Program.max_overlaps = max_overlaps
    echo_inputs(seqs)
    programs = solve(Program(),seqs)
    output(programs, seqs)

