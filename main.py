"""
main.py
Main file for Rubik's Cube solver
"""

__author__ = "Tyler Limbach"

import numpy as np
import math
import random

from numpy.lib.function_base import copy


# color escape sequences for xterm-256color bgs
O = "\033[48;5;208m  \033[0;0m"
Y = "\033[48;5;11m  \033[0;0m"
R = "\033[48;5;9m  \033[0;0m" # 1
G = "\033[48;5;10m  \033[0;0m" # 2
B = "\033[48;5;4m  \033[0;0m" # 21
W = "\033[48;5;254m  \033[0;0m"


def pick_color(char):
    if char == 'R':
        return R
    elif char == 'G':
        return G
    elif char == 'B':
        return B
    elif char == 'Y':
        return Y
    elif char == 'O':
        return O
    elif char == 'W':
        return W

class Cube:
    def __init__(self, state):
        self.size = int(math.sqrt(state.size / 6))
        self.state = state
        
        self.down = self.state[0]
        self.front = self.state[1]
        self.right = self.state[2]
        self.back = self.state[3]
        self.left = self.state[4]
        self.up = self.state[5]

    def display_text(self):
        """       0D 1F 2R 3B 4L 5U               
            555                   
            555                    
            555                   
                                
        444 111 222     333
        444 111 222     333   
        444 111 222     333
        
            000
            000
            000 
        """         
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
            output += "      "
            output += np.array_str(self.state[3, i, :])
            output += "\n"
        for i in range(self.size):
            output += " " * (self.size*4+2)
            output += np.array_str(self.state[0, i, :])
            output += "\n"
        print(output)
        
    def display_colors(self):
        output = ""
        for i in range(self.size):
            output = " " * (self.size*2)
            print (output, end='')
            for color in self.state[5, i, :]:
                print(pick_color(color), end='')
            print()
        for i in range(self.size):
            for color in self.state[4, i, :]:
                print(pick_color(color), end='')
            for color in self.state[1, i, :]:
                print(pick_color(color), end='')
            for color in self.state[2, i, :]:
                print(pick_color(color), end='')
            print("       ", end='')
            for color in self.state[3, i, :]:
                print(pick_color(color), end='')
            print()
        for i in range(self.size):
            output = " " * (self.size*2)
            print (output, end='')
            for color in self.state[0, i, :]:
                print(pick_color(color), end='')
            print()
        print(output)
        

    def execute_turn(self, move):
        new_state = np.copy(self.state)
        if move == "R":
            new_state[2] = np.rot90(new_state[2], 3)
            new_state[[5], :, [self.size - 1]], new_state[[1], :, [self.size - 1]], \
                new_state[[0], :, [self.size - 1]], new_state[[3], ::-1, [0]] = \
                new_state[[1], :, [self.size - 1]], new_state[[0], :, [self.size - 1]], \
                new_state[[3], ::-1, [0]], new_state[[5], :, [self.size - 1]]
        if move == "R-":
            new_state[2] = np.rot90(new_state[2], 1)
            new_state[[1], :, [self.size - 1]], new_state[[0], :, [self.size - 1]], \
                new_state[[3], ::-1, [0]], new_state[[5], :, [self.size - 1]] = \
                new_state[[5], :, [self.size - 1]], new_state[[1], :, [self.size - 1]], \
                new_state[[0], :, [self.size - 1]], new_state[[3], ::-1, [0]]
        if move == "L":
            new_state[4] = np.rot90(new_state[4], 3)
            new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]], new_state[[5], :, [0]] = \
                new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]]
        if move == "L-":
            new_state[4] = np.rot90(new_state[4], 1)
            new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]] = \
                new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]], new_state[[5], :, [0]]
        if move == "U":
            new_state[5] = np.rot90(new_state[5], 3)
            new_state[[1], [0], :], new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :] = \
                new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :], new_state[[1], [0], :]
        if move == "U-":
            new_state[5] = np.rot90(new_state[5], 1)
            new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :], new_state[[1], [0], :] = \
                new_state[[1], [0], :], new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :]
        if move == "D":
            new_state[0] = np.rot90(new_state[0], 3)
            new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :], new_state[[4], [self.size-1], :] = \
                new_state[[4], [self.size-1], :], new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :]           
        if move == "D-":
            new_state[0] = np.rot90(new_state[0], 1)
            new_state[[4], [self.size-1], :], new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :] = \
                new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :], new_state[[4], [self.size-1], :]
        if move == "F":
            new_state[1] = np.rot90(new_state[1], 3)
            new_state[[5], [self.size-1], :], new_state[[2], :, [0]], new_state[[0], [0], :], new_state[[4], :, [self.size-1]] = \
                new_state[[4], ::-1, [self.size-1]], new_state[[5], [self.size-1], :], new_state[[2], ::-1, [0]], new_state[[0], [0], :]
        if move == "F-":
            new_state[1] = np.rot90(new_state[1], 1)
            new_state[[4], ::-1, [self.size-1]], new_state[[5], [self.size-1], :], new_state[[2], ::-1, [0]], new_state[[0], [0], :] = \
                new_state[[5], [self.size-1], :], new_state[[2], :, [0]], new_state[[0], [0], :], new_state[[4], :, [self.size-1]]
        if move == "B":
            new_state[3] = np.rot90(new_state[3], 3)
            new_state[[4], ::-1, [0]], new_state[[5], [0], :], new_state[[2], ::-1, [self.size-1]], new_state[[0], [self.size-1], :] = \
                new_state[[5], [0], :], new_state[[2], :, [self.size-1]], new_state[[0], [self.size-1], :], new_state[[4], :, [0]]
        if move == "B-":
            new_state[3] = np.rot90(new_state[3], 1)
            new_state[[5], [0], :], new_state[[2], :, [self.size-1]], new_state[[0], [self.size-1], :], new_state[[4], :, [0]] = \
                new_state[[4], ::-1, [0]], new_state[[5], [0], :], new_state[[2], ::-1, [self.size-1]], new_state[[0], [self.size-1], :]
        return Cube(new_state)
    
    def scramble(self):
        options = ["U", "U-", "R", "R-", "L", "L-", "D", "D-", "F", "F-", "B", "B-"]
        move_sequence = []
        move_sequence.append(random.choice(options));
        while len(move_sequence) < 25:
            move = random.choice(options)
            is_previous_inverse = not (move_sequence[-1][0] != move[0] or len(move_sequence[-1]) == len(move))
            is_triple_duplicate = len(move_sequence) > 2 and (move == move_sequence[-1] == move_sequence[-2])

            if not is_previous_inverse and not is_triple_duplicate:
                move_sequence.append(move)
            
        cube = Cube(copy(self.state))
        for move in move_sequence:
            cube = cube.execute_turn(move)
        return cube, move_sequence
    

class Node:
    def __init__(self, state, parent, move):
        self.state = state
        self.parent = parent
        self.move = move

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.state)


    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.state == other.state.state
        

    def __hash__(self):
        return hash(tuple(self.state.tiles))
    

def string_to_state(string):
    state = np.array(list(string.split(' ')))
    size = int(math.sqrt(np.size(state) // 6))
    state = np.reshape(state, newshape=(6, size, size))
    return state

solved = string_to_state("W"+" W"*8+" G"*9+" O"*9+" B"*9 +" R"*9+" Y"*9)
#solved_layer1 = string_to_state )

# This function backtracks from current node to reach initial configuration.
# The list of actions would constitute a solution path
def find_path(node):	
	path = []	
	while node.parent is not None:
		path.append(node.action)
		node = node.parent
	path.reverse()
	return path


def h_layer1(node):
    print()


def main():
    start_state = solved
    cube = Cube(start_state)
    root = Node(cube, None, None)

    root.state, scramble_seq = root.state.scramble()
    root.state.display_colors()
    
    print(" ".join(scramble_seq), '\n')
    
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
