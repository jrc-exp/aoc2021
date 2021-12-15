""" Day 15 Solutions """

from collections import defaultdict, Counter
import sys
import numpy as np
from aoc.y2021.utils import load_data


def heur(x, y, xs, ys):
    # using euclidean distance, but it doesn't seem to matter what the heuristic is...
    return np.sqrt((x - xs) ** 2 + (y - ys) ** 2)


def best_f_score(fScore, open_set):
    best = np.inf
    for f in open_set:
        s = fScore[f]
        if s < best:
            best = s
            best_node = f
    return best_node


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

    open_set = set([(0, 0)])
    came_from = dict()
    g_score = defaultdict(lambda: np.inf)
    g_score[(0, 0)] = 0
    h_score = defaultdict(lambda: np.inf)
    h_score[(0, 0)] = hcost[0, 0]
    goal = (r - 1, c - 1)
    while open_set:
        current = best_f_score(h_score, open_set)
        if current == goal:
            path = reconstruct_path(came_from, current)
            break
        open_set.remove(current)
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
                h_score[(xn, yn)] = tentative_g_score + hcost[xn, yn]
                if (xn, yn) not in open_set:
                    open_set.add((xn, yn))

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
            tmp_node_cost = node_cost.copy()
            tmp_node_cost += (x + y) % 9
            tmp_node_cost[tmp_node_cost > 9] -= 9
            big_maze[r * x : r * (x + 1), c * y : c * (y + 1)] = tmp_node_cost

    # pprint big maze:
    # for row in big_maze:
    #     print("".join([str(int(k)) for k in row]))

    result_2 = solve_maze(big_maze)

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
