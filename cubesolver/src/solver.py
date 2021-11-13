"""
solver.py
Module related to solving algorithms and cube Node generation
"""

from cubesolver.src.cube import Cube
from cubesolver.src.cube import solved_state_ints
from cubesolver.src.cube import ACTIONS_3x3


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
            bound = t  # increase bound to lowest neighbor's f


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
    h = h_func(node)
    f = h + g

    if h == 0:  # if reached goal state
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
    """ Determine a heuristic for the bottom cross

    :param node: the Node to solve the cross for
    :return: a heuristic
    """
    h = 0
    state = node.cube.state
    bottom = state[0][1][1]

    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h += 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h += 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h += 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h += 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h += 1
    if state[5][2][1] == bottom:
        h += 1
    if state[5][1][0] == bottom:
        h += 1
    if state[5][1][2] == bottom:
        h += 1

    return h


def h_layer1_1(node):
    """ Determine a heuristic fo1st F2L pair

    :param node: the Node to solve F2L on
    :return: a heuristic
    """
    h = 0
    state = node.cube.state
    bottom = state[0][1][1]

    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h += 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h += 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h += 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h += 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h += 1
    if state[5][2][1] == bottom:
        h += 1
    if state[5][1][0] == bottom:
        h += 1
    if state[5][1][2] == bottom:
        h += 1

    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != state[4][1][1]
            or state[1][2][0] != state[1][1][1]
            or state[4][1][2] != state[4][1][1] or state[1][1][0] != state[1][1][1]):
        bad_corners = bad_corners + 1
    if (state[0][0][2] != bottom or state[1][2][2] != state[1][1][1]
            or state[2][2][0] != state[2][1][1]
            or state[1][1][2] != state[1][1][1] or state[2][1][0] != state[2][1][1]):
        bad_corners = bad_corners + 1
    if (state[0][2][2] != bottom or state[2][2][2] != state[2][1][1]
            or state[3][2][0] != state[3][1][1]
            or state[2][1][2] != state[2][1][1] or state[3][1][0] != state[3][1][1]):
        bad_corners = bad_corners + 1
    if (state[0][2][0] != bottom or state[3][2][2] != state[3][1][1]
            or state[4][2][0] != state[4][1][1]
            or state[3][1][2] != state[3][1][1] or state[4][1][0] != state[4][1][1]):
        bad_corners = bad_corners + 1
    if bad_corners == 4:
        h += 1
    return h


def h_layer1_2(node):
    """ Determine a heuristic fo2nd F2L pair

    :param node: the Node to solve F2L on
    :return: a heuristic
    """
    h = 0
    state = node.cube.state
    bottom = state[0][1][1]

    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h += 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h += 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h += 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h += 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h += 1
    if state[5][2][1] == bottom:
        h += 1
    if state[5][1][0] == bottom:
        h += 1
    if state[5][1][2] == bottom:
        h += 1

    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != state[4][1][1]
            or state[1][2][0] != state[1][1][1]
            or state[4][1][2] != state[4][1][1] or state[1][1][0] != state[1][1][1]
    ):
        bad_corners = bad_corners + 1
    if (state[0][0][2] != bottom or state[1][2][2] != state[1][1][1]
            or state[2][2][0] != state[2][1][1]
            or state[1][1][2] != state[1][1][1] or state[2][1][0] != state[2][1][1]
    ):
        bad_corners = bad_corners + 1
    if (state[0][2][2] != bottom or state[2][2][2] != state[2][1][1]
            or state[3][2][0] != state[3][1][1]
            or state[2][1][2] != state[2][1][1] or state[3][1][0] != state[3][1][1]
    ):
        bad_corners = bad_corners + 1
    if (state[0][2][0] != bottom or state[3][2][2] != state[3][1][1]
            or state[4][2][0] != state[4][1][1]
            or state[3][1][2] != state[3][1][1] or state[4][1][0] != state[4][1][1]
    ):
        bad_corners = bad_corners + 1
    if bad_corners == 4:
        h += 2
    elif bad_corners == 3:
        h += 1

    return h


