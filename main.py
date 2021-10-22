"""
main.py
Main file for Rubik's Cube solver
"""

__author__ = "Tyler Limbach"

from math import sqrt as sqrt
import random
import time
from collections import deque

import cProfile
import pstats
from pstats import SortKey

import os
import sys

#random.seed(0)

# set python hash seed to 0 so hashes are consistent across runs
hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)
    
# color escape sequences for xterm-256color bgs
ORANGE_BG = "\033[48;5;208m  \033[0;0m"
YELLOW_BG = "\033[48;5;11m  \033[0;0m"
RED_BG = "\033[48;5;9m  \033[0;0m" # 1
GREEN_BG = "\033[48;5;10m  \033[0;0m" # 2
BLUE_BG = "\033[48;5;12m  \033[0;0m" # 21
WHITE_BG = "\033[48;5;254m  \033[0;0m"

# ACTIONS will be used a dictionary to quickly determine moves from strings
ACTIONS = {}

class Cube:
    def __init__(self, state):
        self.size = int(len(state[0]))
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
            output += "".join(self.state[5][i])
            output += "\n"
        for i in range(self.size):
            output += "".join(self.state[4][i])
            output += " "
            output += "".join(self.state[1][i])
            output += " "
            output += "".join(self.state[2][i])
            output += " "
            output += "".join(self.state[3][i])
            output += "\n"
        for i in range(self.size):
            output += " " * (self.size*4+2)
            output += "".join(self.state[0][i])
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
            output = " " * (self.size*2)
            print (output, end='')
            for color in self.state[0][i]:
                print(pick_color(color), end='')
            print()
        print(output)
        

    def execute_action(self, move):
        """simulates a turn of this cube

        Args:
            move (string): a string representing the face to turn 
                and the direction to turn:
                
                only 1 letter if clockwise.
                counterclockwise represented by a letter follow by a single quote '
                double turn is letter followed by a 2
                lower case letter is an outer layer + middle layer turned together
                lowercase x, y or z is a rotation about that axis
                
                - 12 normal moves (outer layer turns)
                - 6 center turns (middle layer turns)
                - 9 double turns (same consecutive move twice, 3 center 6 normal)
                - 12 joined turns (outer + middle layer together)
                - 6 rotations
                
                README contains detailed turn notation information
                
                examples: 
                    R -> clockwise turn of right face
                    U' -> counterclockwise turn of up face
                    M2 -> 2x turn of middle column on front face twice (direction doesn't matter)
                    d -> clockwise turn of down face + middle front row (same as 2 moves: D E)
                    x' -> counterclockwise rotation about x axis (turn the whole cube like an R' move)

        Returns:
            Cube: the new cube after the turn
        """
        new_state = deepcopy(self.state)        
        max_idx = self.size - 1
        
        # outer moves
        if move == "R":
            new_state[2] = rot90(new_state[2])
            for i in range(self.size):
                new_state[5][i][max_idx], new_state[1][i][max_idx], \
                    new_state[0][i][max_idx], new_state[3][max_idx - i][0] = \
                    new_state[1][i][max_idx], new_state[0][i][max_idx], \
                    new_state[3][max_idx - i][0], new_state[5][i][max_idx]
        elif move == "R'":
            new_state[2] = rot270(new_state[2])
            for i in range(self.size):
                new_state[1][i][max_idx], new_state[0][i][max_idx], \
                    new_state[3][max_idx - i][0], new_state[5][i][max_idx] = \
                    new_state[5][i][max_idx], new_state[1][i][max_idx], \
                    new_state[0][i][max_idx], new_state[3][max_idx - i][0]
        elif move == "L":
            new_state[4] = rot90(new_state[4])
            for i in range(self.size):
                new_state[1][i][0], new_state[0][i][0], new_state[3][max_idx - i][max_idx], new_state[5][i][0] = \
                    new_state[5][i][0], new_state[1][i][0], new_state[0][i][0], new_state[3][max_idx - i][max_idx]
        elif move == "L'":
            new_state[4] = rot270(new_state[4])            
            for i in range(self.size):            
                new_state[5][i][0], new_state[1][i][0], new_state[0][i][0], new_state[3][max_idx - i][max_idx] = \
                    new_state[1][i][0], new_state[0][i][0], new_state[3][max_idx - i][max_idx], new_state[5][i][0]
        elif move == "U":
            new_state[5] = rot90(new_state[5])
            for i in range(self.size):
                new_state[1][0][i], new_state[2][0][i], new_state[3][0][i], new_state[4][0][i] = \
                    new_state[2][0][i], new_state[3][0][i], new_state[4][0][i], new_state[1][0][i]
        elif move == "U'":
            new_state[5] = rot270(new_state[5])
            for i in range(self.size):
                new_state[2][0][i], new_state[3][0][i], new_state[4][0][i], new_state[1][0][i] = \
                    new_state[1][0][i], new_state[2][0][i], new_state[3][0][i], new_state[4][0][i]
        elif move == "D":
            new_state[0] = rot90(new_state[0])            
            for i in range(self.size):
                new_state[1][max_idx][i], new_state[2][max_idx][i], new_state[3][max_idx][i], new_state[4][max_idx][i] = \
                    new_state[4][max_idx][i], new_state[1][max_idx][i], new_state[2][max_idx][i], new_state[3][max_idx][i]           
        elif move == "D'":
            new_state[0] = rot270(new_state[0])        
            for i in range(self.size):
                new_state[4][max_idx][i], new_state[1][max_idx][i], new_state[2][max_idx][i], new_state[3][max_idx][i] = \
                    new_state[1][max_idx][i], new_state[2][max_idx][i], new_state[3][max_idx][i], new_state[4][max_idx][i]
        elif move == "F":
            new_state[1] = rot90(new_state[1])
            displacedR = new_state[2][0][0]
            displacedL = new_state[4][0][max_idx]
            for i in range(self.size):
                new_state[5][max_idx][i], new_state[2][i][0], new_state[0][0][i], new_state[4][i][max_idx] = \
                    new_state[4][max_idx - i][max_idx], new_state[5][max_idx][i], new_state[2][max_idx - i][0], new_state[0][0][i]
            new_state[5][max_idx][max_idx] = displacedL
            new_state[0][0][max_idx] = displacedR
        elif move == "F'":
            new_state[1] = rot270(new_state[1]) 
            displacedR = new_state[2][max_idx][0]
            displacedL = new_state[4][max_idx][max_idx]
            for i in range(self.size):
                new_state[4][max_idx - i][max_idx], new_state[5][max_idx][i], new_state[2][max_idx - i][0], new_state[0][0][i] = \
                    new_state[5][max_idx][i], new_state[2][i][0], new_state[0][0][i], new_state[4][i][max_idx]
            new_state[5][max_idx][max_idx] = displacedR
            new_state[0][0][max_idx] = displacedL
        elif move == "B":
            new_state[3] = rot90(new_state[3])
            displacedR = new_state[2][max_idx][max_idx]
            displacedL = new_state[4][max_idx][0]
            for i in range(self.size):
                new_state[4][max_idx - i][0], new_state[5][0][i], new_state[2][max_idx - i][max_idx], new_state[0][max_idx][i] = \
                    new_state[5][0][i], new_state[2][i][max_idx], new_state[0][max_idx][i], new_state[4][i][0]
            new_state[5][0][max_idx] = displacedR
            new_state[0][max_idx][max_idx] = displacedL
        elif move == "B'":
            new_state[3] = rot270(new_state[3])
            displacedR = new_state[2][0][max_idx]
            displacedL = new_state[4][0][0]
            for i in range(self.size):
                new_state[5][0][i], new_state[2][i][max_idx], new_state[0][max_idx][i], new_state[4][i][0] = \
                    new_state[4][max_idx - i][0], new_state[5][0][i], new_state[2][max_idx - i][max_idx], new_state[0][max_idx][i]
            new_state[5][0][max_idx] = displacedL
            new_state[0][max_idx][max_idx] = displacedR     
            
        # center moves
        elif move == "M":
            for i in range(self.size):
                new_state[1][i][max_idx - 1], new_state[0][i][max_idx - 1], \
                    new_state[3][max_idx - i][1], new_state[5][i][max_idx - 1] = \
                    new_state[5][i][max_idx - 1], new_state[1][i][max_idx - 1], \
                    new_state[0][i][max_idx - 1], new_state[3][max_idx - i][1]        
        elif move == "M'":
            for i in range(self.size):
                new_state[5][i][max_idx - 1], new_state[1][i][max_idx - 1], \
                    new_state[0][i][max_idx - 1], new_state[3][max_idx - i][1] = \
                    new_state[1][i][max_idx - 1], new_state[0][i][max_idx - 1], \
                    new_state[3][max_idx - i][1], new_state[5][i][max_idx - 1] 
        elif move == "E":
            for i in range(self.size):
                new_state[1][max_idx - 1][i], new_state[2][max_idx - 1][i], new_state[3][max_idx - 1][i], new_state[4][max_idx - 1][i] = \
                    new_state[4][max_idx - 1][i], new_state[1][max_idx - 1][i], new_state[2][max_idx - 1][i], new_state[3][max_idx - 1][i]     
        elif move == "E'":
            for i in range(self.size):
                new_state[4][max_idx - 1][i], new_state[1][max_idx - 1][i], new_state[2][max_idx - 1][i], new_state[3][max_idx - 1][i] = \
                    new_state[1][max_idx - 1][i], new_state[2][max_idx - 1][i], new_state[3][max_idx - 1][i], new_state[4][max_idx - 1][i]
        elif move == "S":
            displacedR = new_state[2][0][1]
            displacedL = new_state[4][0][max_idx - 1]
            for i in range(self.size):
                new_state[5][max_idx - 1][i], new_state[2][i][1], new_state[0][1][i], new_state[4][i][max_idx - 1] = \
                    new_state[4][max_idx - i][max_idx - 1], new_state[5][max_idx - 1][i], new_state[2][max_idx - i][1], new_state[0][1][i]
            new_state[5][max_idx - 1][max_idx] = displacedL
            new_state[0][1][max_idx] = displacedR
        elif move == "S'":
            displacedR = new_state[2][max_idx][1]
            displacedL = new_state[4][max_idx][max_idx - 1]
            for i in range(self.size):
                new_state[4][max_idx - i][max_idx - 1], new_state[5][max_idx - 1][i], new_state[2][max_idx - i][1], new_state[0][1][i] = \
                    new_state[5][max_idx - 1][i], new_state[2][i][1], new_state[0][1][i], new_state[4][i][max_idx - 1]
            new_state[5][max_idx - 1][max_idx] = displacedR
            new_state[0][1][max_idx] = displacedL
        
        # double moves
        elif move == "R2":
            cube = self.execute_action("R")
            cube = cube.execute_action("R")
            return cube
        elif move == "L2":
            cube = self.execute_action("L")
            cube = cube.execute_action("L")
            return cube
        elif move == "U2":
            cube = self.execute_action("U")
            cube = cube.execute_action("U")
            return cube
        elif move == "D2":
            cube = self.execute_action("D")
            cube = cube.execute_action("D")
            return cube
        elif move == "F2":
            cube = self.execute_action("F")
            cube = cube.execute_action("F")
            return cube
        elif move == "B2":
            cube = self.execute_action("B")
            cube = cube.execute_action("B")
            return cube
        elif move == "M2":
            cube = self.execute_action("M")
            cube = cube.execute_action("M")
            return cube
        elif move == "E2":
            cube = self.execute_action("E")
            cube = cube.execute_action("E")
            return cube
        elif move == "S2":
            cube = self.execute_action("S")
            cube = cube.execute_action("S")
            return cube
        
        # 2 layers move at sime time (center + outer)
        elif move == "r":
            cube = self.execute_action("R")
            cube = cube.execute_action("M'")
            return cube
        elif move == "r'":
            cube = self.execute_action("R'")
            cube = cube.execute_action("M")
            return cube
        elif move == "l":
            cube = self.execute_action("L")
            cube = cube.execute_action("M")
            return cube
        elif move == "l'":
            cube = self.execute_action("L'")
            cube = cube.execute_action("M'")
            return cube
        elif move == "u":
            cube = self.execute_action("U")
            cube = cube.execute_action("E'")
            return cube
        elif move == "u'":
            cube = self.execute_action("U'")
            cube = cube.execute_action("E")
            return cube
        elif move == "d":
            cube = self.execute_action("D")
            cube = cube.execute_action("E")
            return cube
        elif move == "d'":
            cube = self.execute_action("D'")
            cube = cube.execute_action("E'")
            return cube
        elif move == "f":
            cube = self.execute_action("F")
            cube = cube.execute_action("S")
            return cube
        elif move == "f'":
            cube = self.execute_action("F'")
            cube = cube.execute_action("S'")
            return cube
        elif move == "b":
            cube = self.execute_action("B")
            cube = cube.execute_action("S'")
            return cube
        elif move == "b'":
            cube = self.execute_action("B'")
            cube = cube.execute_action("S")
            return cube                     
        
        # double joint moves
        elif move == "r2":
            cube = self.execute_action("r")
            cube = cube.execute_action("r")
            return cube
        elif move == "l2":
            cube = self.execute_action("l")
            cube = cube.execute_action("l")
            return cube
        elif move == "u2":
            cube = self.execute_action("u")
            cube = cube.execute_action("u")
            return cube
        elif move == "d2":
            cube = self.execute_action("d")
            cube = cube.execute_action("d")
            return cube
        elif move == "f2":
            cube = self.execute_action("f")
            cube = cube.execute_action("f")
            return cube
        elif move == "b2":
            cube = self.execute_action("b")
            cube = cube.execute_action("b")
            return cube           
        
        # cube rotations
        elif move == "x":
            cube = self.execute_action("r")
            cube = cube.execute_action("L'")
            return cube
        elif move == "x'":
            cube = self.execute_action("r'")
            cube = cube.execute_action("L")
            return cube
        elif move == "y":
            cube = self.execute_action("u")
            cube = cube.execute_action("D'")
            return cube
        elif move == "y'":
            cube = self.execute_action("u'")
            cube = cube.execute_action("D")
            return cube
        elif move == "z":
            cube = self.execute_action("f")
            cube = cube.execute_action("B'")
            return cube
        elif move == "z'":
            cube = self.execute_action("f'")
            cube = cube.execute_action("B")
            return cube                                        
        
        return Cube(new_state)
    
    
    def execute_action_sequence(self, actions):
        new_state = deepcopy(self.state)
        
        cube = Cube(new_state)
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
    

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.state)


    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.state == other.state.state

    
    def __ne__(self, other):   
        return not self.__eq__(other)     


    def __hash__(self):
        return hash(str(self.state.state))
        

