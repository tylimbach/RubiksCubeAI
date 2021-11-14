"""
actions.py
Module for manipulating Cube states (executing actions)
"""


def rot90(arr):
    """ rotate the 3d list 90 degrees clockwise

    :param arr: the 3d list to rotate
    :return: a rotated version of the 3d list
    """
    rotated = zip(*arr[::-1])
    return list([list(elem) for elem in rotated])


def rot270(arr):
    """ rotate the 3d list 270 degrees clockwise

    :param arr: the 3d list to rotate
    :return: a rotated version of the 3d list
    """
    rotated = zip(*arr)
    return list([list(elem) for elem in rotated][::-1])


def turn_r(state, max_idx):
    state[2] = rot90(state[2])
    for i in range(max_idx + 1):
        state[5][i][max_idx], state[1][i][max_idx], \
            state[0][i][max_idx], state[3][max_idx - i][0] = \
            state[1][i][max_idx], state[0][i][max_idx], \
            state[3][max_idx - i][0], state[5][i][max_idx]


def turn_ri(state, max_idx):
    state[2] = rot270(state[2])
    for i in range(max_idx + 1):
        state[1][i][max_idx], state[0][i][max_idx], \
            state[3][max_idx - i][0], state[5][i][max_idx] = \
            state[5][i][max_idx], state[1][i][max_idx], \
            state[0][i][max_idx], state[3][max_idx - i][0]


def turn_l(state, max_idx):
    state[4] = rot90(state[4])
    for i in range(max_idx + 1):
        state[1][i][0], state[0][i][0], state[3][max_idx - i][max_idx], state[5][i][0] = \
            state[5][i][0], state[1][i][0], state[0][i][0], state[3][max_idx - i][max_idx]


def turn_li(state, max_idx):
    state[4] = rot270(state[4])
    for i in range(max_idx + 1):            
        state[5][i][0], state[1][i][0], state[0][i][0], state[3][max_idx - i][max_idx] = \
            state[1][i][0], state[0][i][0], state[3][max_idx - i][max_idx], state[5][i][0]


def turn_u(state, max_idx):
    state[5] = rot90(state[5])
    for i in range(max_idx + 1):
        state[1][0][i], state[2][0][i], state[3][0][i], state[4][0][i] = \
            state[2][0][i], state[3][0][i], state[4][0][i], state[1][0][i]


def turn_ui(state, max_idx):
    state[5] = rot270(state[5])
    for i in range(max_idx + 1):
        state[2][0][i], state[3][0][i], state[4][0][i], state[1][0][i] = \
            state[1][0][i], state[2][0][i], state[3][0][i], state[4][0][i]


def turn_d(state, max_idx):
    state[0] = rot90(state[0])            
    for i in range(max_idx + 1):
        state[1][max_idx][i], state[2][max_idx][i], state[3][max_idx][i], state[4][max_idx][i] = \
            state[4][max_idx][i], state[1][max_idx][i], state[2][max_idx][i], state[3][max_idx][i]           


def turn_di(state, max_idx):
    state[0] = rot270(state[0])        
    for i in range(max_idx + 1):
        state[4][max_idx][i], state[1][max_idx][i], state[2][max_idx][i], state[3][max_idx][i] = \
            state[1][max_idx][i], state[2][max_idx][i], state[3][max_idx][i], state[4][max_idx][i]


def turn_f(state, max_idx):
    state[1] = rot90(state[1])
    displacedR = state[2][0][0]
    displacedL = state[4][0][max_idx]
    for i in range(max_idx + 1):
        state[5][max_idx][i], state[2][i][0], state[0][0][i], state[4][i][max_idx] = \
            state[4][max_idx - i][max_idx], state[5][max_idx][i], state[2][max_idx - i][0], state[0][0][i]
    state[5][max_idx][max_idx] = displacedL
    state[0][0][max_idx] = displacedR


def turn_fi(state, max_idx):
    state[1] = rot270(state[1]) 
    displacedR = state[2][max_idx][0]
    displacedL = state[4][max_idx][max_idx]
    for i in range(max_idx + 1):
        state[4][max_idx - i][max_idx], state[5][max_idx][i], state[2][max_idx - i][0], state[0][0][i] = \
            state[5][max_idx][i], state[2][i][0], state[0][0][i], state[4][i][max_idx]
    state[5][max_idx][max_idx] = displacedR
    state[0][0][max_idx] = displacedL


