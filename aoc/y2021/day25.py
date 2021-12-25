""" Day 25 Solutions """

from argparse import ArgumentParser
import sys
from collections import defaultdict, Counter
from itertools import permutations, product
import numpy as np
from tqdm import tqdm
from aoc.y2021.utils import load_data


def ints(x):
    return list(map(int, x))


def pprint(board):
    for row in board:
        print("".join([rev_key[c] for c in row]))


key = {
    ">": 1,
    "v": 2,
    ".": 0,
}
rev_key = {
    1: ">",
    2: "v",
    0: ".",
    3: "*",
    4: "o",
}


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    n_rows = len(d)
    n_cols = len(d[0])
    x = np.zeros((n_rows, n_cols))
    for idx, row in enumerate(d):
        x[idx] = [key[c] for c in row]

    for step in tqdm(range(10000)):
        start_x = x.copy()
        shift_left = np.roll(x, -1, axis=1)
        shift_right = np.roll(x, 1, axis=1)
        x[(start_x == 1) & (shift_left == 0)] = 0
        x[(shift_right == 1) & (start_x == 0)] = 1

        copy_x = x.copy()
        shift_up = np.roll(x, -1, axis=0)
        shift_down = np.roll(x, 1, axis=0)
        x[np.bitwise_and(copy_x == 2, shift_up == 0)] = 0
        x[np.bitwise_and(shift_down == 2, copy_x == 0)] = 2
        if np.all(x == start_x):
            print("done at step", step)
            break

    result_1 = step + 1

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day25.txt")
        test_answer_1 = 58
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
    d = load_data("day25.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()