def deepcopy(state):
    return [[[x for x in y] for y in z] for z in state]


def get_children(parent_node):
    children = []
    actions = ["R", "R'", "U", "U'", "F", "F'", "L", "L'", "D", "D'", "B", "B'"]
    
    # this entire if block is pruning moves
    if parent_node.parent is not None:
        if parent_node.action == parent_node.parent.action:
            actions.remove(parent_node.action)
        if len(parent_node.action) == 2:
            actions.remove(parent_node.action[0])
            actions.remove(parent_node.action)
        else:
            actions.remove(parent_node.action[0] + "'")    

    
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        child_node = Node(child_state, parent_node, action)
        children.append(child_node)
    return children


def string_to_state(string):
    state_1d = list(string.split(' '))
    size = int(sqrt(len(state_1d) // 6))
    state_3d = []
    for i in range(6):
        state_3d.append([])
        for j in range(size):
            state_3d[i].append([])
        for j in range(size*size):
            state_3d[i][j // size].append(state_1d[i*size*size + j])
            
    #state_3d = print(tuple(tuple(tuple(x) for x in y) for y in state_3d))
    return state_3d


def pick_color(char):
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


def rot90(arr):
    rotated = zip(*arr[::-1])
    return list([list(elem) for elem in rotated])

    
def rot270(arr):
    rotated = zip(*arr)
    return list([list(elem) for elem in rotated][::-1])
       

def astar(root_node, h_func):
    frontier = [root_node]
    seen = set()
    f_scores = [h_func(root_node)]
    while len(frontier) > 0:
        min_idx = f_scores.index(min(f_scores))
        cur_node = frontier.pop(min_idx)
        f_scores.pop(min_idx)
        seen.add(cur_node)
        #cur_node.state.display_colors()
        #print(find_path(cur_node))
        if h_func(cur_node) == 0:
            path = find_path(cur_node)
            return path
        for child in get_children(cur_node):
            if child in seen:
                continue
            elif child not in frontier:
                frontier.append(child)
                f_scores.append(h_func(child) + cost(root_node, child))

            #else:
                #same_node = frontier[frontier.index(child)]
                #if cost(root_node, child) < cost(root_node, same_node):
                #    same_node.parent = child.parent   
                    
        
def idas(root_node, h_func):
    bound = h_func(root_node)
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
   
   
def idas_repeat(root_node, h_func):
    bound = h_func(root_node)
    path = [root_node]
    paths = [[],[]]
    g = 0
    while len(paths) < 84:
        t = idas_repeat_search(path, g, bound, h_func, paths)
        if t == "FOUND":
            path_taken = find_path(path[-1])
            paths[0].append(path[-1])
            paths[1].append(path_taken)
            print(path_taken)
            path[-1].state.display_colors()
            # g = len(paths[1][-1]) * 8
            path = [root_node]
        elif t == float('inf'):
            return False  # not found
        else:
            bound = t   # increase bound to lowest neighbor's f


def idas_search(path, g, bound, h_func):
    node = path[-1]
    f = h_func(node) + g
    #time.sleep(1)
    #node.state.display_colors()
    #print(find_path(node))
    #print(h_func(node))
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


def idas_repeat_search(path, g, bound, h_func, paths):
    node = path[-1]
    f = h_func(node) + g
    #time.sleep(1)
    #node.state.display_colors()
    #print(find_path(node))
    #print(h_func(node))
    if h_func(node) == 0 and node not in paths[0]:  # if reached goal state
        return "FOUND"
    if f > bound:  # if we are over the ids bound
        return f
    minimum = float('inf')
    for child in get_children(node):  # for each child of this node
        if child not in path:
            path.append(child)
            t = idas_repeat_search(path, g + 1, bound, h_func, paths)
            if t == "FOUND":  # if reached goal state
                return "FOUND"
            if t < minimum:  # if we have a new bound < inf
                minimum = t
            path.pop()
    return minimum


def bfs(root_node, goal_func):
    frontier = deque([root_node])
    explored = set()
    paths = []
    while len(frontier) > 0 or len(paths) < 72:
        cur_node = frontier.popleft()
        explored.add(cur_node)
        #print(find_path(cur_node))
        if goal_func(cur_node) == 0:
            path = find_path(cur_node)
            # return path
            paths.append(path)
            print(path)
            cur_node.state.display_colors()
        for child in get_children(cur_node):
            if child in explored:
                continue
            else:
                frontier.append(child)
    print("frontier empty")	
    return paths
    #return False


def h_cross(node):
    h = 0
    state = node.state.state
    bottom = state[0][1][1]
    
    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h = h + 1 
    if state[5][2][1] == bottom:
        h = h + 1
    if state[5][1][0] == bottom:
        h = h + 1
    if state[5][1][2] == bottom:
        h = h + 1
        
    return h 


def h_layer1_1(node):
    h = 0
    state = node.state.state
    bottom = state[0][1][1]
    
    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h = h + 1 
    if state[5][2][1] == bottom:
        h = h + 1
    if state[5][1][0] == bottom:
        h = h + 1
    if state[5][1][2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != state[4][1][1]\
            or state[1][2][0] != state[1][1][1]\
            or state[4][1][2] != state[4][1][1] or state[1][1][0] != state[1][1][1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0][0][2] != bottom or state[1][2][2] != state[1][1][1]\
            or state[2][2][0] != state[2][1][1]\
            or state[1][1][2] != state[1][1][1] or state[2][1][0] != state[2][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][2] != bottom or state[2][2][2] != state[2][1][1]\
            or state[3][2][0] != state[3][1][1]\
            or state[2][1][2] != state[2][1][1] or state[3][1][0] != state[3][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][0] != bottom or state[3][2][2] != state[3][1][1]\
            or state[4][2][0] != state[4][1][1]\
            or state[3][1][2] != state[3][1][1] or state[4][1][0] != state[4][1][1]
            ):
        bad_corners = bad_corners + 1
    if (bad_corners == 4):
        h = h + 1
    return h 
    
    
def h_layer1_2(node):
    h = 0
    state = node.state.state
    bottom = state[0][1][1]
    
    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h = h + 1 
    if state[5][2][1] == bottom:
        h = h + 1
    if state[5][1][0] == bottom:
        h = h + 1
    if state[5][1][2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != state[4][1][1]\
            or state[1][2][0] != state[1][1][1]\
            or state[4][1][2] != state[4][1][1] or state[1][1][0] != state[1][1][1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0][0][2] != bottom or state[1][2][2] != state[1][1][1]\
            or state[2][2][0] != state[2][1][1]\
            or state[1][1][2] != state[1][1][1] or state[2][1][0] != state[2][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][2] != bottom or state[2][2][2] != state[2][1][1]\
            or state[3][2][0] != state[3][1][1]\
            or state[2][1][2] != state[2][1][1] or state[3][1][0] != state[3][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][0] != bottom or state[3][2][2] != state[3][1][1]\
            or state[4][2][0] != state[4][1][1]\
            or state[3][1][2] != state[3][1][1] or state[4][1][0] != state[4][1][1]
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
    bottom = state[0][1][1]
    
    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h = h + 1 
    if state[5][2][1] == bottom:
        h = h + 1
    if state[5][1][0] == bottom:
        h = h + 1
    if state[5][1][2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != state[4][1][1]\
            or state[1][2][0] != state[1][1][1]\
            or state[4][1][2] != state[4][1][1] or state[1][1][0] != state[1][1][1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0][0][2] != bottom or state[1][2][2] != state[1][1][1]\
            or state[2][2][0] != state[2][1][1]\
            or state[1][1][2] != state[1][1][1] or state[2][1][0] != state[2][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][2] != bottom or state[2][2][2] != state[2][1][1]\
            or state[3][2][0] != state[3][1][1]\
            or state[2][1][2] != state[2][1][1] or state[3][1][0] != state[3][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][0] != bottom or state[3][2][2] != state[3][1][1]\
            or state[4][2][0] != state[4][1][1]\
            or state[3][1][2] != state[3][1][1] or state[4][1][0] != state[4][1][1]
            ):
        bad_corners = bad_corners + 1
    if (bad_corners == 4):
        h = h + 3
    elif (bad_corners == 3):
        h = h + 2
    elif (bad_corners == 2):
        h = h + 1
    return h * 2
 

def h_layer1_4(node):
    h = 0
    state = node.state.state
    bottom = state[0][1][1]
    
    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h = h + 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h = h + 1 
    if state[5][2][1] == bottom:
        h = h + 1
    if state[5][1][0] == bottom:
        h = h + 1
    if state[5][1][2] == bottom:
        h = h + 1
    
    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != state[4][1][1]\
            or state[1][2][0] != state[1][1][1]\
            or state[4][1][2] != state[4][1][1] or state[1][1][0] != state[1][1][1]
            ):
        bad_corners = bad_corners + 1
    if  (state[0][0][2] != bottom or state[1][2][2] != state[1][1][1]\
            or state[2][2][0] != state[2][1][1]\
            or state[1][1][2] != state[1][1][1] or state[2][1][0] != state[2][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][2] != bottom or state[2][2][2] != state[2][1][1]\
            or state[3][2][0] != state[3][1][1]\
            or state[2][1][2] != state[2][1][1] or state[3][1][0] != state[3][1][1]
            ):
        bad_corners = bad_corners + 1
    if (state[0][2][0] != bottom or state[3][2][2] != state[3][1][1]\
            or state[4][2][0] != state[4][1][1]\
            or state[3][1][2] != state[3][1][1] or state[4][1][0] != state[4][1][1]
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
    if state[5][0][2] == bottom:
        h = h + 3 
    if state[5][2][0] == bottom:
        h = h + 3
    if state[5][0][0] == bottom:
        h = h + 3
    if state[5][2][2] == bottom:
        h = h + 3
    
    if state[1][1][0] == state[4][1][1] and state[4][1][2] == state[1][1][1]:
        h = h + 2
    
    return h * 2


def h_oll(node):
    h = 0
    state = node.state.state
    bottom = state[0][1][1]
    top = state[5][1][1]
    right = state[2][1][1]
    left = state[4][1][1]
    front = state[1][1][1]
    back = state[3][1][1]
    
    # bottom cross perfect
    if state[1][2][1] != front or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != right or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != back or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != left or state[0][1][0] != bottom:
        h = h + 1
    
    # bottom corners
    if (state[0][0][0] != bottom or state[4][2][2] != left\
            or state[1][2][0] != front\
            #or state[4][1][2] != left or state[1][1][0] != front
            ):
        h = h + 1
    if  (state[0][0][2] != bottom or state[1][2][2] != front\
            or state[2][2][0] != right\
            #or state[1][1][2] != front or state[2][1][0] != right
            ):
        h = h + 1
    if (state[0][2][2] != bottom or state[2][2][2] != right\
            or state[3][2][0] != back\
            #or state[2][1][2] != right or state[3][1][0] != back
            ):
        h = h + 1
    if (state[0][2][0] != bottom or state[3][2][2] != back\
            or state[4][2][0] != left\
            #or state[3][1][2] != back or state[4][1][0] != left
            ):
        h = h + 1
        
    # middle edges
    if state[4][1][2] != left or state[1][1][0] != front:
        h = h + 1  
    if state[1][1][2] != front or state[2][1][0] != right:
        h = h + 1    
    if state[2][1][2] != right or state[3][1][0] != back:
        h = h + 1    
    if state[3][1][2] != back or state[4][1][0] != left:
        h = h + 1
        
    # top cross kinda
    if state[5][0][1] != top:
        h = h + 1
    if state[5][1][2] != top:
        h = h + 1
    if state[5][2][1] != top:
        h = h + 1
    if state[5][1][0] != top:
        h = h + 1    
        
    # top corners 
    if (state[5][0][0] != top):
        h = h + 1
    if  (state[5][0][2] != top):
        h = h + 1
    if (state[5][2][2] != top):
        h = h + 1
    if (state[5][2][0] != top):
        h = h + 1

    return h * 2        
   
   
def h_pll(node):
    h = 0
    state = node.state.state
    bottom = state[0][1][1]
    top = state[5][1][1]
    right = state[2][1][1]
    left = state[4][1][1]
    front = state[1][1][1]
    back = state[3][1][1]
    
    # bottom cross perfect
    if state[1][2][1] != front or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != right or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != back or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != left or state[0][1][0] != bottom:
        h = h + 1
    
    # bottom corners
    if (state[0][0][0] != bottom or state[4][2][2] != left\
            or state[1][2][0] != front\
            #or state[4][1][2] != left or state[1][1][0] != front
            ):
        h = h + 1
    if  (state[0][0][2] != bottom or state[1][2][2] != front\
            or state[2][2][0] != right\
            #or state[1][1][2] != front or state[2][1][0] != right
            ):
        h = h + 1
    if (state[0][2][2] != bottom or state[2][2][2] != right\
            or state[3][2][0] != back\
            #or state[2][1][2] != right or state[3][1][0] != back
            ):
        h = h + 1
    if (state[0][2][0] != bottom or state[3][2][2] != back\
            or state[4][2][0] != left\
            #or state[3][1][2] != back or state[4][1][0] != left
            ):
        h = h + 1
        
    # middle edges
    if state[4][1][2] != left or state[1][1][0] != front:
        h = h + 1  
    if state[1][1][2] != front or state[2][1][0] != right:
        h = h + 1    
    if state[2][1][2] != right or state[3][1][0] != back:
        h = h + 1    
    if state[3][1][2] != back or state[4][1][0] != left:
        h = h + 1
        
    if state[1][2][1] != front or state[0][0][1] != bottom:
        h = h + 1
    if state[2][2][1] != right or state[0][1][2] != bottom:
        h = h + 1
    if state[3][2][1] != back or state[0][2][1] != bottom:
        h = h + 1
    if state[4][2][1] != left or state[0][1][0] != bottom:
        h = h + 1
        
        
    # top cross kinda
    if state[5][0][1] != top or state[1][0][1] != front:
        h = h + 1
    if state[5][1][2] != top or state[2][0][1] != right:
        h = h + 1
    if state[5][2][1] != top or state[3][0][1] != back:
        h = h + 1
    if state[5][1][0] != top or state[4][0][1] != left:
        h = h + 1    
        
    # top corners 
    if state[5][0][0] != top or state[3][0][2] != back \
        or state[4][0][0] != left:
        h = h + 1
    if  state[5][0][2] != top or state[3][0][0] != back \
        or state[2][0][2] != right:
        h = h + 1
    if state[5][2][2] != top or state[1][0][2] != front \
        or state[2][0][0] != right:
        h = h + 1
    if state[5][2][0] != top or state[4][0][2] != left \
        or state[1][0][0] != front:
        h = h + 1

    return h * 2


def goal_test_OLL(node):
    state = node.state.state
    
    bottom = state[0][1][1]
    top = state[5][1][1]
    right = state[2][1][1]
    left = state[4][1][1]
    front = state[1][1][1]
    back = state[3][1][1]
        
    # checks that everythin is solved besides last layer permutation
    return state[1][2][1] == front and state[0][0][1] == bottom and \
        state[2][2][1] == right and state[0][1][2] == bottom and \
        state[3][2][1] == back and state[0][2][1] == bottom and \
        state[4][2][1] == left and state[0][1][0] == bottom and \
        state[0][0][0] == bottom and state[4][2][2] == left and \
        state[1][2][0] == front and state[0][0][2] == bottom and \
        state[1][2][2] == front and state[2][2][0] == right and \
        state[0][2][2] == bottom and state[2][2][2] == right and \
        state[3][2][0] == back and state[0][2][0] == bottom and \
        state[3][2][2] == back and state[4][2][0] == left and \
        state[4][1][2] == left and state[1][1][0] == front and \
        state[1][1][2] == front and state[2][1][0] == right and \
        state[2][1][2] == right and state[3][1][0] == back and \
        state[3][1][2] == back and state[4][1][0] == left and \
        state[5][0][1] == top and state[5][1][2] == top and \
        state[5][2][1] == top and state[5][1][0] == top and \
        state[5][0][0] == top and state[5][0][2] == top and \
        state[5][2][2] == top and state[5][2][0] == top
    
    
def goal_test_solved(node):
    state = node.state.state
    
    bottom = state[0][1][1]
    top = state[5][1][1]
    right = state[2][1][1]
    left = state[4][1][1]
    front = state[1][1][1]
    back = state[3][1][1]
        
    # checks that everythin is solved besides last layer permutation
    return state[1][2][1] == front and state[0][0][1] == bottom and \
        state[2][2][1] == right and state[0][1][2] == bottom and \
        state[3][2][1] == back and state[0][2][1] == bottom and \
        state[4][2][1] == left and state[0][1][0] == bottom and \
        state[0][0][0] == bottom and state[4][2][2] == left and \
        state[1][2][0] == front and state[0][0][2] == bottom and \
        state[1][2][2] == front and state[2][2][0] == right and \
        state[0][2][2] == bottom and state[2][2][2] == right and \
        state[3][2][0] == back and state[0][2][0] == bottom and \
        state[3][2][2] == back and state[4][2][0] == left and \
        state[4][1][2] == left and state[1][1][0] == front and \
        state[1][1][2] == front and state[2][1][0] == right and \
        state[2][1][2] == right and state[3][1][0] == back and \
        state[3][1][2] == back and state[4][1][0] == left and \
        state[5][0][1] == top and state[5][1][2] == top and \
        state[5][2][1] == top and state[5][1][0] == top and \
        state[5][0][0] == top and state[5][0][2] == top and \
        state[5][2][2] == top and state[5][2][0] == top and \
        state[1][0][1] == front and state[2][0][1] == right and \
        state[3][0][1] == back and state[4][0][1] == left and \
        state[3][0][2] == back and state[4][0][0] == left and \
        state[3][0][0] == back and state[2][0][2] == right and \
        state[1][0][2] == front and state[2][0][0] == right and \
        state[4][0][2] == left and state[1][0][0] == front

    
def test_actions():
    cube = Cube(solved_state_ints)
    root = Node(cube, None, None)
    root.state.display_colors()
    
    # for action in ACTIONS:
    #     print("Solved:")
    #     root.state.display_colors()
    #     print(action, ":")
    #     root.state.execute_action(action).display_colors()
    
    root.state.execute_action("R").display_colors()
    root.state.execute_action("R'").display_colors()
    root.state.execute_action("L").display_colors()
    root.state.execute_action("L'").display_colors()
    root.state.execute_action("U").display_colors()
    root.state.execute_action("U'").display_colors()
    root.state.execute_action("D").display_colors()
    root.state.execute_action("D'").display_colors()
    root.state.execute_action("F").display_colors()
    root.state.execute_action("F'").display_colors()
    root.state.execute_action("B").display_colors()
    root.state.execute_action("B'").display_colors()
    
    root.state.execute_action("M").display_colors()
    root.state.execute_action("M'").display_colors()
    root.state.execute_action("E").display_colors()
    root.state.execute_action("E'").display_colors()
    root.state.execute_action("S").display_colors()
    root.state.execute_action("S'").display_colors()
    
    root.state.execute_action("r").display_colors()
    root.state.execute_action("r'").display_colors()
    root.state.execute_action("l").display_colors()
    root.state.execute_action("l'").display_colors()
    root.state.execute_action("u").display_colors()
    root.state.execute_action("u'").display_colors()
    root.state.execute_action("d").display_colors()
    root.state.execute_action("d'").display_colors()
    root.state.execute_action("f").display_colors()
    root.state.execute_action("f'").display_colors()
    root.state.execute_action("b").display_colors()
    root.state.execute_action("b'").display_colors()

    root.state.execute_action("x").display_colors()
    root.state.execute_action("x'").display_colors()
    root.state.execute_action("y").display_colors()
    root.state.execute_action("y'").display_colors()
    root.state.execute_action("z").display_colors()
    root.state.execute_action("z'").display_colors()


def test_alg_oll(node, alg):
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_OLL(test_node):
        return alg
    alg.insert(0, "U")
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_OLL(test_node):
        return alg
    alg[0] = "U'"
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_OLL(test_node):
        return alg
    alg[0] = "U2"
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_OLL(test_node):
        return alg
    
    return False
    

def solve_oll(node):
    try:
        with open("oll.txt", 'r') as f:
            lines = f.read().splitlines()
            #lines = [l.split(',') for l in lines]
            for l in lines:
                result = test_alg_oll(node, l.split())
                if result != False:
                    f.close()
                    return result
            return False
    except IOError:
        print("There was an error reading oll.txt.")
        exit()
        
        
def test_alg_pll(node, alg):
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.state.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.state.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.state.execute_action("U2"), None, None)):
        return alg + ["U2"]        
    
    alg.insert(0, "U")
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.state.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.state.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.state.execute_action("U2"), None, None)):
        return alg + ["U2"]
    
    alg[0] = "U2"
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.state.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.state.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.state.execute_action("U2"), None, None)):
        return alg + ["U2"]      
    
    alg[0] = "U'"
    test_node = Node(node.state.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.state.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.state.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.state.execute_action("U2"), None, None)):
        return alg + ["U2"]  
    
    return False
        
