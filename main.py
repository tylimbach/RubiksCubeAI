"""
main.py
Main file for Rubik's Cube solver
"""

__author__ = "Tyler Limbach"

from math import sqrt as sqrt
import random
import time
import timeit
import cProfile

import numpy as np
from numpy import array_equiv as array_equiv
from numpy.lib.function_base import copy
from collections import deque

# color escape sequences for xterm-256color bgs
O = "\033[48;5;208m  \033[0;0m"
Y = "\033[48;5;11m  \033[0;0m"
R = "\033[48;5;9m  \033[0;0m" # 1
G = "\033[48;5;10m  \033[0;0m" # 2
B = "\033[48;5;12m  \033[0;0m" # 21
W = "\033[48;5;254m  \033[0;0m"



def pick_color(char):
    if char == 'R' or char == 4:
        return R
    elif char == 'G' or char == 1:
        return G
    elif char == 'B' or char == 3:
        return B
    elif char == 'Y' or char == 5:
        return Y
    elif char == 'O' or char == 2:
        return O
    elif char == 'W' or char == 0:
        return W

class Cube:
    def __init__(self, state):
        self.size = int(sqrt(state.size / 6))
        self.state = state
        
        # self.down = self.state[0]
        # self.front = self.state[1]
        # self.right = self.state[2]
        # self.back = self.state[3]
        # self.left = self.state[4]
        # self.up = self.state[5]
        

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
        

    def execute_action(self, move):
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
        
        max_idx = self.size - 1
        
        if move == "R":
            new_state[2] = np.rot90(new_state[2], 3)
            new_state[[5], :, [max_idx]], new_state[[1], :, [max_idx]], \
                new_state[[0], :, [max_idx]], new_state[[3], ::-1, [0]] = \
                new_state[[1], :, [max_idx]], new_state[[0], :, [max_idx]], \
                new_state[[3], ::-1, [0]], new_state[[5], :, [max_idx]]
        elif move == "R'":
            new_state[2] = np.rot90(new_state[2], 1)
            new_state[[1], :, [max_idx]], new_state[[0], :, [max_idx]], \
                new_state[[3], ::-1, [0]], new_state[[5], :, [max_idx]] = \
                new_state[[5], :, [max_idx]], new_state[[1], :, [max_idx]], \
                new_state[[0], :, [max_idx]], new_state[[3], ::-1, [0]]
        elif move == "L":
            new_state[4] = np.rot90(new_state[4], 3)
            new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [max_idx]], new_state[[5], :, [0]] = \
                new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [max_idx]]
        elif move == "L'":
            new_state[4] = np.rot90(new_state[4], 1)
            new_state[[5], :, [0]], new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [max_idx]] = \
                new_state[[1], :, [0]], new_state[[0], :, [0]], new_state[[3], ::-1, [max_idx]], new_state[[5], :, [0]]
        elif move == "U":
            new_state[5] = np.rot90(new_state[5], 3)
            new_state[[1], [0], :], new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :] = \
                new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :], new_state[[1], [0], :]
        elif move == "U'":
            new_state[5] = np.rot90(new_state[5], 1)
            new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :], new_state[[1], [0], :] = \
                new_state[[1], [0], :], new_state[[2], [0], :], new_state[[3], [0], :], new_state[[4], [0], :]
        elif move == "D":
            new_state[0] = np.rot90(new_state[0], 3)
            new_state[[1], [max_idx], :], new_state[[2], [max_idx], :], new_state[[3], [max_idx], :], new_state[[4], [max_idx], :] = \
                new_state[[4], [max_idx], :], new_state[[1], [max_idx], :], new_state[[2], [max_idx], :], new_state[[3], [max_idx], :]           
        elif move == "D'":
            new_state[0] = np.rot90(new_state[0], 1)
            new_state[[4], [max_idx], :], new_state[[1], [max_idx], :], new_state[[2], [max_idx], :], new_state[[3], [max_idx], :] = \
                new_state[[1], [max_idx], :], new_state[[2], [max_idx], :], new_state[[3], [max_idx], :], new_state[[4], [max_idx], :]
        elif move == "F":
            new_state[1] = np.rot90(new_state[1], 3)
            new_state[[5], [max_idx], :], new_state[[2], :, [0]], new_state[[0], [0], :], new_state[[4], :, [max_idx]] = \
                new_state[[4], ::-1, [max_idx]], new_state[[5], [max_idx], :], new_state[[2], ::-1, [0]], new_state[[0], [0], :]
        elif move == "F'":
            new_state[1] = np.rot90(new_state[1], 1)
            new_state[[4], ::-1, [max_idx]], new_state[[5], [max_idx], :], new_state[[2], ::-1, [0]], new_state[[0], [0], :] = \
                new_state[[5], [max_idx], :], new_state[[2], :, [0]], new_state[[0], [0], :], new_state[[4], :, [max_idx]]
        elif move == "B":
            new_state[3] = np.rot90(new_state[3], 3)
            new_state[[4], ::-1, [0]], new_state[[5], [0], :], new_state[[2], ::-1, [max_idx]], new_state[[0], [max_idx], :] = \
                new_state[[5], [0], :], new_state[[2], :, [max_idx]], new_state[[0], [max_idx], :], new_state[[4], :, [0]]
        elif move == "B'":
            new_state[3] = np.rot90(new_state[3], 1)
            new_state[[5], [0], :], new_state[[2], :, [max_idx]], new_state[[0], [max_idx], :], new_state[[4], :, [0]] = \
                new_state[[4], ::-1, [0]], new_state[[5], [0], :], new_state[[2], ::-1, [max_idx]], new_state[[0], [max_idx], :]
                        
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
        moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]
        move_sequence = []
        move_sequence.append(random.choice(moves));
        while len(move_sequence) < 25:
            move = random.choice(moves)
            is_previous_inverse = not (move_sequence[-1][0] != move[0] or len(move_sequence[-1]) == len(move))
            is_triple_duplicate = len(move_sequence) > 2 and (move == move_sequence[-1] == move_sequence[-2])

            if not is_previous_inverse and not is_triple_duplicate:
                move_sequence.append(move)
            
        cube = Cube(copy(self.state))
        for move in move_sequence:
            cube = cube.execute_action(move)
        return cube, move_sequence
    

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return " ".join(self.state.state.flatten())


    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return array_equiv(self.state.state, other.state.state)

    
    def __ne__(self, other):   
        return not self.__eq__(other)     


    def __hash__(self):
        return hash(tuple(self.state.state.tobytes()))
    

