# Recital

## Generate optimal programs for a dance recital

### Description  
The input consists of a set of dance sequences, each composed of one or more dances.  A dance has a set of dancers and optionally a title.  A sample input file "sequences.txt" is included in this repository.  Any generated programs are printed out and written to the file output.txt.

By default, a 'valid program' for a recital consists of a list of dance sequences which are arranged so that the order of dances in each specified sequence is preserved, but so that no dancer appears in two consecutive dances (i.e. no 'overlaps'), except possibly within one of the given input sequences.  The goal is to give dancers a chance to rest between numbers.

To handle overconstrained problems, it is possible to weaken the definition of a valid program by setting a maximum number of overlaps.  This is specified by setting the command line argument -n.  For example, -n=1 allows one overlap.

A dance sequence may also be assigned a specific order within the program.  For example, we may want to start or end the program with a particular sequence.  This can be done by prefacing the dance sequence by a number followed by a pipe character "|" in the input file (see sequences.txt for an example).  If the command line flag -a is set, any programs satisfying all constraints are printed first, then additionally, programs which satisfy all but these special ordering constraints are listed.

To test the algorithm with some randomly generated inputs, just run the program without specifying an input file.

```
usage: dance.py [-h] [-f F] [-n N] [-a]

Compute possible programs for a recital.

optional arguments:
  -h, --help  show this help message and exit
  -f F        Sequence file path. If no file is set, random data will be used.
  -n N        Number of allowed overlaps
  -a          After listing programs, show programs which are valid except for
              ordering
```
### Installation
git clone git@github.com:ddrake/recital.git 

### Examples 

#### Test with random data
cd recital

./dance.py

#### Test with sample input file
cd recital

./dance.py -f sequences.txt -n1