def solve_pll(node):
    if goal_test_solved(node):
        return []
    try:
        with open("pll.txt", 'r') as f:
            lines = f.read().splitlines()
            #lines = [l.split(',') for l in lines]
            for l in lines:
                result = test_alg_pll(node, l.split())
                if result != False:
                    f.close()
                    return result
            return False
    except IOError:
        print("There was an error reading oll.txt.")
        exit()

#solved_state = string_to_state("W"+" W"*8+" G"*9+" O"*9+" B"*9 +" R"*9+" Y"*9)
solved_state_ints = string_to_state('0'+' 0'*8+" 1"*9+" 2"*9+" 3"*9 +" 4"*9+" 5"*9)
for i in range(6):
    for j in range(3):
        for k in range(3):
            solved_state_ints[i][j][k] = int(solved_state_ints[i][j][k])


def main():
    start_state = solved_state_ints
    scramble_seq = []
    
    # gen root and set to start puzzle
    cube = Cube(start_state)
    root = Node(cube, None, None)
    root.state.display_colors()
    
    start_time = time.time()

    # feed custom scramble
    # root.state = root.state.execute_action_sequence("F' U' U' B L' F' R D' B' L B' B' U' F' D' B R' B' D' R' L D F L' F")
    
    
    # scramble puzzle
    root.state, scramble_seq = root.state.scramble()
    print(" ".join(scramble_seq), '\n')
    
    
    root.state.display_colors()
    
    solve_sequence = []
    
    cross_path = idas(root, h_cross)
    end_time = time.time() - start_time
    print(end_time)
    for move in cross_path:
        root.state = root.state.execute_action(move)
    print(" ".join(cross_path), "\n")
    root.state.display_colors()
    solve_sequence.append(cross_path)

    layer1_1_path = idas(root, h_layer1_1)
    for move in layer1_1_path:
        root.state = root.state.execute_action(move)
    end_time = time.time() - start_time
    print(end_time)
    print(" ".join(layer1_1_path), "\n")
    root.state.display_colors()
    solve_sequence.append(layer1_1_path)
    
    layer1_2_path = idas(root, h_layer1_2)
    for move in layer1_2_path:
        root.state = root.state.execute_action(move)
    end_time = time.time() - start_time
    print(end_time)
    print(" ".join(layer1_2_path), "\n")    
    root.state.display_colors()
    solve_sequence.append(layer1_2_path)
    
    layer1_3_path = idas(root, h_layer1_3)
    for move in layer1_3_path:
        root.state = root.state.execute_action(move)
    end_time = time.time() - start_time
    print(end_time) 
    print(" ".join(layer1_3_path), "\n")
    root.state.display_colors()
    solve_sequence.append(layer1_3_path)
    
    layer1_4_path = idas(root, h_layer1_4)
    for move in layer1_4_path:
        root.state = root.state.execute_action(move)
    end_time = time.time() - start_time
    print(end_time)
    print(" ".join(layer1_4_path), "\n")
    root.state.display_colors()
    solve_sequence.append(layer1_4_path)

    oll_path = solve_oll(root)
    for move in oll_path:
        root.state = root.state.execute_action(move)
    end_time = time.time() - start_time
    print(end_time)
    print(" ".join(oll_path), "\n")
    root.state.display_colors()
    solve_sequence.append(oll_path)
    
    
    full_path = solve_pll(root)
    for move in full_path:
        root.state = root.state.execute_action(move)
    end_time = time.time() - start_time
    print(end_time)
    print(" ".join(full_path), "\n")
    root.state.display_colors()
    solve_sequence.append(full_path)
    
    print("\nScramble:    " + " ".join(scramble_seq) + "\n")
    solve_seq_str = " ".join([" ".join(x) for x in solve_sequence])
    print("Full solve: ", solve_seq_str)
    
    
if __name__ == '__main__':
    main()
    
    #cProfile.run('main()', 'restats')
    #p = pstats.Stats('restats')
    #p.strip_dirs().sort_stats(SortKey.TIME).print_stats()

