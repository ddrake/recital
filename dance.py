#! /usr/bin/python3
import random
import sys
import argparse

#-------------------
# Class Definitions
#-------------------
class Dance:
    def __init__(self, dancers, title="Untitled"):
        self.dancers = set(dancers) # dancers' names
        self.title = title

    def __str__(self):
        return "{}: {}".format(self.title, str(self.dancers))

class DanceSequence:
    def __init__(self, dances=None, order=None):
        if not dances:
            raise ValueError("Each sequence must contain at least one dance")
        
        self.dances = dances
        self.order = int(order) if order else None

    def __str__(self):
        order_str = "{0:d} | ".format(self.order) if self.order else ""
        return order_str + ", ".join([str(dance) for dance in self.dances])

    def isect_ct(self, sequence):
        return len(self.dances[-1].dancers.intersection(sequence.dances[0].dancers))

class Program:
    def __init__(self, dance_seqs = []):
        self.dance_seqs = []
        self.overlaps = 0
        for s in dance_seqs:
            self.add_seq(s)

    def __str__(self):
        return "Program {0:d}:\n".format(self.number) + \
                "\n".join([str(d) for d in self.dances()])+"\n"

    def set_number(self, number):
        self.number = number

    def can_add_seq(self, seq):
        global max_overlaps
        return self.isect_ct(seq) + self.overlaps <= max_overlaps

    def add_seq(self, seq):
        global max_overlaps
        if self.can_add_seq(seq):
            self.overlaps += self.isect_ct(seq)
            self.dance_seqs.append(seq)
        else:
            raise ArgumentError("Can't add sequence to program -- too many overlaps.")

    def isect_ct(self, seq):
        return 0 if not self.dance_seqs else self.dance_seqs[-1].isect_ct(seq)

    def dances(self):
        return [dance for seq in self.dance_seqs for dance in seq.dances]

    def respects_ordering(self):
        return all(not seq.order or seq.order == self.dance_seqs.index(seq)+1 \
                for seq in self.dance_seqs)

#--------
# Solver
#--------
# Generate a list of all possible programs by taking a partially 
# complete Program and a list of dance sequences that must to be added.
# If the current Program is complete, return it in a list.
# Otherwise call solve() recursively for any valid Programs
# formed by appending one of the seqs to a copy of the current Program
def solve(cur_prog, seqs):
    programs = []
    if not seqs:
        return [cur_prog]
    for s in seqs:
        if cur_prog.can_add_seq(s):
            new_prog = Program(cur_prog.dance_seqs[:])
            assert new_prog.overlaps == cur_prog.overlaps, "overlaps changed"
            new_prog.add_seq(s)
            rest = seqs[:]
            rest.remove(s)
            programs += solve(new_prog,rest)
    return programs

#--------------------
# Generate Test Data
#--------------------
def make_dance(dancers,ct,n):
    random.shuffle(dancers)
    return Dance(dancers[:ct], "Dance {0:d}".format(n))

def make_dance_seq(dancers, cts, start_num, order=None):
    dances = []
    dancerset = set()
    for i in range(len(cts)):
        distinct = False
        while not distinct:
            dance = make_dance(dancers, cts[i], start_num + i)
            if dancerset.isdisjoint(dance.dancers):
                dancerset = dancerset.union(dance.dancers)
                distinct = True
        dances.append(dance)
    return DanceSequence(dances, order=order)

def make_test_data():
    dancers = list("abcdefghigklmnopqr")
    seqs = []
    seqs.append(make_dance_seq(dancers, [3,5,2], 1, order=1))
    seqs.append(make_dance_seq(dancers, [4,7], 4, order=10))
    for i in range(8):
        seqs.append(make_dance_seq(dancers,[4],i+6))
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
    else: raise Exception("Can't parse dance sequence")
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
    else: raise Exception("Can't parse dance")
    return Dance(dancers.strip().split(), title)

#--------------------------------
# Command line argument parsing
#--------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description='Compute possible programs for a recital.')
    parser.add_argument('-f', help='Sequence file path.  If no file is set, random data will be used.')
    parser.add_argument('-n', type=int, default=0, help='Number of allowed overlaps')
    parser.add_argument('-a', action='store_true', \
            help="After listing programs, show programs which are valid except for ordering")
    ns = parser.parse_args(sys.argv[1:])
    return ns.a, ns.f, ns.n

#-------------------
# Output Generation
#-------------------
def output(programs, seqs, include_all, max_overlaps):
    output = "Maximum allowed overlaps: {0:d}\n".format(max_overlaps)
    output += "Input Sequences \n"
    for s in seqs:
        output += "{0}\n".format(s)

    results = [p for p in programs if p.respects_ordering()]
    output += "\n{0:d} program(s) found.\n".format(len(results))
    for i, p in enumerate(results):
        p.set_number(i+1)
        output += "{}\n".format(p)
    if include_all:
        extras = [p for p in programs if not p.respects_ordering()]
        output += "\n{0:d} additional program(s) if required order of some sequences may change.\n" \
                .format(len(extras))
        for i, p in enumerate(extras):
            p.set_number(i+1)
            output += "{}\n".format(p)

    print(output)
    with open('output.txt','w') as f:
        f.write(output)

#--------------
# Main Program
#--------------
include_all, infile, max_overlaps = parse_args()
if infile:
    with open(infile,'r') as f:
        contents = f.read()
    seqs = parse_contents(contents)
else:
    seqs = make_test_data()

programs = solve(Program(),seqs)
output(programs, seqs, include_all, max_overlaps)

