""" Day 23 Solutions """

import sys
from copy import deepcopy
from collections import defaultdict, Counter
from itertools import permutations, product
import numpy as np
from aoc.y2021.utils import load_data


def ints(x):
    return list(map(int, x))


OPEN = "."
WALL = "#"
MOVE_COST = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


class Node:
    """NODE HELPER"""

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __add__(self, z):
        return Node(self.y + z[0], self.x + z[1])

    def __hash__(self) -> int:
        return (self.y, self.x).__hash__()

    def __repr__(self):
        return f"({self.y}, {self.x})"

    def __eq__(self, n):
        return self.y == n.y and self.x == n.x


GOAL_NODES = {
    "A": (Node(2, 3), Node(3, 3)),
    "B": (Node(2, 5), Node(3, 5)),
    "C": (Node(2, 7), Node(3, 7)),
    "D": (Node(2, 9), Node(3, 9)),
}

GOAL_X = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9,
}

U = (-1, 0)
D = (1, 0)
L = (0, -1)
R = (0, 1)
MOVES = (U, D, L, R)


def in_hall(node):
    return node.y == 1


def done_moving(node, nodes):
    char = nodes[node]
    return in_goal(node, nodes) and nodes[node + D] in [WALL, char]


def in_goal(node, nodes):
    char = nodes[node]
    return node in GOAL_NODES[char]


def in_doorway(node):
    return in_hall(node) and node.x in [3, 5, 7, 9]


def is_open(node, nodes):
    return nodes[node] == OPEN


def legal_moves(nodes, dudes, first_move=False):
    """FIND LEGAL MOVES FROM POSITION"""
    moves = []
    # if anyone is in the doorway, they must keep moving immediately
    for (node, _) in dudes:
        char = nodes[node]
        if in_doorway(node):
            # you have to move into goal if it's chill
            if node + D in GOAL_NODES[char]:
                if goal_open(node, nodes):
                    return [(node, node + D)]
            # otherwise you go left or right if there's room
            if is_open(node + L, nodes):
                moves.append((node, node + L))
            if is_open(node + R, nodes):
                moves.append((node, node + R))
            return moves

    for (node, moving) in dudes:
        char = nodes[node]
        if done_moving(node, nodes):
            # print(char, "at", node, "is done.")
            continue

        # we either have to be moving or have an open goal
        for d in MOVES:
            if not is_open(node + d, nodes):
                continue
            # we can only go down if we're aligned
            if d == D and node.x is not GOAL_X[char]:
                continue
            if moving or first_move or goal_open(node, nodes):
                if moving or first_move:
                    moves.append((node, node + d))
                elif toward_goal(node, d, nodes):
                    moves.append((node, node + d))
            # we can start to leave our room though:
            elif d == U and node.y > 1:
                moves.append((node, node + U))
    return moves


def toward_goal(node, d, nodes):
    """is direction toward goal"""
    char = nodes[node]
    if GOAL_X[char] == node.x:
        if d == D:
            return True
    if GOAL_X[char] < node.x:
        if d == R:
            return True
    elif GOAL_X[char] > node.x:
        if d == L:
            return True
    return False


def goal_open(node, nodes):
    """is the path clear to the goal?"""
    char = nodes[node]
    # check if the room is clear or has a friend in it
    for spot in GOAL_NODES[char]:
        # TODO(JRC): It's not ok if our friend is not at the bottom!
        if not (is_open(spot, nodes) or nodes[spot] == char):
            return False
    doorway = Node(1, GOAL_X[char])
    if node == doorway:
        return True
    if GOAL_X[char] < node.x:
        spot = node
        while spot is not doorway:
            if is_open(spot + R, nodes):
                spot = spot + R
            else:
                return False
    elif GOAL_X[char] > node.x:
        spot = node
        while spot is not doorway:
            if is_open(spot + L, nodes):
                spot = spot + L
            else:
                return False
    return True


def move_cost(move, nodes):
    return MOVE_COST[nodes[move[0]]]


def print_board(nodes, dudes=None):
    for row in range(5):
        x = ""
        for char in range(13):
            x += nodes.get(Node(row, char), "")
        print(x)
    if dudes:
        print(dudes)


def make_move(move, nodes, dudes):
    """apply a move"""
    node, node_out = move
    assert is_open(node_out, nodes)
    assert nodes[node] in "ABCD", f"{nodes[node]} and {move} and {dudes}/ {print_board(nodes)}"
    nodes = deepcopy(nodes)
    dudes = deepcopy(dudes)
    nodes[node_out] = nodes[node]
    nodes[node] = OPEN
    dudes = [(dude, False) for dude, _ in dudes if dude != node]
    dudes.append((node_out, True))
    return nodes, dudes


def find_paths(nodes, dudes, moves, first_move=False):
    """find paths"""
    nodes = deepcopy(nodes)
    dudes = deepcopy(dudes)
    if all(in_goal(dude, nodes) for dude, _ in dudes):
        print("Done!")
        return moves
    all_paths = []
    for move in legal_moves(nodes, dudes, first_move):
        # don't repeat a move
        if moves and move[0] == moves[-1][1] and move[1] == moves[-1][0]:
            continue
        tnodes, tdudes = make_move(move, nodes, dudes)
        all_paths = all_paths + [find_paths(tnodes, tdudes, moves + [move])]
    return all_paths


##################################################################################################################
# TODO: Run Djikstra except use only "legal_moves" at a step, and track the 8-letter states for best cost so far #
##################################################################################################################


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    nodes = {}
    dudes = []
    for idx, row in enumerate(d):
        for idy, char in enumerate(row):
            nodes[Node(idx, idy)] = char
            if char in "ABCD":
                dudes.append((Node(idx, idy), 0))

    # print("Legal Moves")
    # for move in legal_moves(nodes, dudes, first_move=True):
    # print(move, move_cost(move, nodes))

    paths = find_paths(nodes, dudes, [], first_move=True)
    for path in paths:
        print(path)

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day23.txt")
        test_answer_1 = 12521
        test_answer_2 = 0
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day23.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
