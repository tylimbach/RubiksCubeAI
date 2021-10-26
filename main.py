"""
main.py
Main script for Rubik's Cube Solver
"""

__author__ = "Tyler Limbach"

# moves includes all the functions that modify states.
from moves import ACTIONS

from math import sqrt as sqrt
import random
import time
from collections import deque
import os
import sys

## profiling imports
#import cProfile
#import pstats
#from pstats import SortKey

import os


def clear():
    os.system("clear")

# # profiling imports
# import cProfile
# import pstats
# from pstats import SortKey

# random.seed(1)

# # set python hash seed to 0 so hashes are consistent across runs
# hashseed = os.getenv('PYTHONHASHSEED')
# if not hashseed:
#     os.environ['PYTHONHASHSEED'] = '0'
#     os.execv(sys.executable, [sys.executable] + sys.argv)
    
# color escape sequences for xterm-256color bgs
ORANGE_BG = "\033[48;5;208m  \033[0;0m"
YELLOW_BG = "\033[48;5;11m  \033[0;0m"
RED_BG = "\033[48;5;9m  \033[0;0m" # 1
GREEN_BG = "\033[48;5;10m  \033[0;0m" # 2
BLUE_BG = "\033[48;5;12m  \033[0;0m" # 21
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
            output += " " * (self.size*3+1)
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
            output += " " * (self.size*3+1)
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
        
        
    def execute_action(self, action):
        """ simulates a turn or rotation of the cube
        
        moves.py contains the functions that modify the state in order to perform each action

        Args:
            action (string): string representation of the action to perform in 3x3 Rubiks notation
                example strings:
                R -> turn right face CW 1/4
                R' -> counterclockwise turn of right face
                x -> clockwise rotation around x axis
                
                see README.txt for more detailed notation
                ACTIONS is a dictionary that maps action to the correct function from moves.py

        Returns:
            Cube: a Cube reflecting the new state after the action is performed
        """
        state = deepcopy_state(self.state)        
        max_idx = self.size - 1
        
        ACTIONS[action](state, max_idx)  # update state by executing the matching function in ACTIONS dict
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
    

class Node:
    """ nodes holding a cube. used for expansion in search
    """
    def __init__(self, cube, parent, action):
        self.cube = cube
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.cube.state)


    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.cube.state == other.cube.state

    
    def __ne__(self, other):   
        return not self.__eq__(other)     


    def __hash__(self):
        return hash(str(self.cube.state))
        

def deepcopy_state(state):
    """performs a deepcopy on the a 3d list cube state

    Args:
        state (3d list): a cube state we want to copy
        
    Returns:
        3d list: a deep copy of state
    """
    return [[[x for x in y] for y in z] for z in state]


def get_children(parent_node):
    """expands a node by generating child nodes for all potential moves

    Args:
        parent_node (Node): node to expand from

    Returns:
        Node list: list of expanded nodes
    """
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
        child_state = parent_node.cube.execute_action(action)
        child_node = Node(child_state, parent_node, action)
        children.append(child_node)
    return children


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
        for j in range(size*size):
            state_3d[i][j // size].append(state_1d[i*size*size + j])
            
    #state_3d = print(tuple(tuple(tuple(x) for x in y) for y in state_3d))
    return state_3d


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


def find_path(node):
    """ find the path taken from the root node to here

    Args:
        node (Node): the child node at the end of the path

    Returns:
        string list: path taken from the root node to the child node as actions
    """
    path = []	
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path
                    
        
def idas(root_node, h_func):
    """ perform an IDA* search to find a path to a goal state

    Args:
        root_node (Node): the Node to start the search from
        h_func (function): a heuristic function

    Returns:
        string list: the path taken from root to solution as actions
        false: if no path found after expanding all possible nodes
    """
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
   

def idas_search(path, g, bound, h_func):
    """recursive function to perform the search in IDA*

    Args:
        path (list): a stack that keeps track of the action path taken from the root to here
        g (int): the cost it took to move from the root node to here
        bound (int): the fscore threshold for nodes we are expanding
        h_func (function): a heuristic function

    Returns:
        int/float or string: "FOUND" returned if we reached solution
                             "inf" returned if no solution
                             an fscore to update the bound if we have more nodes
    """
    node = path[-1]
    f = h_func(node) + g
    #time.sleep(1)
    #node.cube.display_colors()
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


def h_cross(node):
    h = 0
    state = node.cube.state
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
    state = node.cube.state
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
        h = h + 2
    if state[5][2][1] == bottom:
        h = h + 2
    if state[5][1][0] == bottom:
        h = h + 2
    if state[5][1][2] == bottom:
        h = h + 2
    
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
    state = node.cube.state
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
    state = node.cube.state
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
    state = node.cube.state
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
    
    return h*2     
   

def goal_test_oll(node):
    state = node.cube.state
    
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
    state = node.cube.state
    
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
    root.cube.display_colors()
    
    for action in ACTIONS:
        # print("Solved:")
        # root.cube.display_colors()
        print(action, ":")
        root.cube.execute_action(action).display_colors()


def test_alg_oll(node, alg):
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_oll(test_node):
        return alg
    alg.insert(0, "U")
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_oll(test_node):
        return alg
    alg[0] = "U'"
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_oll(test_node):
        return alg
    alg[0] = "U2"
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_oll(test_node):
        return alg
    
    return False
    

def solve_oll(node):
    if goal_test_oll(node):
        return []
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
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.cube.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.cube.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.cube.execute_action("U2"), None, None)):
        return alg + ["U2"]        
    
    alg.insert(0, "U")
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.cube.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.cube.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.cube.execute_action("U2"), None, None)):
        return alg + ["U2"]
    
    alg[0] = "U2"
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.cube.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.cube.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.cube.execute_action("U2"), None, None)):
        return alg + ["U2"]      
    
    alg[0] = "U'"
    test_node = Node(node.cube.execute_action_sequence(alg), None, None)
    if goal_test_solved(test_node):
        return alg
    elif goal_test_solved(Node(test_node.cube.execute_action("U"), None, None)):
        return alg + ["U"]
    elif goal_test_solved(Node(test_node.cube.execute_action("U'"), None, None)):
        return alg + ["U'"]    
    elif goal_test_solved(Node(test_node.cube.execute_action("U2"), None, None)):
        return alg + ["U2"]  
    
    return False


