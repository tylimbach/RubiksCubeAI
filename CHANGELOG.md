_All notable changes will be found here_


# [1.1.0] (2021-11-13)
## Release Notes
> File layout has changed and so has the command to launch the application. Check the README.md to see updated guides or info.
### Added
- New commmands:
    - Help: toggle a display that shows all valid moves and their notation
    - Toggle Text Mode: toggle the display type of the cube from colors to arrays with numbers
- Automatic parsing of user inputted move sequences in place of a command
- Simultaneously display the before and after cube after executing any command in the terminal
- Display additional tracked information like move history
- CHANGLOG.md added to repo
### Changed
- Restructured & Organized Files & Modules
- Main script is now `__main__.py`
- Improved visual layout of terminal manu
- README.md updated
- .gitignore updated
### Fixed
- Solve algorithm failing to find a solution for various PLL and OLL cases

# [1.0.0] (2021-10-26)
## Release Notes
> This is the first stable release. The user can now interface with the program via a terminal menu.
### Added
- Menu loop to control application flow
- Menu accepts commands from the user
- Expanded actions to include all 3x3 official moves:
    - Rotations added
    - Slice turns added
- Support to directly execute inverse or double variation of any action
- Ability for the user to provide custom random seeds

### Changed
- Application now accepts inputs and runs as a loop, as described above
- README.md updated
---
# Pre-release Notes
The "versions" listed here are not tagged or released. This section is just a vague chronological record of major changes in very early development. The numbers aren't attached to specific commits and may never be. Eventually this section will likely be removed.
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
- Support for more actions (such as wide turns)
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