def h_layer1_3(node):
    """ Determine a heuristic fo3rd F2L pair

    :param node: the Node to solve F2L on
    :return: a heuristic
    """
    h = 0
    state = node.cube.state
    bottom = state[0][1][1]

    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h += 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h += 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h += 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h += 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h += 1
    if state[5][2][1] == bottom:
        h += 1
    if state[5][1][0] == bottom:
        h += 1
    if state[5][1][2] == bottom:
        h += 1

    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != state[4][1][1]
            or state[1][2][0] != state[1][1][1]
            or state[4][1][2] != state[4][1][1] or state[1][1][0] != state[1][1][1]
    ):
        bad_corners = bad_corners + 1
    if (state[0][0][2] != bottom or state[1][2][2] != state[1][1][1]
            or state[2][2][0] != state[2][1][1]
            or state[1][1][2] != state[1][1][1] or state[2][1][0] != state[2][1][1]
    ):
        bad_corners = bad_corners + 1
    if (state[0][2][2] != bottom or state[2][2][2] != state[2][1][1]
            or state[3][2][0] != state[3][1][1]
            or state[2][1][2] != state[2][1][1] or state[3][1][0] != state[3][1][1]
    ):
        bad_corners = bad_corners + 1
    if (state[0][2][0] != bottom or state[3][2][2] != state[3][1][1]
            or state[4][2][0] != state[4][1][1]
            or state[3][1][2] != state[3][1][1] or state[4][1][0] != state[4][1][1]
    ):
        bad_corners = bad_corners + 1
    if bad_corners == 4:
        h += 3
    elif bad_corners == 3:
        h += 2
    elif bad_corners == 2:
        h += 1
    return h * 2


def h_layer1_4(node):
    """ Determine a heuristic fo4th (final) F2L pair

    :param node: the Node to solve F2L on
    :return: a heuristic
    """
    h = 0
    state = node.cube.state
    bottom = state[0][1][1]
    right = state[2][1][1]
    left = state[4][1][1]
    front = state[1][1][1]
    back = state[3][1][1]

    # white cross perfect
    if state[1][2][1] != state[1][1][1] or state[0][0][1] != bottom:
        h += 1
    if state[2][2][1] != state[2][1][1] or state[0][1][2] != bottom:
        h += 1
    if state[3][2][1] != state[3][1][1] or state[0][2][1] != bottom:
        h += 1
    if state[4][2][1] != state[4][1][1] or state[0][1][0] != bottom:
        h += 1

    # top has white edges?
    if state[5][0][1] == bottom:
        h += 1
    if state[5][2][1] == bottom:
        h += 1
    if state[5][1][0] == bottom:
        h += 1
    if state[5][1][2] == bottom:
        h += 1

    # 1 corner
    bad_corners = 0
    if (state[0][0][0] != bottom or state[4][2][2] != left
            or state[1][2][0] != front
            or state[4][1][2] != left or state[1][1][0] != front):
        h += 1
    if (state[0][0][2] != bottom or state[1][2][2] != front
            or state[2][2][0] != right
            or state[1][1][2] != front or state[2][1][0] != right):
        h += 1
    if (state[0][2][2] != bottom or state[2][2][2] != right
            or state[3][2][0] != back
            or state[2][1][2] != right or state[3][1][0] != back):
        h += 1
    if (state[0][2][0] != bottom or state[3][2][2] != back
            or state[4][2][0] != left
            or state[3][1][2] != back or state[4][1][0] != left):
        h += 1

    # top has bottom corners?
    if state[5][0][2] == bottom:
        h += 2
    if state[5][2][0] == bottom:
        h += 2
    if state[5][0][0] == bottom:
        h += 2
    if state[5][2][2] == bottom:
        h += 2

    # misoriented bottom corners
    if state[1][2][0] == bottom:
        h += 1
    if state[1][2][2] == bottom:
        h += 1
    if state[2][2][0] == bottom:
        h += 1
    if state[2][2][2] == bottom:
        h += 1
    if state[3][2][0] == bottom:
        h += 1
    if state[3][2][2] == bottom:
        h += 1
    if state[4][2][0] == bottom:
        h += 1
    if state[4][2][2] == bottom:
        h += 1

    # if state[1][1][0] == left and state[4][1][2] == bottom:
    #     h += 3
    # if state[1][1][2] == right and state[2][1][0] == bottom:
    #     h += 3
    # if state[2][1][2] == back and state[3][1][0] == right:
    #     h += 3
    # if state[3][1][2] == left and state[4][1][0] == back:
    #     h += 3

    return h * 2


