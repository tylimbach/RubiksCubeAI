"""
menu.py
Module for I/O (a terminal menu application)
"""
import random
import time
import os

from .actions import ACTIONS_3x3
from .cube import solved_state_ints
from .cube import Cube
from .solver import Node
from .solver import solve_cfop


def clear():
    os.system("clear")


def menu_loop():
    """ Starts a menu loop that accepts commands and runs until the user quits
    """
    start_state = solved_state_ints
    scramble_sequence = []
    user_moves = []
    solution_sequence = []
    seed = None
    time_taken = 0.0
    help_toggle = False
    text_display_toggle = False

    # gen root and set to start puzzle
    solved_cube = Cube(start_state)
    root = Node(solved_cube, None, None)
    old_root = Node(solved_cube, None, None)

    while True:
        display_menu(old_root, root, scramble_sequence, user_moves, solution_sequence, time_taken,
                     seed, help_toggle, text_display_toggle)
        if seed is not None:
            random.seed(int(seed))
        else:
            random.seed()

        command = input()

        if command == "h" or command == "H" or command == "help":
            help_toggle = not help_toggle
            continue

        start_time = time.process_time()

        if command == '1':
            old_root = Node(solved_cube, None, None)
            root.cube, scramble_sequence = Node(Cube(start_state), None, None).cube.scramble()
            user_moves = []
            solution_sequence = []
        elif command == '2':
            old_root = Node(root.cube, None, None)
            print("Enter a space separated move sequence:  ", end="")
            raw_sequence = input()
            sequence = raw_sequence.split()
            root.cube = root.cube.execute_action_sequence(sequence)
            user_moves.extend(sequence)
        elif command == '3':
            old_root = Node(root.cube, None, None)
            print("Solving...")
            solution_sequence, root = solve_cfop(root)
        elif command == '4':
            print("Enter a seed integer:  ", end="")
            seed = int(input())
        elif command == '5':
            seed = None
        # elif command == '6':
        #     old_root = Node(root.cube, None, None)
        #     print("Solving...")
        #     solution_sequence, root = solve_kociemba(root)
        elif command == 'Q' or command == 'q':
            exit()
        elif command == 'T' or command == "t":
            text_display_toggle = not text_display_toggle
        command_list = command.split()
        if set(command_list).issubset(set(ACTIONS_3x3)):
            old_root = Node(root.cube, None, None)
            root.cube = root.cube.execute_action_sequence(command_list)
            user_moves.extend(command_list)

        end_time = time.process_time()
        time_taken = end_time - start_time


def display_menu(old_node, node, scramble_sequence="", user_moves="",
                 solution_sequence="", time_taken="0.00", seed="",
                 help_toggle=False, is_text_mode=False):
    """ Clear console and display the updated menu

    :param old_node: a Node containing the "previous" cube state
    :param node: a Node containing the "newest" cube state
    :param scramble_sequence: the sequence of the last scramble
    :param user_moves: the running sequence of moves input by the user
    :param solution_sequence: the solution sequence for old_node
    :param time_taken: cpu runtime of previous command
    :param seed: optional random seed integer
    :param help_toggle: boolean to toggle help menu for moves
    :param is_text_mode: boolean to toggle text vs color display mode
    """
    clear()
    if seed is None:
        seed = ""

    if help_toggle:
        moves = " ".join(ACTIONS_3x3)
        print("--------------- Move Options ----------------")
        print("Face/Slice Turns : R, L, U, D, F, B, M, E, S")
        print("Wide Turns       : r, l, u, d, f, b")
        print("Cube Rotations   : x, y, z")
        print()
        print("Inverse          : Add ' after a move")
        print("Double           : Add 2 after a move")
        # print("---------------------------------------------")

    print("----------------- Commands ------------------")
    print("1. Random Scramble")
    print("2. Enter Moves")
    print("3. CFOP Solve")
    print("4. Set Random Seed")
    print("5. Remove Random Seed")
    # print("6. Kociemba Solve")
    print()
    print("H. Toggle Move Help")
    print("T. Toggle Text Mode")
    print("Q. Quit")
    print("------------------ Before -------------------")
    if is_text_mode:
        old_node.cube.display_text()
    else:
        old_node.cube.display_colors()
    print("------------------ After --------------------")
    if is_text_mode:
        node.cube.display_text()
    else:
        node.cube.display_colors()
    print("------------------- Info --------------------")

    print("Random seed        : ", seed)
    print("Current scramble   : ", " ".join(scramble_sequence))
    print("Move History       : ", " ".join(user_moves))
    print("Solution sequence  :  ", end="")
    for idx, move in enumerate(solution_sequence):
        if idx % 25 == 0 and idx > 0:
            print()
            print("                      ", end="")
        print(move, end=" ")
    print()
    print("----------------- %.2f secs -----------------" % time_taken)
    print("Enter move(s) or command : ", end="")

