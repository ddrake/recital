import sys
sys.path.append('../')
from dance import *

# if we have 4 single dance sequences, each with one unique dancer
# we'd better get 24 solutions
def test_fully_disjoint_case():
    dancers = list("abcd")
    dances = [Dance([d]) for d in dancers]
    danceSeqs = [DanceSequence([d]) for d in dances]
    ps = solve(Program(),danceSeqs)
    assert len(ps) == 24

def test_simple_ordered_case():
    dancers = list("abcdef")
    dances = [Dance(dancers[i:i+2]) for i in range(5)]
    danceSeqs = [DanceSequence([d]) for d in dances]
    danceSeqs[0].order = 1
    danceSeqs[3].order = 5
    ps = solve(Program(),danceSeqs)
    assert len(ps) == 1
    p = ps[0]
    assert p.dance_seqs[0].dances[0].dancers == set(['a','b'])
    assert p.dance_seqs[1].dances[0].dancers == set(['c','d'])
    assert p.dance_seqs[2].dances[0].dancers == set(['e','f'])
    assert p.dance_seqs[3].dances[0].dancers == set(['b','c'])
    assert p.dance_seqs[4].dances[0].dancers == set(['d','e'])
    assert Program.max_overlaps == 0

def test_simple_overlap_case():
    dancers = list("abcde")
    dances = [Dance(dancers[i:i+2]) for i in range(4)]
    danceSeqs = [DanceSequence([d]) for d in dances]
    Program.max_overlaps = 0
    ps = solve(Program(),danceSeqs)
    # should be two solutions: bc de ab cd and the reverse
    assert len(ps) == 2
    Program.max_overlaps = 1
    ps = solve(Program(),danceSeqs)
    # should be two solutions with no overlap
    # plus 10 more solutions with one overlap, e.g. (ab cd de bc)
    assert len(ps) == 12
    Program.max_overlaps = 2
    ps = solve(Program(),danceSeqs)
    # should get all permutations except ab bc cd de and the reverse
    assert len(ps) == 22
    Program.max_overlaps = 3
    ps = solve(Program(),danceSeqs)
    # should get all 24 permutations
    assert len(ps) == 24

def test_overlap_with_order_case():
    dancers = list("abcde")
    dances = [Dance(dancers[i:i+2]) for i in range(4)]
    danceSeqs = [DanceSequence([d]) for d in dances]
    danceSeqs[0].order = 1
    danceSeqs[3].order = 4
    Program.max_overlaps = 1
    ps = solve(Program(),danceSeqs)
    # should be one solution: ab cd bc de
    assert len(ps) == 1
 
def test_intermission_affect_on_overlap():
    dancers = list("abcde")
    dances = [Dance(dancers[i:i+2]) for i in range(4)]
    danceSeqs = [DanceSequence([d]) for d in dances]
    danceSeqs.insert(2, DanceSequence([Dance([])]))
    Program.max_overlaps = 0
    ps = solve(Program(),danceSeqs)
    # with the intermission, we get 20 solutions instead of 2!
    assert len(ps) == 20

