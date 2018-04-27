#! /usr/bin/python3
import random
import sys
import argparse

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
        self.order = order

    def __str__(self):
        return ", ".join([str(dance) for dance in self.dances])

    def isdisjoint(self, sequence):
        return self.dances[-1].dancers.isdisjoint(sequence.dances[0].dancers)

# a program is a valid list of DanceSequences
class Program:
    def __init__(self, dance_seqs):
        for i in range(len(dance_seqs)-1):
            if not dance_seqs[i].isdisjoint(dance_seqs[i+1]):
                raise ValueError("Can't construct program - dancers must rest.")
        self.dance_seqs = dance_seqs
    
    def __str__(self):
        return "Program:\n"+"\n".join([str(d) for d in self.dances()])+"\n"

    def dances(self):
        return [dance for seq in self.dance_seqs for dance in seq.dances]

# Recursively generate a list of all possible programs from the given data
# take a list of dance sequences (a program in process) 
# and a list of dance sequences that need to be added
# try to append.
def step(cur_prog, seqs):
    programs = []
    if not seqs:
        return [Program(cur_prog)]
    for s in seqs:
        if not cur_prog or cur_prog[-1].isdisjoint(s):
            cp = cur_prog[:]
            cp.append(s)
            rest = seqs[:]
            rest.remove(s)
            programs += step(cp,rest)
    return programs

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

def parse_line(line):
    seqinfo = line.strip().split('|')
    if len(seqinfo) == 2:
        order, dances = seqinfo
    elif len(seqinfo) == 1:
        order, dances = None, seqinfo[0]
    else: raise Exception("Can't parse line")

# Program starts here
parser = argparse.ArgumentParser(description='Compute some possible programs for a recital.')
parser.add_argument('-f', help='sequence file path')
parser.add_argument('-n', type=int, default=0, help='number of allowed overlaps')
parser.add_argument('-a', action='store_true', \
        help="show all programs, even those which don't satisfy ordering")
ns = parser.parse_args(sys.argv)
include_all = ns.a
infile      = ns.f
overlaps    = ns.n

if infile:
    try:
        lines = contents.strip().split('\n')
        lines = [line for line in lines if line and line[0] != '#']
        seqs = []
        for line in lines:
            parse_line(line)
            order, dances = parse_line(line)
            dances = dances.strip().split(';')
            seq = []
            for d in dances:
                dinfo = d.strip().split(':')
                if len(dinfo) == 2:
                    title, dancers = dinfo
                elif len(dinfo) == 1:
                    title, dancers = None, dinfo[0]
                else: raise Exception("Can't parse dance")

                dance = Dance(set(dancers.strip().split()), title)
                seq.append(dance)

            seqs.append(DanceSequence(seq, order=order))

    except Exception as ex:
        print(ex)
        sys.exit(2)
else:
    seqs = make_test_data()

for s in seqs:
    print(s)

programs = step([],seqs)
print("\n{0:d} program(s) found.".format(len(programs)))
for p in programs:
    print(p)

