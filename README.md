## Bimaru Solver

### Description

Made for the Artificial Intelligence (IArt @ IST) class, this program solves puzzles of the popular game Bimaru.

The program should be given as input a bimaru puzzle, with the format similar to the ones in the "instances" or "Private" folders.

### How to run

If you want to run a single instance of a puzzle, you can do it as follows:

```
python3 bimaru.py > instances/instance01.txt
```

You can run an automatic script that will print all the puzzles of the 10 example instances in the "instances" folder, and
the individual times will be placed in the "PublicOutputs" folder:

```
python3 run_tests.py
```

Since this program was submitted in Mooshak, it was subjected to exaustive private tests.
They were given at the end of the course to the students, and they can be run as follows:

```
python3 tester.py
```

This will print how long the program took to solve each test in the "Private", in sequence. The outputs will be in the "TesterOutputs" folder.

### Strategy

* The program starts by doing all the pre-processing it can according to the hints and the rules of the game (iteratively checking if it can fill
a row or column with water, or placing water in the adjacent cells of a ship). 

* After that, it starts to solve the puzzle by using a ship-based approach and a list of actions, where it uses DFS and backtracking to place
ships, from bigger to smaller ones, into the puzzle, and constantly checking for more possible water placements or rows/columns that can be filled.


### Have fun!

This was a fun project to do, and I hope you have fun with it too! 

You can try giving it your own different puzzles, as long as they are valid and follow the format of the examples, and watch the program solve it.