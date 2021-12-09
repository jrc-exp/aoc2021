""" Day 9 Solutions """

import sys
import numpy as np
from aoc.y2021.utils import load_data
from scipy.ndimage import generic_filter
from skimage.measure import regionprops, label


def low_point(d):
    if d[2] < min(d[0], d[1], d[3], d[4]):
        return d[2] + 1
    return 0


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    d = np.array([[int(k) for k in x] for x in d])
    footprint = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    mins = generic_filter(d, low_point, footprint=footprint, mode="constant", cval=1000)
    result_1 = np.sum(mins)

    d[d < 9] = 0
    x = label(d, background=9, connectivity=1)
    result_2 = np.prod(sorted([r.area for r in regionprops(x)])[-3:])

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day9.txt")
        test_answer_1 = 15
        test_answer_2 = 1134
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day9.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