def goal_test_oll(node):
    """ Test if node is solved at least through OLL

    :param node: the Node to test
    :return: True if solved, False if unsolved
    """
    state = node.cube.state

    bottom = state[0][1][1]
    top = state[5][1][1]
    right = state[2][1][1]
    left = state[4][1][1]
    front = state[1][1][1]
    back = state[3][1][1]

    # checks that everything is solved besides last layer permutation
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
    """ Test if node is as solved cube

    :param node: the Node to test
    :return: True if solved, False if unsolved
    """
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
    """ Function to display all actions for visual testing
    """
    cube = Cube(solved_state_ints)
    root = Node(cube, None, None)
    root.cube.display_colors()

    for action in ACTIONS_3x3:
        # print("Solved:")
        # root.cube.display_colors()
        print(action, ":")
        root.cube.execute_action(action).display_colors()


def test_alg_oll(node, alg):
    """ Determine if the given algorithm can solve OLL for the node.

    :param node: a Node containing the Cube before OLL
    :param alg: a list containing the base algorithm to test cases for
    :return: If the algorithm succeeds, the succeeding algorithm variant.
        Otherwise, False
    """
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
    """ Find an OLL sequence for the cube

    :param node: a Node for the cube state before OLL. should have F2L finished.
    :return: the algorithm that solves OLL
    """
    if goal_test_oll(node):
        return []
    try:
        with open("cubesolver/resources/oll.txt", 'r') as f:
            lines = f.read().splitlines()
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
    """ Determine if the given algorithm can solve PLL for the node.

    :param node: a Node containing the Cube before PLL
    :param alg: a list containing the base algorithm to test cases for
    :return: if the algorithm succeeds, the succeeding algorithm variant.
        otherwise, False
    """
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
    """ Find a PLL sequence for the cube

    :param node: a Node for the cube state before PLL. should have OLL finished.
    :return: the algorithm that solves PLL
    """
    if goal_test_solved(node):
        return []
    try:
        with open("cubesolver/resources/pll.txt", 'r') as f:
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


def solve_cfop(node):
    """ Find a solution sequence to the cube using CFOP method

    :param node: a Node for the initial cube state to solve
    :return: solve_path: the sequence that solves the cube
    :return: node: a Node for the newly solved cube
    """
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


def h_g1(node):
    h = 0

    state = node.cube.state
    bottom = state[0][1][1]
    top = state[5][1][1]
    right = state[2][1][1]
    left = state[4][1][1]

    # corner orientations
    if not (state[0][0][0] == bottom or state[0][0][0] == top):
        h += 1
    if not (state[0][2][0] == bottom or state[0][2][0] == top):
        h += 1
    if not (state[0][0][2] == bottom or state[0][0][2] == top):
        h += 1
    if not (state[0][2][2] == bottom or state[0][2][2] == top):
        h += 1
    if not (state[5][0][0] == bottom or state[5][0][0] == top):
        h += 1
    if not (state[5][2][0] == bottom or state[5][2][0] == top):
        h += 1
    if not (state[5][0][2] == bottom or state[5][0][2] == top):
        h += 1
    if not (state[5][2][2] == bottom or state[5][2][2] == top):
        h += 1

    # edge orientation
    if not (state[0][0][1] == bottom or state[0][0][1] == top):
        h += 1
    if not (state[0][1][0] == bottom or state[0][1][0] == top):
        h += 1
    if not (state[0][1][2] == bottom or state[0][1][2] == top):
        h += 1
    if not (state[0][2][1] == bottom or state[0][2][1] == top):
        h += 1
    if not (state[5][0][1] == bottom or state[5][0][1] == top):
        h += 1
    if not (state[5][1][0] == bottom or state[5][1][0] == top):
        h += 1
    if not (state[5][1][2] == bottom or state[5][1][2] == top):
        h += 1
    if not (state[5][2][1] == bottom or state[5][2][1] == top):
        h += 1

    # middle edges orientation and middle layer
    # if not (state[2][0][1] == right or state[2][0][1] == left):
    #     h += 1
    if not (state[2][1][0] == right or state[2][1][0] == left):
        h += 1
    if not (state[2][1][2] == right or state[2][1][2] == left):
        h += 1
    # if not (state[2][2][1] == right or state[2][2][1] == left):
    #     h += 1
    # if not (state[4][0][1] == right or state[4][0][1] == left):
    #     h += 1
    if not (state[4][1][0] == right or state[4][1][0] == left):
        h += 1
    if not (state[4][1][2] == right or state[4][1][2] == left):
        h += 1
    # if not (state[4][2][1] == right or state[4][2][1] == left):
    #     h += 1

    return h * 2


def solve_kociemba(node):
    g1_path = idas(node, h_g1)
    node.cube = node.cube.execute_action_sequence(g1_path)

    solve_path = g1_path
    return solve_path, node

