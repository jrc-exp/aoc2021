""" Day 13 Solutions """

import sys
import numpy as np
from aoc.y2021.utils import load_data


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    xs, ys = [], []
    folds = []
    for row in d:
        if ',' in row:
            x, y = map(int, row.split(','))
            xs.append(x)
            ys.append(y)
        if 'along' in row:
            folds.append(row.split(' ')[-1].split('='))
    page = np.zeros((max(ys)+1, max(xs)+1), dtype=np.bool)
    for x, y in zip(xs, ys):
        page[y, x] = True
    for direction, dist in folds:
        dist = int(dist)
        if direction == 'x':
            page = page[:, :dist] | page[:, -dist:][:, ::-1]
        if direction == 'y':
            page = page[:dist] | page[-dist:][::-1]
        if not result_1:
            result_1 = np.sum(page)
    result_2 = np.sum(page)
    for r in page:
        x = ''
        for l in r:
            x += '#' if l else '.'
        print(x)

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day13.txt")
        test_answer_1 = 17
        test_answer_2 = 16
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day13.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
