#! /usr/bin/python3
import random
import sys
import argparse

#-------------------
# Class Definitions
#-------------------
class Dance:
    def __init__(self, dancers, title="Untitled"):
        self.dancers = dancers # a set of dancer names
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
        return "Program:\n"+"\n".join([str(d) for d in self.dances()])+"\n"

    def can_add_seq(self, seq):
        global max_overlaps
        return self.isect_ct(seq) + self.overlaps <= max_overlaps

    def add_seq(self, seq):
        global max_overlaps
        if self.can_add_seq(seq):
            self.overlaps += self.isect_ct(seq)
            self.dance_seqs.append(seq)
            assert self.overlaps <= max_overlaps, "too many overlaps"
        else:
            raise ArgumentError("Can't add sequence to program")

    def isect_ct(self, seq):
        return 0 if not self.dance_seqs else self.dance_seqs[-1].isect_ct(seq)

    def dances(self):
        return [dance for seq in self.dance_seqs for dance in seq.dances]

    def respects_ordering(self):
        return all(not seq.order or seq.order == self.dance_seqs.index(seq)+1 for seq in self.dance_seqs)

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
def make_test_data():
    dancers = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
    dances = []
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:3]),"Dance 1"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:5]),"Dance 2"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:2]),"Dance 3"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:4]),"Dance 4"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:7]),"Dance 5"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:3]),"Dance 6"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:1]),"Dance 7"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:5]),"Dance 8"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:6]),"Dance 9"))
    random.shuffle(dancers)
    dances.append(Dance(set(dancers[:5]),"Dance 10"))

    seqs = []
    seqs.append(DanceSequence([dances[0],dances[1],dances[2]]))
    seqs.append(DanceSequence([dances[3],dances[4]]))
    for i in range(5,len(dances)):
        seqs.append(DanceSequence([dances[i]]))

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
    return Dance(set(dancers.strip().split()), title)


#--------------------------------
# Command line argument parsing
#--------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description='Compute possible programs for a recital.')
    parser.add_argument('-f', help='sequence file path')
    parser.add_argument('-n', type=int, default=0, help='number of allowed overlaps')
    parser.add_argument('-a', action='store_true', \
        help="show all programs, even those which don't satisfy ordering")
    ns = parser.parse_args(sys.argv[1:])
    return ns.a, ns.f, ns.n


#-------------------
# Output Generation
#-------------------
def output(programs, seqs, include_all):
    output = ""
    for s in seqs:
        output += "{0}\n".format(s)

    results = [p for p in programs if p.respects_ordering()]
    output += "\n{0:d} program(s) found.\n".format(len(results))
    for p in results:
        output += "{}\n".format(p)
    if include_all:
        extras = [p for p in programs if not p.respects_ordering()]
        output += "\n{0:d} additional program(s) if required order of some sequences may change.\n" \
                .format(len(extras))
        for p in extras:
            output += "{}\n".format(p)

    print(output)
    with open('output.txt','w') as f:
        f.write(output)

#--------------
# Main Program
#--------------
include_all, infile, max_overlaps = parse_args()
print("max_overlaps: ", max_overlaps)
if infile:
    with open(infile,'r') as f:
        contents = f.read()
    seqs = parse_contents(contents)
else:
    seqs = make_test_data()

for s in seqs:
    print(s)

programs = solve(Program(),seqs)
output(programs, seqs, include_all)

