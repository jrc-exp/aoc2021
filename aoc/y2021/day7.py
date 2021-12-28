""" Day 7 Solutions """

import os
import sys

import numpy as np

from aoc.y2021.utils import load_data

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    d = list(map(int, d[0].split(",")))
    print(d)

    def cost_to_move(d, pos):
        d = np.array(d)
        cost = np.sum(np.abs(d - pos))
        return cost

    def p2_cost_to_move(d, pos):
        d = np.array(d)
        dist = np.abs(d - pos)
        cost = np.sum(dist * (dist + 1) / 2)
        return cost

    cost = np.inf
    cost2 = np.inf
    for pos in range(0, np.max(d)):
        c = cost_to_move(d, pos)
        if c < cost:
            cost = c
            lowest_cost = c
        c = p2_cost_to_move(d, pos)
        if c < cost2:
            cost2 = c
            lowest_cost2 = c

    result_1 = lowest_cost
    result_2 = lowest_cost2

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day7.txt")
        test_answer_1 = 37
        test_answer_2 = 168
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day7.txt")
    from time import time

    now = time()
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)
    print("Time to solve:", time() - now)


if __name__ == "__main__":
    main()
