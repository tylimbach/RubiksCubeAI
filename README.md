# Rubiks Cube

Rubiks Cube is a project that simulates a 3x3 rubik's cube written in Python. It supports multiple operations.

- Creation of a solved 3x3
- Perform turns or rotations
- Execution of random 25 move scrambles
- Display the cube state as a 2D unfolded cube in terminal (with colors)
- Solve the cube using the most popular speedsolving method for humans: CFOP

## Installation

Download or clone the repository.
Requires Python 3 (tested on Python 3.9).

Run from within the rubiks-cube folder.

```
python3 main.py
```

## 3x3 Notation
This project uses official rubik's cube notation to represent the cube, this is especially important to understand for turns and rotations. A detailed notation guide can be found here for reference:

https://ruwix.com/the-rubiks-cube/notation/advanced/

This project includes simulation for all quarter and half face turns, slice turns, double layer turns and quarter cube rotations. This includes both primary and inverse moves (CW and CCW).

## Solving Algorithm
The AI that solves the cube mimics the CFOP method that is used commonly in advanced speed-cubing. This method is a 4 step method represented by the name: Cross , F2L, OLL, PLL. 

This method is not an "optimal" algorithm, this is a human method. Furthermore, the heuristics used in the AI's algorithm are inadmissible, as a result search times are far shorter, but solution found for each search step is not guaranteed to be the shortest.

Steps involving search are limited to only attempting quarter face turns. Slices, half turns, cube rotations and 2 layer turns are excluded from the search, as they are all composed of some combination of the quarter face turns. OLL and PLL use algorithms that may include any combination of moves since we don't worry about a branching factor there.

#### Cross
1 IDA* search to solve the bottom cross (4 bottom edges).

#### F2L (First 2 Layers)
4 IDA* searches to solve F2L. It solves each pair (1 bottom corner + 1 second layer edge) one at a time using a separate search.

#### OLL (Orientation of Last Layer)
Brute force testing of 57 possible algorithms which cover all possible OLL cases. This can require additional U turns to set up the algorithm.

Algorithms are read from oll.txt

#### PLL (Permutation of Last Layer)
Brute force testing of 21 possible algorithms which cover all possible OLL cases. This can require additional U turns to set up the algorithm, as well as additional U turns after the algorithm to align the last layer with the other two layers. A 22nd algorithm is included, to cover any case when the layers are misaligned and just require U turns. 

Algorithms are read from pll.txt

## Roadmap

- [ ] Add a GUI
- [ ] Add a changelog
- [ ] Improve search heuristics
- [ ] Improve code documentation
