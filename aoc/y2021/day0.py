""" Day 0 Solutions """

import sys
import numpy as np
from aoc.y2021.utils import load_data


def solve(d):
    """ actual solution with puzzle input """
    result = 0
    print("INPUT DATA:")
    print(d)
    return result


def main():
    """ Main function """
    # load data:
    skip_test = False
    if not skip_test:
        try:
            d = load_data("test_day0.txt")
            test_answer = 0
            test_solution_1 = solve(d)
            assert test_solution_1 == test_answer
            print('TEST PASSES')
            print("Test Answer 1: ", test_answer)
            print("My Test Answer 1: ", test_solution_1)
        except OSError:
            print('No Test File!')
        except AssertionError:
            print(f"TEST FAILED: TRUTH={test_answer}, YOURS={test_solution_1}")
            sys.exit()
    print('**** REAL DATA ****')
    d = load_data("day0.txt")
    answer_1 = solve(d)
    print("Answer 1:", answer_1)


if __name__ == "__main__":
    main()
