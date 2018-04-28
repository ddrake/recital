# Recital
Generate possible programs for a dance recital.  The input consists of a set of dance sequences, each composed of one or more dances.  A dance has a set of dancers and optionally a title.  A sample input file "sequences.txt" is included in this repository"

By default, a valid program for a recital consists of a sequence (list) of dance sequences which are arranged so that the order of dances in each specified sequence is preserved, but so that no dancer appears in two consecutive dances except possibly within one of the input sequences (i.e. no 'overlaps')

It is possible to weaken the definition of a valid program by specifying a maximum number of overlaps.  This is specified by setting the command line argument -n.  For example -n=1 allows one overlap.

A dance sequence can also be assigned a specific order within the program.  For example, we may want to start or end the program with a particular sequence.  This can be done by prefacing the dance sequence by a number followed by a pipe character "|" in the input file as shown in sequences.txt.

Any generated programs are printed out and written to the file output.txt.

