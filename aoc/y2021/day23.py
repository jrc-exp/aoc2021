""" Day 23 Solutions """
from argparse import ArgumentParser
import heapq
from functools import cache
import sys
from copy import deepcopy
from collections import defaultdict, Counter
from itertools import permutations, product
from unittest import result
import numpy as np
from aoc.y2021.utils import load_data

import os

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


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


GOAL_NODES = {
    "A": ((2, 3), (3, 3)),
    "B": ((2, 5), (3, 5)),
    "C": ((2, 7), (3, 7)),
    "D": ((2, 9), (3, 9)),
}

GOAL_NODES_BIG = {
    "A": ((2, 3), (3, 3), (4, 3), (5, 3)),
    "B": ((2, 5), (3, 5), (4, 5), (5, 5)),
    "C": ((2, 7), (3, 7), (4, 7), (5, 7)),
    "D": ((2, 9), (3, 9), (4, 9), (5, 9)),
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


def in_goal(node, letter, goal_nodes):
    assert letter in "ABCD"
    return node in goal_nodes[letter]


def path_clear(node1, node2, paths, occupied):
    path = paths[(node1, node2)]
    # if all(node not in occupied for node in path[1:]):
    for node in path:
        if node in occupied:
            return 0
    return len(path)


NON_DOOR_NODES = [(1, x) for x in range(1, 12) if x not in [3, 5, 7, 9]]

# pylint: disable=dangerous-default-value
def full_moves(state, paths, goal_nodes=GOAL_NODES):
    """full sized moves"""
    moves = []
    occupied = set(node for node, _ in state)
    for node, letter in state:
        # finished moving:
        if in_goal(node, letter, goal_nodes):
            for y in range(node[0], 4 if len(state) == 8 else 6):
                if ((y, node[1]), letter) not in state:
                    break
            else:
                continue

        goal_available = False
        for node_out in reversed(goal_nodes[letter]):
            if node_out == node:
                continue
            cost = path_clear(node, node_out, paths, occupied)
            if not cost:
                # if we can't get here, this needs to be a correct type
                if (node_out, letter) not in state:
                    break
                # if it's the right one at the bottom, we can check above
                continue
            moves.append((cost * MOVE_COST[letter], node, node_out))
            goal_available = True
            break
        if goal_available:
            continue

        # if we're not finished, but in a lower place we can maybe move to the hall
        if node[0] > 1:
            for node_out in NON_DOOR_NODES:
                cost = path_clear(node, node_out, paths, occupied)
                if cost:
                    moves.append((cost * MOVE_COST[letter], node, node_out))
    return moves


def print_board(state, spaces):
    """print the board"""
    for row in range(5 if len(state) == 8 else 7):
        x = ""
        for letter in range(13):
            for c in "ABCD":
                if ((row, letter), c) in state:
                    x += c
                    break
            else:
                if (row, letter) in spaces:
                    x += "."
                else:
                    x += "#"

        print(x)


GOAL_STATE = frozenset(
    (
        ((2, 3), "A"),
        ((3, 3), "A"),
        ((2, 5), "B"),
        ((3, 5), "B"),
        ((2, 7), "C"),
        ((3, 7), "C"),
        ((2, 9), "D"),
        ((3, 9), "D"),
    )
)

GOAL_STATE_BIG = []
for l, x in GOAL_X.items():
    for y in range(2, 6):
        GOAL_STATE_BIG.append(((y, x), l))
GOAL_STATE_BIG = frozenset(GOAL_STATE_BIG)


def heur_node(node, letter, goal_nodes, paths):
    h = 0
    if not in_goal(node, letter, goal_nodes):
        h = MOVE_COST[letter] * len(paths[(node, goal_nodes[letter][0])])
    return h


def heur(out_state, paths):
    """
    one heuristic that is "fast" is that everything has to move
    at least their x-distance from the goal column to be finished
    but this doesn't seem to be enough to speed the search
    """
    h = 0
    goal_nodes = GOAL_NODES if len(out_state) == 8 else GOAL_NODES_BIG
    for node, letter in out_state:
        h += heur_node(node, letter, goal_nodes, paths)
    return h


def solve_puzzle(goal, pod_locs, paths, spaces):
    """solve maze"""
    # keep a look-up map/hash table for quick access to "if in open set"
    print_board(pod_locs, spaces)
    if len(pod_locs) == 8:
        goal_nodes = GOAL_NODES
    else:
        goal_nodes = GOAL_NODES_BIG
    open_set_hash = defaultdict(lambda: False)
    print("start_state", pod_locs)
    start_state = frozenset(pod_locs)
    open_set_hash[start_state] = True
    open_set = [
        (0, start_state),
    ]
    came_from = dict()
    g_score = defaultdict(lambda: np.inf)
    g_score[start_state] = 0
    while open_set:
        _, state = heapq.heappop(open_set)
        open_set_hash[state] = False
        moves = full_moves(state, paths, goal_nodes)
        for node_cost, node_in, node_out in moves:
            letter = ""
            for n, c in state:
                if node_in == n:
                    letter = c
            out_state = list(state)
            out_state.remove((node_in, letter))
            out_state.append((node_out, letter))
            out_state = frozenset(out_state)
            tentative_g_score = g_score[state] + node_cost
            if tentative_g_score < g_score[out_state]:
                came_from[out_state] = state
                g_score[out_state] = tentative_g_score
                # slower with the heuristic... *sigh*
                fn = g_score[out_state]  # + heur(out_state, paths)
                if not open_set_hash[out_state]:
                    heapq.heappush(open_set, (fn, out_state))
                    open_set_hash[out_state] = True

    path = [goal]
    state = came_from[goal]
    while True:
        state = came_from.get(state, None)
        if not state:
            break
        path.append(state)
    path = list(reversed(path))

    return g_score[goal], path


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    # part 1
    nodes = {}
    pod_locs = []
    spaces = []
    for idx, row in enumerate(d):
        for idy, letter in enumerate(row):
            nodes[(idx, idy)] = letter
            if letter in "ABCD.":
                spaces.append((idx, idy))
            if letter in "ABCD":
                pod_locs.append(((idx, idy), letter))

    neighbors = defaultdict(list)
    for node in spaces:
        for move in MOVES:
            neighb = (node[0] + move[0], node[1] + move[1])
            if neighb in spaces:
                neighbors[node].append(neighb)

    paths = {}
    for node in spaces:
        for node_out in spaces:
            if node != node_out:
                paths[(node, node_out)] = set(find_goal(node, node_out, [], neighbors)[1:])

    occupied = set(node for node, _ in pod_locs)
    assert path_clear((3, 7), (1, 10), paths, occupied) == 0
    assert path_clear((2, 7), (1, 7), paths, occupied) == 1
    assert path_clear((2, 7), (1, 8), paths, occupied) == 2
    assert path_clear((3, 3), (1, 7), paths, occupied) == 0
    assert path_clear((2, 9), (1, 1), paths, occupied) == 9

    # print(full_moves(pod_locs, paths))
    result_1, _ = solve_puzzle(GOAL_STATE, pod_locs, paths, spaces)
    nodes = {}
    pod_locs = []
    spaces = []
    bonus_lines = load_data("day23_p2.txt")
    d = d[:3] + bonus_lines + d[3:]
    for idx, row in enumerate(d):
        for idy, letter in enumerate(row):
            nodes[(idx, idy)] = letter
            if letter in "ABCD.":
                spaces.append((idx, idy))
            if letter in "ABCD":
                pod_locs.append(((idx, idy), letter))

    neighbors = defaultdict(list)
    for node in spaces:
        for move in MOVES:
            neighb = (node[0] + move[0], node[1] + move[1])
            if neighb in spaces:
                neighbors[node].append(neighb)

    paths = {}
    for node in spaces:
        for node_out in spaces:
            if node != node_out:
                paths[(node, node_out)] = set(find_goal(node, node_out, [], neighbors)[1:])

    result_2, path = solve_puzzle(GOAL_STATE_BIG, pod_locs, paths, spaces)
    for idx, step in enumerate(path):
        print("Step", idx)
        print_board(step, spaces)

    return result_1, result_2


def find_goal(start, goal, path, neighbors):
    """Find the shortest path from a node to another node"""
    if goal in neighbors[start]:
        return path + [start, goal]
    for node in neighbors[start]:
        visited = set(a for a in path)
        if node not in visited:
            goal_path = find_goal(node, goal, path + [start], neighbors)
            if goal_path is not None:
                return goal_path
    return None


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day23.txt")
        test_answer_1 = 12521
        test_answer_2 = 44169
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
    assert answer_1 == 16059
    assert answer_2 == 43117
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
