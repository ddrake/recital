#! /usr/bin/python3
import random
import sys

class DanceSequence:
    def __init__(self, dances=None):
        if not dances:
            raise ValueError("Each sequence must contain at least one dance")
        
        self.dances = dances

    def __str__(self):
        return ", ".join([str(d) for d in self.dances])

    def isdisjoint(self, sequence):
        return self.dances[-1].isdisjoint(sequence.dances[0])

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
    dances.append(set(dancers[:3]))
    random.shuffle(dancers)
    dances.append(set(dancers[:5]))
    random.shuffle(dancers)
    dances.append(set(dancers[:2]))
    random.shuffle(dancers)
    dances.append(set(dancers[:4]))
    random.shuffle(dancers)
    dances.append(set(dancers[:7]))
    random.shuffle(dancers)
    dances.append(set(dancers[:3]))
    random.shuffle(dancers)
    dances.append(set(dancers[:1]))
    random.shuffle(dancers)
    dances.append(set(dancers[:5]))
    random.shuffle(dancers)
    dances.append(set(dancers[:6]))
    random.shuffle(dancers)
    dances.append(set(dancers[:5]))

    seqs = []
    seqs.append(DanceSequence([dances[0],dances[1],dances[2]]))
    seqs.append(DanceSequence([dances[3],dances[4]]))
    for i in range(5,len(dances)):
        seqs.append(DanceSequence([dances[i]]))

    for s in seqs:
        print(s)
    return seqs

if len(sys.argv) > 1:
    try:
        with open(sys.argv[1],'r') as f:
            contents = f.read()
    except Exception as ex:
        print(ex)
        sys.exit(2)

    try:
        lines = contents.strip().split('\n')
        lines = [line for line in lines if line and line[0] != '#']
        seqs = []
        for line in lines:
            tseqs = line.strip().split(';')
            seqs.append(DanceSequence([set(tseq.strip().split()) for tseq in tseqs if tseq]))
            #print([set(tseq.strip().split()) for tseq in tseqs])
    except Exception as ex:
        print(ex)
        sys.exit(2)
else:
    seqs = make_test_data()

for s in seqs:
    print(s)

programs = step([],seqs)
print(len(programs))
for p in programs:
    print(p)