def turn_b(state, max_idx):
    state[3] = rot90(state[3])
    displacedR = state[2][max_idx][max_idx]
    displacedL = state[4][max_idx][0]
    for i in range(max_idx + 1):
        state[4][max_idx - i][0], state[5][0][i], state[2][max_idx - i][max_idx], state[0][max_idx][i] = \
            state[5][0][i], state[2][i][max_idx], state[0][max_idx][i], state[4][i][0]
    state[5][0][max_idx] = displacedR
    state[0][max_idx][max_idx] = displacedL


def turn_bi(state, max_idx):
    state[3] = rot270(state[3])
    displacedR = state[2][0][max_idx]
    displacedL = state[4][0][0]
    for i in range(max_idx + 1):
        state[5][0][i], state[2][i][max_idx], state[0][max_idx][i], state[4][i][0] = \
            state[4][max_idx - i][0], state[5][0][i], state[2][max_idx - i][max_idx], state[0][max_idx][i]
    state[5][0][max_idx] = displacedL
    state[0][max_idx][max_idx] = displacedR   


# center moves
def turn_m(state, max_idx):
    for i in range(max_idx + 1):
        state[1][i][max_idx - 1], state[0][i][max_idx - 1], \
            state[3][max_idx - i][1], state[5][i][max_idx - 1] = \
            state[5][i][max_idx - 1], state[1][i][max_idx - 1], \
            state[0][i][max_idx - 1], state[3][max_idx - i][1]        


def turn_mi(state, max_idx):
    for i in range(max_idx + 1):
        state[5][i][max_idx - 1], state[1][i][max_idx - 1], \
            state[0][i][max_idx - 1], state[3][max_idx - i][1] = \
            state[1][i][max_idx - 1], state[0][i][max_idx - 1], \
            state[3][max_idx - i][1], state[5][i][max_idx - 1] 


def turn_e(state, max_idx):
    for i in range(max_idx + 1):
        state[1][max_idx - 1][i], state[2][max_idx - 1][i], state[3][max_idx - 1][i], state[4][max_idx - 1][i] = \
            state[4][max_idx - 1][i], state[1][max_idx - 1][i], state[2][max_idx - 1][i], state[3][max_idx - 1][i]     


def turn_ei(state, max_idx):
    for i in range(max_idx + 1):
        state[4][max_idx - 1][i], state[1][max_idx - 1][i], state[2][max_idx - 1][i], state[3][max_idx - 1][i] = \
            state[1][max_idx - 1][i], state[2][max_idx - 1][i], state[3][max_idx - 1][i], state[4][max_idx - 1][i]


def turn_s(state, max_idx):
    displacedR = state[2][0][1]
    displacedL = state[4][0][max_idx - 1]
    for i in range(max_idx + 1):
        state[5][max_idx - 1][i], state[2][i][1], state[0][1][i], state[4][i][max_idx - 1] = \
            state[4][max_idx - i][max_idx - 1], state[5][max_idx - 1][i], state[2][max_idx - i][1], state[0][1][i]
    state[5][max_idx - 1][max_idx] = displacedL
    state[0][1][max_idx] = displacedR


def turn_si(state, max_idx):
    displacedR = state[2][max_idx][1]
    displacedL = state[4][max_idx][max_idx - 1]
    for i in range(max_idx + 1):
        state[4][max_idx - i][max_idx - 1], state[5][max_idx - 1][i], state[2][max_idx - i][1], state[0][1][i] = \
            state[5][max_idx - 1][i], state[2][i][1], state[0][1][i], state[4][i][max_idx - 1]
    state[5][max_idx - 1][max_idx] = displacedR
    state[0][1][max_idx] = displacedL


def turn_r2(state, max_idx):
    turn_r(state, max_idx)
    turn_r(state, max_idx)


def turn_l2(state, max_idx):
    turn_l(state, max_idx)
    turn_l(state, max_idx)


def turn_u2(state, max_idx):
    turn_u(state, max_idx)
    turn_u(state, max_idx)


def turn_d2(state, max_idx):
    turn_d(state, max_idx)
    turn_d(state, max_idx)


def turn_f2(state, max_idx):
    turn_f(state, max_idx)
    turn_f(state, max_idx)


def turn_b2(state, max_idx):
    turn_b(state, max_idx)
    turn_b(state, max_idx)


def turn_m2(state, max_idx):
    turn_m(state, max_idx)
    turn_m(state, max_idx)


def turn_e2(state, max_idx):
    turn_e(state, max_idx)
    turn_e(state, max_idx)


def turn_s2(state, max_idx):
    turn_s(state, max_idx)
    turn_s(state, max_idx)


