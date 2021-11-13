"""
cube.py
Module for Cube data structure and creation
"""
from math import sqrt
import random

from cubesolver.src.actions import ACTIONS_3x3

# color escape sequences for xterm-256color bgs
ORANGE_BG = "\033[48;5;208m  \033[0;0m"
YELLOW_BG = "\033[48;5;11m  \033[0;0m"
RED_BG = "\033[48;5;9m  \033[0;0m"  # 1
GREEN_BG = "\033[48;5;10m  \033[0;0m"  # 2
BLUE_BG = "\033[48;5;12m  \033[0;0m"  # 21
WHITE_BG = "\033[48;5;254m  \033[0;0m"


class Cube:
    """ data structure to represent a rubiks cube
    """

    def __init__(self, state):
        self.size = int(len(state[0]))
        self.state = state

    def display_text(self):
        """ prints to terminal a text representation of the cube

            the print output represents a physical cube's faces as if
            they were unfolded away from the middle (front) face into 2d space
            numbers 1-6 represent colors
        """
        output = ""
        for i in range(self.size):
            output += " " * (self.size * 3 + 1)
            output += "".join(str(self.state[5][i]))
            output += "\n"
        for i in range(self.size):
            output += "".join(str(self.state[4][i]))
            output += " "
            output += "".join(str(self.state[1][i]))
            output += " "
            output += "".join(str(self.state[2][i]))
            output += " "
            output += "".join(str(self.state[3][i]))
            output += "\n"
        for i in range(self.size):
            output += " " * (self.size * 3 + 1)
            output += "".join(str(self.state[0][i]))
            output += "\n"
        print(output)

    def display_colors(self):
        """ prints to terminal a colored representation of the cube

        the print output represents a physical cube's faces as if
        they were unfolded away from the middle (front) face into 2d space
        """
        output = ""
        for i in range(self.size):
            output = " " * (self.size * 2)
            print(output, end='')
            for color in self.state[5][i]:
                print(pick_color(color), end='')
            print()
        for i in range(self.size):
            for color in self.state[4][i]:
                print(pick_color(color), end='')
            for color in self.state[1][i]:
                print(pick_color(color), end='')
            for color in self.state[2][i]:
                print(pick_color(color), end='')
            for color in self.state[3][i]:
                print(pick_color(color), end='')
            print()
        for i in range(self.size):
            output = " " * (self.size * 2)
            print(output, end='')
            for color in self.state[0][i]:
                print(pick_color(color), end='')
            print()

    def execute_action(self, action):
        """ simulates a turn or rotation of the cube

        actions.py contains the functions that modify the state in order to perform each action

        Args:
            action (string): string representation of the action to perform in 3x3 Rubiks notation
                example strings:
                R -> turn right face CW 1/4
                R' -> counterclockwise turn of right face
                x -> clockwise rotation around x axis

                see README.md for more detailed notation
                ACTIONS_3x3 is a dictionary that maps action to the correct function from actions.py

        Returns:
            Cube: a Cube reflecting the new state after the action is performed
        """
        state = deepcopy_state(self.state)
        max_idx = self.size - 1

        ACTIONS_3x3[action](state, max_idx)
        return Cube(state)

    def execute_action_sequence(self, actions):
        """simulates a series of actions on the cube (turns or rotations)

        Args:
            actions (string list): sequence of actions to simulate on the cube

        Returns:
            Cube: a Cube reflecting the new state after the sequence is performed
        """
        state = deepcopy_state(self.state)

        cube = Cube(state)
        for action in actions:
            cube = cube.execute_action(action)
        return cube

    def scramble(self):
        """performs a 25 move random scramble on the cube struct
        - scramble method is picking random moves and executing them
        - this algorithm avoids any wasted moves
            ex: R' R: cancels out to 0 moves, L L L = L' 1 move

        Returns:
            Cube: the new scrambled cube
            list: sequence of moves used to scramble
        """
        moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]
        move_sequence = []
        move_sequence.append(random.choice(moves))
        while len(move_sequence) < 25:
            move = random.choice(moves)
            is_previous_inverse = not (move_sequence[-1][0] != move[0] or len(move_sequence[-1]) == len(move))
            is_triple_duplicate = len(move_sequence) > 2 and (move == move_sequence[-1] == move_sequence[-2])

            if not is_previous_inverse and not is_triple_duplicate:
                move_sequence.append(move)

        cube = Cube(self.state)
        for move in move_sequence:
            cube = cube.execute_action(move)

        return cube, move_sequence


def pick_color(char):
    """ match a char or num to it's color code

    Args:
        char (string/char or int): an identifier representing the color of a cube square

    Returns:
        string: an xterm-256 escape sequence used to print a colored bg square
    """
    if char == 'R' or char == 4:
        return RED_BG
    elif char == 'G' or char == 1:
        return GREEN_BG
    elif char == 'B' or char == 3:
        return BLUE_BG
    elif char == 'Y' or char == 5:
        return YELLOW_BG
    elif char == 'O' or char == 2:
        return ORANGE_BG
    elif char == 'W' or char == 0:
        return WHITE_BG


def deepcopy_state(state):
    """performs a deepcopy on the a 3d list cube state

    Args:
        state (3d list): a cube state we want to copy

    Returns:
        3d list: a deep copy of state
    """
    return [[[x for x in y] for y in z] for z in state]


def string_to_state(string):
    """ convert a single string into a cube state

    Args:
        string (string): a string representing cube state

    Returns:
        3d list: a useable cube state
    """
    state_1d = list(string.split(' '))
    size = int(sqrt(len(state_1d) // 6))
    state_3d = []
    for i in range(6):
        state_3d.append([])
        for j in range(size):
            state_3d[i].append([])
        for j in range(size * size):
            state_3d[i][j // size].append(state_1d[i * size * size + j])

    # state_3d = print(tuple(tuple(tuple(x) for x in y) for y in state_3d))
    return state_3d


solved_state_ints = string_to_state('0' + ' 0' * 8 + " 3" * 9 + " 4" * 9 + " 1" * 9 + " 2" * 9 + " 5" * 9)
for i in range(6):
    for j in range(3):
        for k in range(3):
            solved_state_ints[i][j][k] = int(solved_state_ints[i][j][k])