def get_children(parent_node):
    children = []
    actions = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        child_node = Node(child_state, parent_node, action)
        children.append(child_node)
    return children


def string_to_state(string):
    state = np.array(list(string.split(' ')))
    size = int(sqrt(np.size(state) // 6))
    state = np.reshape(state, newshape=(6, size, size))
    return state

solved_state = string_to_state("W"+" W"*8+" G"*9+" O"*9+" B"*9 +" R"*9+" Y"*9)
solved_state_ints = string_to_state('0'+' 0'*8+" 1"*9+" 2"*9+" 3"*9 +" 4"*9+" 5"*9)
for i in range(6):
    for j in range(3):
        for k in range(3):
            solved_state_ints[i,j,k] = int(solved_state_ints[i,j,k])

# This function backtracks from current node to reach initial configuration.
# The list of actions would constitute a solution path
def find_path(node):	
	path = []	
	while node.parent is not None:
		path.append(node.action)
		node = node.parent
	path.reverse()
	return path


def cost(root_node, node):
    g = 0
    while node is not root_node:
        g = g + 0.25
        node = node.parent
    return g


def goal_test_solved(state):
    if array_equiv(state, solved_state):
        return True


def h_f2l(state):
    print()


def goal_test_cross(state):
    bottom = state[0,0,1]
    
    # 1 layer check
    return state[0, 0, 1] == bottom and state[0, 2, 1] == bottom \
        and state[0, 1, 0] == bottom and state[0, 1, 2] == bottom \
        and state[1, 2, 1] == state[1, 1, 1] and state[2, 2, 1] == state[2, 1, 1] \
        and state[3, 2, 1] == state[3, 1, 1] and state[4, 2, 1] == state[4, 1, 1] \
        and state[0, 2, 2] == bottom and state[0, 2, 0] == bottom \
        and state[0, 0, 2] == bottom and state[0, 0, 0] == bottom 
    
    # white cross check
    return state[0, 0, 1] == state[0, 1, 1] and state[0, 2, 1] == state[0, 1, 1] \
        and state[0, 1, 0] == state[0, 1, 1] and state[0, 1, 2] == state[0, 1, 1] \
        and state[1, 2, 1] == state[1, 1, 1] and state[2, 2, 1] == state[2, 1, 1] \
        and state[3, 2, 1] == state[3, 1, 1] and state[4, 2, 1] == state[4, 1, 1]
    

# def astar_cross(root_node):
#     frontier = [root_node]
#     seen = set()
#     g = 0
#     while len(frontier) > 0:
#         f_scores = [h_cross(node) + cost(root_node, node) for node in frontier]
#         cur_node = frontier.pop((f_scores.index(min(f_scores))))
#         seen.add(cur_node)
#         cur_node.state.display_colors()
#         print(find_path(cur_node))
#         if h_cross(cur_node.state.state) == 0:
#             path = find_path(cur_node)
#             return path, cur_node
#         for child in get_children(cur_node):
#             if child in seen:
#                 continue
#             elif child not in frontier:
#                 frontier.append(child)
#             else:
#                 same_node = frontier[frontier.index(child)]
#                 if cost(root_node, child) < cost(root_node, same_node):
#                     same_node.parent = child.parent   
                    
        
def idas(root_node, h_func):
	bound = h_cross(root_node)
	path = [root_node]
	while True:
		t = idas_search(path, 0, bound, h_func)
		if t == "FOUND":
			path_taken = find_path(path[-1])
			return path_taken
		elif t == float('inf'):
			return False  # not found
		else:
			bound = t   # increase bound to lowest neighbor's f


def idas_search(path, g, bound, h_func):
    node = path[-1]
    f = h_func(node) + g
    #time.sleep(1)
    #node.state.display_colors()
    #print(h_cross(node))
    #print(f)
    if h_func(node) == 0:  # if reached goal state
        return "FOUND"
    if f > bound:  # if we are over the ids bound
        return f
    minimum = float('inf')
    for child in get_children(node):  # for each child of this node
        if child not in path:
            path.append(child)
            t = idas_search(path, g + 1, bound, h_func)
            if t == "FOUND":  # if reached goal state
                return "FOUND"
            if t < minimum:  # if we have a new bound < inf
                minimum = t
            path.pop()
    return minimum




def h_cross(node):
    h = 0
    state = node.state.state
    bottom = state[0, 1, 1]
    
    # white cross perfect
    if state[1, 2, 1] != state[1, 1, 1] or state[0, 0, 1] != bottom:
        h = h + 1
    if state[2, 2, 1] != state[2, 1, 1] or state[0, 1, 2] != bottom:
        h = h + 1
    if state[3, 2, 1] != state[3, 1, 1] or state[0, 2, 1] != bottom:
        h = h + 1
    if state[4, 2, 1] != state[4, 1, 1] or state[0, 1, 0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5, 0, 1] == bottom:
        h = h + 1 
    if state[5, 2, 1] == bottom:
        h = h + 1
    if state[5, 1, 0] == bottom:
        h = h + 1
    if state[5, 1, 2] == bottom:
        h = h + 1
    
    # # white corners
    # if state[0, 0, 0] != bottom:
    #     h = h + 1
    # if state[0, 0, 2] != bottom:
    #     h = h + 1
    # if state[0, 2, 0] != bottom:
    #     h = h + 1
    # if state[0, 2, 2] != bottom:
    #     h = h + 1
        
    # # top has white corners?
    # if state[5, 0, 2] == bottom:
    #     h = h + 1 
    # if state[5, 2, 0] == bottom:
    #     h = h + 1
    # if state[5, 0, 0] == bottom:
    #     h = h + 1
    # if state[5, 2, 2] == bottom:
    #     h = h + 1   
        
    return h


def h_layer1_1(node):
    h = 0
    state = node.state.state
    bottom = state[0, 1, 1]
    
    # white cross perfect
    if state[1, 2, 1] != state[1, 1, 1] or state[0, 0, 1] != bottom:
        h = h + 1
    if state[2, 2, 1] != state[2, 1, 1] or state[0, 1, 2] != bottom:
        h = h + 1
    if state[3, 2, 1] != state[3, 1, 1] or state[0, 2, 1] != bottom:
        h = h + 1
    if state[4, 2, 1] != state[4, 1, 1] or state[0, 1, 0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5, 0, 1] == bottom:
        h = h + 1 
    if state[5, 2, 1] == bottom:
        h = h + 1
    if state[5, 1, 0] == bottom:
        h = h + 1
    if state[5, 1, 2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0, 0, 0] != bottom or state[4, 2, 2] != state[4, 1, 1]\
            or state[1, 2, 0] != state[1, 1, 1]\
            or state[4, 1, 2] != state[4, 1, 1] or state[1, 1, 0] != state[1, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0, 0, 2] != bottom or state[1, 2, 2] != state[1, 1, 1]\
            or state[2, 2, 0] != state[2, 1, 1]\
            or state[1, 1, 2] != state[1, 1, 1] or state[2, 1, 0] != state[2, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 2] != bottom or state[2, 2, 2] != state[2, 1, 1]\
            or state[3, 2, 0] != state[3, 1, 1]\
            or state[2, 1, 2] != state[2, 1, 1] or state[3, 1, 0] != state[3, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 0] != bottom or state[3, 2, 2] != state[3, 1, 1]\
            or state[4, 2, 0] != state[4, 1, 1]\
            or state[3, 1, 2] != state[3, 1, 1] or state[4, 1, 0] != state[4, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (bad_corners == 4):
        h = h + 1
    return h
    
def h_layer1_2(node):
    h = 0
    state = node.state.state
    bottom = state[0, 1, 1]
    
    # white cross perfect
    if state[1, 2, 1] != state[1, 1, 1] or state[0, 0, 1] != bottom:
        h = h + 1
    if state[2, 2, 1] != state[2, 1, 1] or state[0, 1, 2] != bottom:
        h = h + 1
    if state[3, 2, 1] != state[3, 1, 1] or state[0, 2, 1] != bottom:
        h = h + 1
    if state[4, 2, 1] != state[4, 1, 1] or state[0, 1, 0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5, 0, 1] == bottom:
        h = h + 1 
    if state[5, 2, 1] == bottom:
        h = h + 1
    if state[5, 1, 0] == bottom:
        h = h + 1
    if state[5, 1, 2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0, 0, 0] != bottom or state[4, 2, 2] != state[4, 1, 1]\
            or state[1, 2, 0] != state[1, 1, 1]\
            or state[4, 1, 2] != state[4, 1, 1] or state[1, 1, 0] != state[1, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0, 0, 2] != bottom or state[1, 2, 2] != state[1, 1, 1]\
            or state[2, 2, 0] != state[2, 1, 1]\
            or state[1, 1, 2] != state[1, 1, 1] or state[2, 1, 0] != state[2, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 2] != bottom or state[2, 2, 2] != state[2, 1, 1]\
            or state[3, 2, 0] != state[3, 1, 1]\
            or state[2, 1, 2] != state[2, 1, 1] or state[3, 1, 0] != state[3, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 0] != bottom or state[3, 2, 2] != state[3, 1, 1]\
            or state[4, 2, 0] != state[4, 1, 1]\
            or state[3, 1, 2] != state[3, 1, 1] or state[4, 1, 0] != state[4, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (bad_corners == 4):
        h = h + 2
    elif (bad_corners == 3):
        h = h + 1
    return h
    
def h_layer1_3(node):
    h = 0
    state = node.state.state
    bottom = state[0, 1, 1]
    
    # white cross perfect
    if state[1, 2, 1] != state[1, 1, 1] or state[0, 0, 1] != bottom:
        h = h + 1
    if state[2, 2, 1] != state[2, 1, 1] or state[0, 1, 2] != bottom:
        h = h + 1
    if state[3, 2, 1] != state[3, 1, 1] or state[0, 2, 1] != bottom:
        h = h + 1
    if state[4, 2, 1] != state[4, 1, 1] or state[0, 1, 0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5, 0, 1] == bottom:
        h = h + 1 
    if state[5, 2, 1] == bottom:
        h = h + 1
    if state[5, 1, 0] == bottom:
        h = h + 1
    if state[5, 1, 2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0, 0, 0] != bottom or state[4, 2, 2] != state[4, 1, 1]\
            or state[1, 2, 0] != state[1, 1, 1]\
            or state[4, 1, 2] != state[4, 1, 1] or state[1, 1, 0] != state[1, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0, 0, 2] != bottom or state[1, 2, 2] != state[1, 1, 1]\
            or state[2, 2, 0] != state[2, 1, 1]\
            or state[1, 1, 2] != state[1, 1, 1] or state[2, 1, 0] != state[2, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 2] != bottom or state[2, 2, 2] != state[2, 1, 1]\
            or state[3, 2, 0] != state[3, 1, 1]\
            or state[2, 1, 2] != state[2, 1, 1] or state[3, 1, 0] != state[3, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 0] != bottom or state[3, 2, 2] != state[3, 1, 1]\
            or state[4, 2, 0] != state[4, 1, 1]\
            or state[3, 1, 2] != state[3, 1, 1] or state[4, 1, 0] != state[4, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (bad_corners == 4):
        h = h + 3
    elif (bad_corners == 3):
        h = h + 2
    elif (bad_corners == 2):
        h = h + 1
    return h            
 

def h_layer1_4(node):
    h = 0
    state = node.state.state
    bottom = state[0, 1, 1]
    
    # white cross perfect
    if state[1, 2, 1] != state[1, 1, 1] or state[0, 0, 1] != bottom:
        h = h + 1
    if state[2, 2, 1] != state[2, 1, 1] or state[0, 1, 2] != bottom:
        h = h + 1
    if state[3, 2, 1] != state[3, 1, 1] or state[0, 2, 1] != bottom:
        h = h + 1
    if state[4, 2, 1] != state[4, 1, 1] or state[0, 1, 0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5, 0, 1] == bottom:
        h = h + 1 
    if state[5, 2, 1] == bottom:
        h = h + 1
    if state[5, 1, 0] == bottom:
        h = h + 1
    if state[5, 1, 2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0, 0, 0] != bottom or state[4, 2, 2] != state[4, 1, 1]\
            or state[1, 2, 0] != state[1, 1, 1]\
            or state[4, 1, 2] != state[4, 1, 1] or state[1, 1, 0] != state[1, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0, 0, 2] != bottom or state[1, 2, 2] != state[1, 1, 1]\
            or state[2, 2, 0] != state[2, 1, 1]\
            or state[1, 1, 2] != state[1, 1, 1] or state[2, 1, 0] != state[2, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 2] != bottom or state[2, 2, 2] != state[2, 1, 1]\
            or state[3, 2, 0] != state[3, 1, 1]\
            or state[2, 1, 2] != state[2, 1, 1] or state[3, 1, 0] != state[3, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (state[0, 2, 0] != bottom or state[3, 2, 2] != state[3, 1, 1]\
            or state[4, 2, 0] != state[4, 1, 1]\
            or state[3, 1, 2] != state[3, 1, 1] or state[4, 1, 0] != state[4, 1, 1]
            ):
        bad_corners = bad_corners + 1
    if (bad_corners == 4):
        h = h + 4
    elif (bad_corners == 3):
        h = h + 3
    elif (bad_corners == 2):
        h = h + 2
    elif (bad_corners == 1):
        h = h + 1
    
    # top has white corners?
    if state[5, 0, 2] == bottom:
        h = h + 1 
    if state[5, 2, 0] == bottom:
        h = h + 1
    if state[5, 0, 0] == bottom:
        h = h + 1
    if state[5, 2, 2] == bottom:
        h = h + 1   
    
    if state[1, 1, 0] == state[4, 1, 1] and state[4, 1, 2] == state[1, 1, 1]:
        h = h + 2
    
    return h



def main():
    start_state = solved_state
    
    # gen root and set to start puzzle
    cube = Cube(start_state)
    root = Node(cube, None, None)
    root.state.display_colors()
    
    cube2 = Cube(solved_state_ints)
    root2 = Node(cube2, None, None)

    # scramble puzzle
    root.state, scramble_seq = root.state.scramble()
    for move in scramble_seq:
        root2.state = root2.state.execute_action(move)

    root.state.display_colors()
    
    # root.state = root.state.execute_action('R').execute_action("L'").execute_action("L'").execute_action("U")
    
    start_time = time.time()
    cross_path = idas(root, h_cross)
    print(" ".join(scramble_seq), '\n')
    end_time = time.time() - start_time
    print(end_time)
    
    for move in cross_path:
        root.state = root.state.execute_action(move)
    print(" ".join(cross_path), "\n")
    root.state.display_colors()
    
    layer1_1_path = idas(root, h_layer1_1)
    for move in layer1_1_path:
        root.state = root.state.execute_action(move)
    print(" ".join(layer1_1_path), "\n")
    root.state.display_colors()
    
    layer1_2_path = idas(root, h_layer1_2)
    for move in layer1_2_path:
        root.state = root.state.execute_action(move)
    print(" ".join(layer1_2_path), "\n")    
    root.state.display_colors()
    
    layer1_3_path = idas(root, h_layer1_3)
    for move in layer1_3_path:
        root.state = root.state.execute_action(move)
    print(" ".join(layer1_3_path), "\n")
    root.state.display_colors()
    
    layer1_4_path = idas(root, h_layer1_4)
    for move in layer1_4_path:
        root.state = root.state.execute_action(move)
    print(" ".join(layer1_4_path), "\n")
    root.state.display_colors()
    
    
    
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
