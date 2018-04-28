# Recital

## Generate optimal programs for a dance recital

### Usage  
The input consists of a set of dance sequences, each composed of one or more dances.  A dance has a set of dancers and optionally a title.  A sample input file "sequences.txt" is included in this repository.  Any generated programs are printed out and written to the file output.txt.

By default, a 'valid program' for a recital consists of a sequence (list) of dance sequences which are arranged so that the order of dances in each specified sequence is preserved, but so that no dancer appears in two consecutive dances (i.e. no 'overlaps'), except possibly within one of the given input sequences.  The goal is to give dancers a chance to rest between numbers.

To handle overconstrained problems, it is possible to weaken the definition of a valid program by setting a maximum number of overlaps.  This is specified by setting the command line argument -n.  For example, -n=1 allows one overlap.

A dance sequence may also be assigned a specific order within the program.  For example, we may want to start or end the program with a particular sequence.  This can be done by prefacing the dance sequence by a number followed by a pipe character "|" in the input file (see sequences.txt for an example).  If the command line flag -a is set, any programs satisfying all constraints are printed first, then additionally, programs which satisfy all but these ordering constraints are listed.

