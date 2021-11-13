
# Change Log
All notable changes to this project will be documented in this file.


## [1.2.0]
The file layout has changed and so has the command to launch the application. Check the README.md to see updated guides or info.
### Added
- Toggle command to display notation help for actions (moves)
- Toggle command to toggle display type between colored squares and arrays of numbers.
- Set or remove a custom random seed
### Changed
- Restructured & Organized Files & Modules
- Improved visual layout of terminal manu
- README.md

## [1.1.0]
### Added
- Auto-detect when a move or move sequence is entered, and perform it.
- Display the cube's state before the previous action or command, as well as the new cube after than action
- Track time each command takes (mostly for solves)
- Track user's turn history

## [1.0.0]
Major upgrades added to restructure the program and to make it user-friendly in the form of a terminal menu loop.
### Added
- Menu loop to control application flow
- Menu accepts commands:
  - Random scramble
  - Enter a sequence of strings to execute moves on the cube
  - Have the AI solve the cube

---
## [0.6.0] 
### Added
- README.md explaining project and instructions
- .gitignore added
- Increased solve speed via optimizations
- Function to execute a sequence of moves given 1 string

## [0.5.1] 
### Fixed
- Certain PLL cases weren't matching to their algorithm

## [0.5.0] 
### Added 
- Support for more actions (slice turns, rotations, wide turns)
### Fixed
- PLL and OLL cases involving the added turn types now work correctly

## [0.4.0] 
oll.txt & pll.txt files must be in project directory, and must not be altered by the user.
### Added 
- Last layer algorithms
- oll.txt  & pll.txt files
### Changed
- Now solves last layer via algorithm case tests rather than IDA* search.

## [0.3.0] 
### Added 
- Capable of very slow full solves
### Changed
- Cube now stores the state as 3D list instead of NumPy array

## [0.2.0]

### Added 
- Search Nodes
- Heuristics and IDA* algorithm

## [0.1.0]
### Added 
- Iteration 1 of Cube data structure
- Colored terminal unfolded cube display
