"""
Rubik's Cube Solver
by Tyler Limbach
"""

__author__ = "Tyler Limbach"

import numpy as np
import math

"""
    555
    555
    555
    
444 111 222 333
444 111 222 333
444 111 222 333
    
    000
    000
    000 
"""


class Cube:
    def __init__(self, state):
        self.size = int(math.sqrt(state.size / 6))
        self.state = state

    def display(self):
        output = ""
        for i in range(self.size):
            output += " " * (self.size*4+2)
            output += np.array_str(self.state[5, i, :])
            output += "\n"
        for i in range(self.size):
            output += np.array_str(self.state[4, i, :])
            output += " "
            output += np.array_str(self.state[1, i, :])
            output += " "
            output += np.array_str(self.state[2, i, :])
            output += " "
            output += np.array_str(self.state[3, i, :])
            output += "\n"
        for i in range(self.size):
            output += " " * (self.size*4+2)
            output += np.array_str(self.state[0, i, :])
            output += "\n"
        print(output)

    def execute_turn(self, move):
        new_state = np.copy(self.state)
        if move == "R":
            new_state[2] = np.rot90(new_state[2], 3)
            new_state[[5], :, [self.size - 1]], new_state[[1], :, [self.size - 1]], \
                new_state[[0], :, [self.size - 1]], new_state[[3], :, [self.size - 1]] = \
                new_state[[1], :, [self.size - 1]], new_state[[0], :, [self.size - 1]], \
                new_state[[3], :, [self.size - 1]], new_state[[5], :, [self.size - 1]]
        if move == "R'":
            new_state[2] = np.rot90(new_state[2], 1)
            new_state[[1], :, [self.size - 1]], new_state[[0], :, [self.size - 1]], \
                new_state[[3], :, [self.size - 1]], new_state[[5], :, [self.size - 1]] = \
                new_state[[5], :, [self.size - 1]], new_state[[1], :, [self.size - 1]], \
                new_state[[0], :, [self.size - 1]], new_state[[3], :, [self.size - 1]]
        if move == "L":
            new_state[4] = np.rot90(new_state[2], 3)
            new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], :, [0]], new_state[[5], :, [0]] = \
                new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], :, [0]]
        if move == "L'":
            new_state[4] = np.rot90(new_state[2], 1)
            new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], :, [0]] = \
                new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], :, [0]], new_state[[5], :, [0]]
        if move == "U":
            new_state[5] = np.rot90(new_state[5], 3)
            new_state[[1], [0], :], new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :] = \
                new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :], new_state[[1], [0], :]
        """
        if move == "U'":
        if move == "D":
        if move == "D'":
        if move == "F":
        if move == "F'":
        if move == "B":
        if move == "B'":
        """
        return Cube(new_state)


class Node:
    def __init__(self, state, parent, move):
        self.state = state
        self.parent = parent
        self.move = move


def string_to_cube(size, string):
    state = np.array(list(string.split(' ')))
    state = np.reshape(state, newshape=(6, size, size))
    return state


solved = string_to_cube(3, "W W W W W W W W W " +
                           "R R R R R R R R R " +
                           "G G G G G G G G G " +
                           "O O O O O O O O O " +
                           "B B B B B B B B B " +
                           "Y Y Y Y Y Y Y Y Y")


def main():
    state = solved
    print(solved)
    cube = Cube(state)
    cube.display()
    cube.execute_turn("R'").execute_turn("U").execute_turn("R").display()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
