> Note for employers and viewers: If you want to see my best code, check the C# code in this repository, as that is the future of the project. That code is more recent and a better demo of my work, than the original Python code.
> 
> However, if you want to test out the program I highly recommend using the Python version and it's instructions below until I get the time to finish porting and documenting the C# version. The C# version is not quite useable yet.

# Rubiks Cube AI
A terminal menu application that simulates a 3x3 rubik's cube. Originally written in Python. Some of the functionality is listed below.

- Creation of a solved 3x3 cube
- Simulate turns or rotations
- Execution of random 25 move scrambles
- Display the cube state as a 2D unfolded cube in terminal (with colors)
- Solve the cube using the most popular speedsolving method for humans: CFOP

> Note: I have begun the process of porting to C# for learning purposes, refactoring, and adding features. This is described below. These files are meant more for viewing than use currently, as the program's menu and README documentation is not quite useable yet.

The C# files included in this repository are a W.I.P., porting over from Python and adding additional features such as NxN dimensional cubes. Currently, the C# version supports the following operations.

- Creation of an NxN solved cube
- Scramble any cube, using an algorithm that scales with the cube's size
- Simulate the turning of any layer in either direction, using user input
- Display the cube state as a 2D unfolded cube in terminal (with colors)

_No support for an AI solver has been added yet to the C# version_

_The menu doesn't have prompts and documentation configured yet_

## Installation & Running
You must have Python 3 installed. The project was tested and developed using Python 3.9.

Download the desired release's source code on GitHub. Navigate to the PythonApp directory containing the README and the cubesolver directory, start the script with
the command: _python3 cubesolver_
```shell
$ python3 cubesolver
```
Alternatively, you can run the \_\_main\_\_.py script in cubesolver directly.

## 3x3 Notation Guide
This project uses official WCA notation to represent the cube, this is especially important to understand for turns and rotations. A detailed notation guide can be found here for reference:

[J Perm's Notation Guide](https://jperm.net/3x3/moves)

Here is a quick cheat sheet from J Perm's website:

<img src="https://jperm.net/images/notation.png" width="700" height="350">

The above moves are the normal moves in the clockwise direction. You can reverse the direction of any move by appending a single quote ' to the letter. Reversed, or inverse moves, are counter-clockwise. Appending a 2 to the move just means do it twice in a row.

The program provides simulation for all official moves, as well as their doubles and inverses.

## Visualizing the Cube
The cube state is primarily displayed use xterm-256 color escape sequences. It is unfolded from the front face. The front face in this case is blue.

Here is a solved cube before a scramble, and the new cube after the scramble:

<img src="https://user-images.githubusercontent.com/63261198/141620907-188bdb3a-824e-4859-924f-80ed26da9f98.png" width="700" height="400">

> Note: This is not compatible with some computer terminals, only terminals that support xterm-256

Because some terminals do not support all the colors used, the current alternative method to display the cube is using numbers rather than colors. Numbers 1-6 represent colors.

Here is a solved cube displayed with numbers:

<img src="https://user-images.githubusercontent.com/63261198/138527688-b586fcb1-effb-4cef-8ce4-321b00a14c7d.png" width="700" height="200">

## CFOP Solving Algorithm
The AI that solves the cube mimics the CFOP method that is used commonly in advanced speed-cubing. This method is a 4 step method represented by the name: Cross , F2L, OLL, PLL. 

- The bottom cross is solved first using 1 IDA* search.
- F2L (first 2 layer) is solved using 4 consecutive IDA* searches.
- OLL (orient last layer) is solved by testing algorithms saved in oll.txt. These cover all OLL cases.
- PLL (permute last layer) is solved by testing algorithms saved in pll.txt. These cover all PLL cases.

## Known Issues
- Occasionally, F2L can take awhile (10-15 seconds) in an unlucky case

## Roadmap
- [x] Add a menu loop
- [x] Add a changelog
- [ ] Improve F2L search heuristics
- [ ] Implement Kociemba's Algorithm
- [ ] Add a GUI

## Long Term Goals (future versions)

- Add support for alternate cube sizes (2x2, 4x4, 5x5, etc.)
- Live 3D simulation of the cube and turn animation
- Deploy as a web app

Supporting larger cubes becomes much more complex not only to solve, but even operations such as turns or node creation
become more expensive. I likely need to implement variants of Kociemba's algorithm in order find solutions for larger cubes.

Eventually I will port to a compiled language like Java to improve performance and pursue these goals. These goals 
will require a lot of refactoring regardless, so it would be a good idea to port beforehand.
## Advice & Collaboration
Feel free to email me at tylimbach@gmail if you have any advice or would like to aid in the project.


