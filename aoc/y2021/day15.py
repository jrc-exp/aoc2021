""" Day 15 Solutions """

from bisect import insort_left
from collections import defaultdict, Counter, deque
import sys
from networkx import Graph, DiGraph, shortest_path_length
import numpy as np
from aoc.y2021.utils import load_data


def heur(x, y, xs, ys):
    # using manhattan distance
    return abs(x - xs) + abs(y - ys)


def reconstruct_path(came_from, node, path=[]):
    while node != (0, 0):
        path = [node] + path
        node = came_from[node]
    return path


def solve_maze(node_cost):
    cost = np.zeros_like(node_cost)
    r, c = node_cost.shape
    moves = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    hcost = np.zeros_like(node_cost)
    for k in range(r):
        for j in range(r):
            hcost[k, j] = heur(k, j, r, c)

    # keep these sorted high to low so we can just call pop()
    open_set = deque([(0, 0, 0)])
    # keep a look-up map/hash table for quick access to "if in"
    open_set_hash = defaultdict(lambda: False)
    open_set_hash[(0, 0)] = True
    came_from = dict()
    g_score = defaultdict(lambda: np.inf)
    g_score[(0, 0)] = 0
    f_score = defaultdict(lambda: np.inf)
    f_score[(0, 0)] = hcost[0, 0]
    goal = (r - 1, c - 1)
    ct = 0
    while open_set:
        ct += 1
        # the lists are sorted so we just pop(0) here
        x, y, _ = open_set.popleft()
        current = (x, y)
        open_set_hash[current] = False
        if current == goal:
            path = reconstruct_path(came_from, current)
            break
        x, y = current
        for xm, ym in moves:
            xn, yn = x + xm, y + ym
            if xn < 0 or xn >= r or yn < 0 or yn >= c:
                # don't go off edge
                continue
            tentative_g_score = g_score[current] + node_cost[xn, yn]
            if tentative_g_score < g_score[(xn, yn)]:
                came_from[(xn, yn)] = current
                g_score[(xn, yn)] = tentative_g_score
                f_score[(xn, yn)] = tentative_g_score + hcost[xn, yn]
                fn = f_score[(xn, yn)]
                if not open_set_hash[(xn, yn)]:
                    # insert the node sorted so we can pop(0) above
                    insort_left(open_set, (xn, yn, fn), key=lambda x: x[2])
                    open_set_hash[(xn, yn)] = True

    cost = 0
    for x, y in path:
        if (x, y) == (0, 0):
            pass
        cost += node_cost[x, y]

    return cost


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    # print("INPUT DATA:")
    # print(d)
    node_cost = np.zeros((len(d), len(d[0])))
    for idx, row in enumerate(d):
        node_cost[idx] = list(map(int, row))
    print()

    result_1 = solve_maze(node_cost)

    # pprint small_maze:
    # for row in node_cost:
    #     print("".join([str(int(k)) for k in row]))

    r, c = node_cost.shape
    big_maze = np.zeros((5 * r, 5 * c))
    for x in range(5):
        for y in range(5):
            big_maze[r * x : r * (x + 1), c * y : c * (y + 1)] = (node_cost + x + y - 1) % 9 + 1

    # pprint big maze:
    # for row in big_maze:
    #     print("".join([str(int(k)) for k in row]))

    result_2 = solve_maze(big_maze)

    """
    # for posterity: here's how to use networkx for a directed graph:

    from networkx import DiGraph, shortest_path_length
    G = DiGraph()
    moves = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    r, c = big_maze.shape
    for x in range(r):
        for y in range(c):
            for xm, ym in moves:
                xn, yn = x + xm, y + ym
                if xn < 0 or xn >= r or yn < 0 or yn >= c:
                    continue
                G.add_edge((x, y), (xn, yn), weight=big_maze[xn, yn])
    result_2 = shortest_path_length(G, (0, 0), (r - 1, c - 1), "weight")
    """

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day15.txt")
        test_answer_1 = 40
        test_answer_2 = 315
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day15.txt")
    answer_1, answer_2 = solve(d)
    assert answer_1 == 447
    assert answer_2 == 2825
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
