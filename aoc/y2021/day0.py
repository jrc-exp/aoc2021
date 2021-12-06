""" Day 0 Solutions """

import sys
import numpy as np
from aoc.y2021.utils import load_data


def solve(d):
    """ actual solution with puzzle input """
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    return result_1, result_2


def main():
    """ Main function """
    # load data:
    skip_test = False
    if not skip_test:
        print('**** TEST DATA ****')
        d = load_data("test_day0.txt")
        test_answer_1 = TEST_ANSWER
        test_answer_2 = 0
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print('**** TESTS PASSED ****')
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print('**** REAL DATA ****')
    d = load_data("day0.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