def solve_pll(node):
    if goal_test_solved(node):
        return []
    try:
        with open("pll.txt", 'r') as f:
            lines = f.read().splitlines()
            # lines = [l.split(',') for l in lines]
            for line in lines:
                result = test_alg_pll(node, line.split())
                if result:
                    f.close()
                    return result
            return False
    except IOError:
        print("There was an error reading oll.txt.")
        exit()


def solve(node):
    cross_path = idas(node, h_cross)
    node.cube = node.cube.execute_action_sequence(cross_path)

    f2l_path1 = idas(node, h_layer1_1)
    node.cube = node.cube.execute_action_sequence(f2l_path1)
    f2l_path2 = idas(node, h_layer1_2)
    node.cube = node.cube.execute_action_sequence(f2l_path2)
    f2l_path3 = idas(node, h_layer1_3)
    node.cube = node.cube.execute_action_sequence(f2l_path3)
    f2l_path4 = idas(node, h_layer1_4)
    node.cube = node.cube.execute_action_sequence(f2l_path4)

    oll_path = solve_oll(node)
    node.cube = node.cube.execute_action_sequence(oll_path)
    pll_path = solve_pll(node)
    node.cube = node.cube.execute_action_sequence(pll_path)

    solve_path = cross_path + f2l_path1 + f2l_path2 + f2l_path3 \
        + f2l_path4 + oll_path + pll_path

    return solve_path, node


def display_menu(node, scramble_sequence="", user_moves="",
                 solution_sequence="", time_taken="0.00", seed=""):
    clear()
    if seed is None:
        seed = ""
    print("Random seed       : ", seed)
    print("Current scramble  : ", " ".join(scramble_sequence))
    print("Move History      : ", " ".join(user_moves))
    print("Solution sequence :  ", end="")
    for idx, move in enumerate(solution_sequence):
        if idx % 25 == 0 and idx > 0:
            print()
            print("                     ", end="")
        print(move, end=" ")
    print()
    print()
    print("Time of last operation: %.2f seconds " % time_taken)
    print()

    node.cube.display_colors()

    print("1. Random Scramble")
    print("2. Enter Moves")
    print("3. Computer Solve")
    print("4. Set Random Seed")
    print("5. Remove Random Seed")

    # print()
    # print("6. Watch Solve (Work in progress)")

    print()
    print("Enter a number from above:  ", end="")


solved_state_ints = string_to_state('0'+' 0'*8+" 3"*9+" 4"*9+" 1"*9+" 2"*9+" 5"*9)

for i in range(6):
    for j in range(3):
        for k in range(3):
            solved_state_ints[i][j][k] = int(solved_state_ints[i][j][k])


def main():
    start_state = solved_state_ints
    scramble_sequence = []
    user_moves = []
    solution_sequence = []
    seed = None
    time_taken = 0.0

    # gen root and set to start puzzle
    cube = Cube(start_state)
    root = Node(cube, None, None)

    while True:
        display_menu(root, scramble_sequence, user_moves, solution_sequence, time_taken,
                     seed)
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

        command = input()
        start_time = time.process_time()

        if command == '1':
            root.cube, scramble_sequence = Node(Cube(start_state), None, None).cube.scramble()
            user_moves = []
        elif command == '2':
            print("Enter a space separated move sequence:  ", end="")
            raw_sequence = input()
            sequence = raw_sequence.split()
            root.cube = root.cube.execute_action_sequence(sequence)
            user_moves.extend(sequence)
        elif command == '3':
            print()
            print("Solving...")
            solution_sequence, root = solve(root)
        elif command == '4':
            print("Enter a seed integer: ", end="")
            seed = int(input())
        elif command == '5':
            seed = None

        # elif command == '6':
        #     print()
        #     print("Finding Solve Sequence...")
        #     solution_sequence, root = solve(root)

        command_list = command.split()
        if set(command_list).issubset(set(ACTIONS)):
            root.cube = root.cube.execute_action_sequence(command_list)
            user_moves.extend(command_list)

        end_time = time.process_time()
        time_taken = end_time - start_time


if __name__ == '__main__':
    main()
    
    # cProfile.run('main()', 'restats')
    # p = pstats.Stats('restats')
    # p.strip_dirs().sort_stats(SortKey.TIME).print_stats()

