# Recital

## Generate optimal programs for a dance recital

### Description
In preparing for a recital, we assume that a number of dance pieces have been prepared so that each piece has a title and a fixed set of dancers.  In designing an optimal program (sequence of dance pieces) for a recital, we wish to eliminate or minimize "overlaps", i.e. scenarios in which one or more dancers must appear in consecutive sequences.

Some of the dance pieces may be logically grouped together in some order.  We call such a grouping a "dance sequence".  When designing a program, we wish to retain the internal order of each dance sequence, while considering rearrangements of the sequences within the program. 

It may be useful to apply special ordering constraints to the sequences.  For example, we may want to specify that one particular sequence must appear first in the program or that a sequence must appear after the fifth position.

The input to this application consists of a set of dance sequences, each composed of one or more dances.  A dance is modelled as a (possibly empty) set of dancers names and an optional title.  A dance with no dances may be considered an "intermission".  A sample input file "sequences.txt" is included in this repository and demonstrates the syntax for specifying dance sequences and special ordering constraints.  The program can be run in a terminal with a specified input file via
```
$ ./dance.py -f <input file path>
```
When the program is run, it first prints to the console a confirmation of the parsed input dance sequences followed by a list of programs (if any) that satisfy the overlap and ordering constraints.  For convenience, the program output is also written to the file output.txt.

When running the program, it's possible to specify a maximum number of allowed overlaps by setting the command line argument -n.  For example, -n=1 allows one overlap.

To set a dance sequence to specific order within the program, we preface its definition in the input file by a number followed by a pipe character "|".  For example, a line in the input file like this
```
1 | "A Dance": Joe Sue
```
specifies a dance sequence with a single dance which must appear first in the program.  The following example 
```
>3 <8 | "Fancy Dance": Mary Bob Sue; "Quick Dance": Joe Ann Sue Bill
```
specifies a dance sequence consisting of two dances, which must appear after the third sequence and before the eighth sequence.

To test the algorithm with some (partially) randomly generated input data, just run the program without specifying an input file.

A pytest test suite is also included in the repository in the folder 'tests'.  The tests can be run using
```
$ cd tests
$ pytest
```
You may need to install pytest first.

```
usage: dance.py [-h] [-f F] [-n N] [-a]

Compute possible programs for a recital.

optional arguments:
  -h, --help  show this help message and exit
  -f F        Sequence file path. If no file is set, random data will be used.
  -n N        Number of allowed overlaps
  -a          After listing programs, show programs which are valid except for
              special ordering
```
### Installation
```
$ git clone git@github.com:ddrake/recital.git 
```

### Examples 

#### Test with random data allowing one overlap
```
$ cd recital
$ ./dance.py -n=1
```

#### Test with sample input file allowing two overlaps
```
$ cd recital
$ ./dance.py -f sequences.txt -n=2
```