# 2 layers move at sime time (center + outer)
def turn_rw(state, max_idx):
    turn_r(state, max_idx)
    turn_mi(state, max_idx)


def turn_rwi(state, max_idx):
    turn_ri(state, max_idx)
    turn_m(state, max_idx)


def turn_lw(state, max_idx):
    turn_l(state, max_idx)
    turn_m(state, max_idx)


def turn_lwi(state, max_idx):
    turn_li(state, max_idx)
    turn_mi(state, max_idx)


def turn_uw(state, max_idx):
    turn_u(state, max_idx)
    turn_ei(state, max_idx)


def turn_uwi(state, max_idx):
    turn_ui(state, max_idx)
    turn_e(state, max_idx)


def turn_dw(state, max_idx):
    turn_d(state, max_idx)
    turn_e(state, max_idx)


def turn_dwi(state, max_idx):
    turn_di(state, max_idx)
    turn_ei(state, max_idx)


def turn_fw(state, max_idx):
    turn_f(state, max_idx)
    turn_s(state, max_idx)


def turn_fwi(state, max_idx):
    turn_fi(state, max_idx)
    turn_si(state, max_idx)


def turn_bw(state, max_idx):
    turn_b(state, max_idx)
    turn_si(state, max_idx)


def turn_bwi(state, max_idx):
    turn_bi(state, max_idx)
    turn_s(state, max_idx)                


# double wide moves (2 layers)
def turn_rw2(state, max_idx):
    turn_rw(state, max_idx)
    turn_rw(state, max_idx)


def turn_lw2(state, max_idx):
    turn_lw(state, max_idx)
    turn_lw(state, max_idx)


def turn_uw2(state, max_idx):
    turn_uw(state, max_idx)
    turn_uw(state, max_idx)


def turn_dw2(state, max_idx):
    turn_dw(state, max_idx)
    turn_dw(state, max_idx)


def turn_fw2(state, max_idx):
    turn_fw(state, max_idx)
    turn_fw(state, max_idx)


def turn_bw2(state, max_idx):
    turn_bw(state, max_idx)
    turn_bw(state, max_idx)          


# cube rotations
def rot_x(state, max_idx):
    turn_rw(state, max_idx)
    turn_li(state, max_idx)


def rot_xi(state, max_idx):
    turn_rwi(state, max_idx)
    turn_l(state, max_idx)


def rot_y(state, max_idx):
    turn_uw(state, max_idx)
    turn_di(state, max_idx)


def rot_yi(state, max_idx):
    turn_uwi(state, max_idx)
    turn_d(state, max_idx)


def rot_z(state, max_idx):
    turn_fw(state, max_idx)
    turn_bi(state, max_idx)


def rot_zi(state, max_idx):
    turn_fwi(state, max_idx)
    turn_b(state, max_idx)


def rot_x2(state, max_idx):
    rot_x(state, max_idx)
    rot_x(state, max_idx)


def rot_y2(state, max_idx):
    rot_y(state, max_idx)
    rot_y(state, max_idx)


def rot_z2(state, max_idx):
    rot_z(state, max_idx)
    rot_z(state, max_idx)


ACTIONS_3x3 = {"R": turn_r, "R'": turn_ri, "L": turn_l, "L'": turn_li, "U": turn_u,
           "U'": turn_ui, "D": turn_d, "D'": turn_di, "F": turn_f, "F'": turn_fi,
           "B": turn_b, "B'": turn_bi, "M": turn_m, "M'": turn_mi, "E": turn_e,
           "E'": turn_ei, "S": turn_s, "S'": turn_si, "r": turn_rw, "r'": turn_rwi,
           "l": turn_lw, "l'": turn_lwi, "u": turn_uw, "u'": turn_uwi, "d": turn_dw,
           "d'": turn_dwi, "f": turn_fw, "f'": turn_fwi, "b": turn_bw, "b'": turn_bwi,
           "x": rot_x, "x'": rot_xi, "y": rot_y, "y'": rot_yi, "z": rot_z,
           "z'": rot_zi, "R2": turn_r2, "L2": turn_l2, "U2": turn_u2, "D2": turn_d2,
           "F2": turn_f2, "B2": turn_b2, "M2": turn_m2, "E2": turn_e2, "S2": turn_s2,
           "r2": turn_rw2, "l2": turn_lw2, "u2": turn_uw2, "d2": turn_dw2, "f2": turn_fw2,
           "b2": turn_bw2, "x2": rot_x2, "y2": rot_y2, "z2": rot_z2}

