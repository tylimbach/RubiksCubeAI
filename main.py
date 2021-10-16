"""
main.py
Main file for Rubik's Cube solver
"""

__author__ = "Tyler Limbach"

import math
import random

import numpy as np
from numpy.lib.function_base import copy
from collections import deque

# color escape sequences for xterm-256color bgs
O = "\033[48;5;208m  \033[0;0m"
Y = "\033[48;5;3m  \033[0;0m"
R = "\033[48;5;1m  \033[0;0m" # 1
G = "\033[48;5;2m  \033[0;0m" # 2
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
        """ prints to terminal a text representation of the cube
        
        the print output represents a physical cube's faces as if
        they were unfolded away from the middle (front) face into 2d space
        
        ex: a default solved cube state (green is front face)
        
            YYY                   
            YYY                    
            YYY                                     
        RRR GGG OOO BBB
        RRR GGG OOO BBB   
        RRR GGG OOO BBB
            WWW
            WWW
            WWW 
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
            output += " "
            output += np.array_str(self.state[3, i, :])
            output += "\n"
        for i in range(self.size):
            output += " " * (self.size*4+2)
            output += np.array_str(self.state[0, i, :])
            output += "\n"
        print(output)
        
    def display_colors(self):
        """ prints to terminal a colored representation of the cube in space
        
        the print output represents a physical cube's faces as if
        they were unfolded away from the middle (front) face into 2d space
        
        this function works just like display_text, but instead of printing
        letters it displays colors using color escape sequences from xterm-256
        as a result, this function may not work correctly in terminals that don't
        support xterm-256
        """         
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
        """simulates a turn of this cube

        Args:
            move (string): a string representing the face to turn 
                and the direction to turn. only 1 letter if clockwise.
                counterclockwise represented by a letter follow by a single quote '
                
                example: 
                    R -> clockwise turn of right face
                    U' -> counterclockwise turn of up face

        Returns:
            Cube: the new cube after the turn
        """
        new_state = np.copy(self.state)
        
        if move == "R":
            new_state[2] = np.rot90(new_state[2], 3)
            new_state[[5], :, [self.size - 1]], new_state[[1], :, [self.size - 1]], \
                new_state[[0], :, [self.size - 1]], new_state[[3], ::-1, [0]] = \
                new_state[[1], :, [self.size - 1]], new_state[[0], :, [self.size - 1]], \
                new_state[[3], ::-1, [0]], new_state[[5], :, [self.size - 1]]
        if move == "R'":
            new_state[2] = np.rot90(new_state[2], 1)
            new_state[[1], :, [self.size - 1]], new_state[[0], :, [self.size - 1]], \
                new_state[[3], ::-1, [0]], new_state[[5], :, [self.size - 1]] = \
                new_state[[5], :, [self.size - 1]], new_state[[1], :, [self.size - 1]], \
                new_state[[0], :, [self.size - 1]], new_state[[3], ::-1, [0]]
        if move == "L":
            new_state[4] = np.rot90(new_state[4], 3)
            new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]], new_state[[5], :, [0]] = \
                new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]]
        if move == "L'":
            new_state[4] = np.rot90(new_state[4], 1)
            new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]] = \
                new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [self.size - 1]], new_state[[5], :, [0]]
        if move == "U":
            new_state[5] = np.rot90(new_state[5], 3)
            new_state[[1], [0], :], new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :] = \
                new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :], new_state[[1], [0], :]
        if move == "U'":
            new_state[5] = np.rot90(new_state[5], 1)
            new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :], new_state[[1], [0], :] = \
                new_state[[1], [0], :], new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :]
        if move == "D":
            new_state[0] = np.rot90(new_state[0], 3)
            new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :], new_state[[4], [self.size-1], :] = \
                new_state[[4], [self.size-1], :], new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :]           
        if move == "D'":
            new_state[0] = np.rot90(new_state[0], 1)
            new_state[[4], [self.size-1], :], new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :] = \
                new_state[[1], [self.size-1], :], new_state[[2], [self.size-1], :], new_state[[3], [self.size-1], :], new_state[[4], [self.size-1], :]
        if move == "F":
            new_state[1] = np.rot90(new_state[1], 3)
            new_state[[5], [self.size-1], :], new_state[[2], :, [0]], new_state[[0], [0], :], new_state[[4], :, [self.size-1]] = \
                new_state[[4], ::-1, [self.size-1]], new_state[[5], [self.size-1], :], new_state[[2], ::-1, [0]], new_state[[0], [0], :]
        if move == "F'":
            new_state[1] = np.rot90(new_state[1], 1)
            new_state[[4], ::-1, [self.size-1]], new_state[[5], [self.size-1], :], new_state[[2], ::-1, [0]], new_state[[0], [0], :] = \
                new_state[[5], [self.size-1], :], new_state[[2], :, [0]], new_state[[0], [0], :], new_state[[4], :, [self.size-1]]
        if move == "B":
            new_state[3] = np.rot90(new_state[3], 3)
            new_state[[4], ::-1, [0]], new_state[[5], [0], :], new_state[[2], ::-1, [self.size-1]], new_state[[0], [self.size-1], :] = \
                new_state[[5], [0], :], new_state[[2], :, [self.size-1]], new_state[[0], [self.size-1], :], new_state[[4], :, [0]]
        if move == "B'":
            new_state[3] = np.rot90(new_state[3], 1)
            new_state[[5], [0], :], new_state[[2], :, [self.size-1]], new_state[[0], [self.size-1], :], new_state[[4], :, [0]] = \
                new_state[[4], ::-1, [0]], new_state[[5], [0], :], new_state[[2], ::-1, [self.size-1]], new_state[[0], [self.size-1], :]
                
        return Cube(new_state)
    
    def scramble(self):
        """performs a 25 move random scramble on the cube struct
        - scramble method is picking random moves and executing them
        - this algorithm avoids any wasted moves
            ex: R' R: cancels out to 0 moves, L L L = L' 1 move 

        Returns:
            Cube: the new scrambled cube
            list: sequence of moves used to scramble
        """
        options = ["U", "U'", "R", "R'", "L'", "L'", "D'", "D'", "F", "F'", "B", "B'"]
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
        return " ".join(self.state.state)


    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return np.array_equiv(self.state.state, other.state.state)
        

    def __hash__(self):
        return hash(tuple(np.array2string(self.state.state)))
    

def string_to_state(string):
    state = np.array(list(string.split(' ')))
    size = int(math.sqrt(np.size(state) // 6))
    state = np.reshape(state, newshape=(6, size, size))
    return state

solved_state = string_to_state("W"+" W"*8+" G"*9+" O"*9+" B"*9 +" R"*9+" Y"*9)
#solved_layer1 = string_to_state() 

# This function backtracks from current node to reach initial configuration.
# The list of actions would constitute a solution path
def find_path(node):	
	path = []	
	while node.parent is not None:
		path.append(node.action)
		node = node.parent
	path.reverse()
	return path


def run_bfs(root_node):
	start_time = time.time()
	frontier = deque([root_node])
	explored = set()
	max_memory = 0
	while len(frontier) > 0:
		max_memory = max(max_memory, sys.getsizeof(frontier)+sys.getsizeof(explored))
		cur_time = time.time()
		cur_node = frontier.popleft()
		explored.add(cur_node)
		if goal_test(cur_node.state.tiles):
			path = find_path(cur_node)
			end_time = time.time()
			return path, len(explored), (end_time-start_time), max_memory
		for child in get_children(cur_node):
			if child in explored:
				continue
			else:
				frontier.append(child)
	print("frontier empty")	
	return False


def h_layer1(node):
    print()


def main():
    start_state = solved_state
    cube = Cube(start_state)
    root = Node(cube, None, None)
    root.state.display_colors()

    root.state, scramble_seq = root.state.scramble()
    print(" ".join(scramble_seq), '\n')
    
    root.state.display_colors()
    

    
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
