""" Day 23 Solutions """
import heapq
from functools import cache
import sys
from copy import deepcopy
from collections import defaultdict, Counter
from itertools import permutations, product
from unittest import result
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

    def __lt__(self, z):
        if self.x < z.x:
            return True
        elif self.y < z.y:
            return True
        return False

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

GOAL_NODES_BIG = {
    "A": (Node(2, 3), Node(3, 3), Node(4, 3), Node(5, 3)),
    "B": (Node(2, 5), Node(3, 5), Node(4, 5), Node(5, 5)),
    "C": (Node(2, 7), Node(3, 7), Node(4, 7), Node(5, 7)),
    "D": (Node(2, 9), Node(3, 9), Node(4, 9), Node(5, 9)),
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


def in_goal(node, char):
    assert char in "ABCD"
    return node in GOAL_NODES[char]


def is_open(node, nodes):
    return nodes[node] == OPEN


def path_clear(node1, node2, state, paths):
    occupied = set(node for node, _ in state)
    path = paths[(node1, node2)]
    if all(node not in occupied for node in path[1:]):
        return len(path) - 1
    return 0


NON_DOOR_NODES = [Node(1, x) for x in range(1, 12) if x not in [3, 5, 7, 9]]

# pylint: disable=dangerous-default-value
def full_moves(state, paths, goal_nodes=GOAL_NODES):
    """full sized moves"""
    moves = []
    for node, char in state:
        # finished moving:
        if in_goal(node, char):
            # TODO(JRC): FIX THIS FOR ANY SIZE
            for y in range(node.y, 4 if len(state) == 8 else 6):
                if (Node(y, node.x), char) not in state:
                    break
            else:
                continue

        goal_available = False
        for node_out in goal_nodes[char]:
            if node_out == node:
                continue
            cost = path_clear(node, node_out, state, paths)
            if not cost:
                # if we can't get here, this needs to be a correct type
                if (node_out, char) not in state:
                    break
                # if it's the right one at the bottom, we can check above
                continue
            moves.append((cost * MOVE_COST[char], node, node_out))
            goal_available = True
            break
        if goal_available:
            continue

        # if we're not finished, but in a lower place we can maybe move to the hall
        if node.y > 1:
            for node_out in NON_DOOR_NODES:
                if node_out == node:
                    continue
                cost = path_clear(node, node_out, state, paths)
                if cost:
                    moves.append((cost * MOVE_COST[char], node, node_out))
    return moves


def print_board(state, spaces):
    """print the board"""
    for row in range(5):
        x = ""
        for char in range(13):
            for c in "ABCD":
                if (Node(row, char), c) in state:
                    x += c
                    break
            else:
                if Node(row, char) in spaces:
                    x += "."
                else:
                    x += "#"

        print(x)


GOAL_STATE = frozenset(
    (
        (Node(2, 3), "A"),
        (Node(3, 3), "A"),
        (Node(2, 5), "B"),
        (Node(3, 5), "B"),
        (Node(2, 7), "C"),
        (Node(3, 7), "C"),
        (Node(2, 9), "D"),
        (Node(3, 9), "D"),
    )
)

GOAL_STATE_BIG = []
for char, x in GOAL_X.items():
    for y in range(2, 6):
        GOAL_STATE_BIG.append((Node(y, x), char))
print(GOAL_STATE_BIG)
GOAL_STATE_BIG = frozenset(GOAL_STATE_BIG)


def state_to_occupied(state):
    return set(n for n, c in state)


def solve_maze(goal, pod_locs, paths, spaces):
    """solve maze"""
    # keep a look-up map/hash table for quick access to "if in open set"
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
            char = ""
            for n, c in state:
                if node_in == n:
                    char = c
            out_state = [(n, c) for (n, c) in state if n != node_in]
            out_state.append((node_out, char))
            out_state = frozenset(out_state)
            out_nodes = [n for (n, _) in out_state]
            count = Counter(out_nodes)
            # print((node_in, node_out), out_state)
            assert all(count[k] == 1 for k in count)
            tentative_g_score = g_score[state] + node_cost
            if tentative_g_score < g_score[out_state]:
                came_from[out_state] = state
                g_score[out_state] = tentative_g_score
                fn = g_score[out_state]
                if not open_set_hash[out_state]:
                    heapq.heappush(open_set, (fn, out_state))
                    open_set_hash[out_state] = True

    return g_score[goal]


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
        for idy, char in enumerate(row):
            nodes[Node(idx, idy)] = char
            if char in "ABCD.":
                spaces.append(Node(idx, idy))
            if char in "ABCD":
                pod_locs.append((Node(idx, idy), char))

    neighbors = defaultdict(list)
    for node in spaces:
        for move in MOVES:
            if node + move in spaces:
                neighbors[node].append(node + move)

    paths = {}
    for node in spaces:
        for node_out in spaces:
            if node != node_out:
                paths[(node, node_out)] = find_goal(node, node_out, [], neighbors)

    assert path_clear(Node(3, 7), Node(1, 10), pod_locs, paths) == 0
    assert path_clear(Node(2, 7), Node(1, 7), pod_locs, paths) == 1
    assert path_clear(Node(2, 7), Node(1, 8), pod_locs, paths) == 2
    assert path_clear(Node(3, 3), Node(1, 7), pod_locs, paths) == 0
    assert path_clear(Node(2, 9), Node(1, 1), pod_locs, paths) == 9

    # print(full_moves(pod_locs, paths))
    result_1 = solve_maze(GOAL_STATE, pod_locs, paths, spaces)
    nodes = {}
    pod_locs = []
    spaces = []
    bonus_lines = load_data("day23_p2.txt")
    d = d[:2] + bonus_lines + d[2:]
    for idx, row in enumerate(d):
        for idy, char in enumerate(row):
            nodes[Node(idx, idy)] = char
            if char in "ABCD.":
                spaces.append(Node(idx, idy))
            if char in "ABCD":
                pod_locs.append((Node(idx, idy), char))

    neighbors = defaultdict(list)
    for node in spaces:
        for move in MOVES:
            if node + move in spaces:
                neighbors[node].append(node + move)

    paths = {}
    for node in spaces:
        for node_out in spaces:
            if node != node_out:
                paths[(node, node_out)] = find_goal(node, node_out, [], neighbors)

    result_2 = solve_maze(GOAL_STATE_BIG, pod_locs, paths, spaces)

    return result_1, result_2


def find_goal(start, goal, path, neighbors):
    """Find the path from a scanner to the origin scanner"""
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
    # load data:
    skip_test = False
    if not skip_test:
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
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
