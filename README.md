# Rubiks Cube AI
A terminal menu application that simulates a 3x3 rubik's cube written in Python. It supports multiple operations.

- Creation of a solved 3x3 cube
- Simulate turns or rotations
- Execution of random 25 move scrambles
- Display the cube state as a 2D unfolded cube in terminal (with colors)
- Solve the cube using the most popular speedsolving method for humans: CFOP

## Installation
You must have Python 3 installed. The project was tested on Python 3.9.

Download the repository on GitHub. Navigate to project folder containing the README and rubikscube directory, start the script with
the command: _python3 cubesolver_
```shell
/rubiks-cube $ python3 cubesolver
```

## 3x3 Notation
This project uses official rubik's cube notation to represent the cube, this is especially important to understand for turns and rotations. A detailed notation guide can be found here for reference:

[J Perm's Notation Guide](https://jperm.net/3x3/moves)

Here is a quick cheat sheet from J Perm's website:

<img src="https://jperm.net/images/notation.png" width="700" height="350">

The above moves are the normal moves in the clockwise direction. You can reverse the direction of any move by appending a single quote ' to the letter. Reversed, or inverse moves, are counter-clockwise. Appending a 2 to the move just means do it twice in a row.

The program provides simulation for all official moves: quarter and half face turns, slice turns, two layer (wide) turns and quarter cube rotations. This includes both primary and inverse moves (CW and CCW).

## Visualizing the Cube
The cube state is primarily displayed use xterm-256 color escape sequences. It is unfolded from the front face. The front face in this case is green.
> Note: This is not compatible with some computer terminals, only terminals that support xterm-256

Here is a solved cube before a scramble, and the new cube after the scramble:

<img src="https://user-images.githubusercontent.com/63261198/141620907-188bdb3a-824e-4859-924f-80ed26da9f98.png" width="700" height="400">


Because some terminals do not support all the colors used, the current alternative method to display the cube is using numbers rather than colors. Numbers 1-6 represent colors.

Here is a solved cube displayed with numbers:

<img src="https://user-images.githubusercontent.com/63261198/138527688-b586fcb1-effb-4cef-8ce4-321b00a14c7d.png" width="700" height="200">

## CFOP Solving Algorithm
The AI that solves the cube mimics the CFOP method that is used commonly in advanced speed-cubing. This method is a 4 step method represented by the name: Cross , F2L, OLL, PLL. 

#### Cross
Bottom 4 edges. Uses IDA* search.

#### F2L (First 2 Layers)
4 corner/edge pairs. Uses 4 IDA* searches.

#### OLL (Orientation of Last Layer)
Attempts algorithms read from oll.txt. The 57 algorithms cover all cases when positioned correctly.

#### PLL (Permutation of Last Layer)
Attempts algorithms read from pll.txt. The 21 algorithms cover all cases when positioned correctly.

## Known Issues
None

## Roadmap
- [x] Add a menu loop
- [ ] Add a changelog
- [ ] Improve F2L search heuristics
- [ ] Implement Kociemba's Algorithm
- [ ] Add a GUI

## Long Term Goals

- Add support for alternate cube sizes (2x2, 4x4, 5x5, etc.)
- Live 3D simulation of the cube and turn animation
- Deploy as a web app

Supporting larger cubes becomes much more complex not only to solve, but even operations such as turns or node creation
become more expensive. I likely need to implement variants of Kociemba's algorithm in order to simulate larger cubes.

Eventually I will port to a compiled language like Java to improve performance and pursue these goals. These goals 
will require a lot of refactoring regardless, so it would be a good idea to port beforehand.
## Advice & Collaboration
Feel free to email me at tylimbach@gmail if you have any advice or would like to aid in the project.


