""" Day 13 Solutions """

import sys
import numpy as np
from aoc.y2021.utils import load_data


def pageprint(page):
    print()
    for row in page:
        x = ""
        for char in row:
            x += "#" if char else "."
        print(x)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    xs, ys = [], []
    folds = []
    for row in d:
        if "," in row:
            x, y = list(map(int, row.split(",")))
            xs.append(x)
            ys.append(y)
        if "fold" in row:
            dir, dist = row.split(" ")[-1].split("=")
            folds.append((dir, int(dist)))

    print(list(zip(xs, ys)))
    print(folds)
    paper = np.zeros((max(ys) + 1, max(xs) + 1), dtype=np.bool)
    for x, y in zip(xs, ys):
        paper[y, x] = True
    # pageprint(paper)
    ct = 0
    for direction, dist in folds:
        ct += 1
        if direction == "x":
            a = paper[:, :dist]
            b = paper[:, -dist:]
            # pageprint(a)
            # pageprint(b)
            paper = a | b[:, ::-1]
            # pageprint(paper)
        if direction == "y":
            a = paper[:dist, :]
            b = paper[-dist:, :]
            # pageprint(a)
            # pageprint(b)
            paper = a | b[::-1, :]
            # pageprint(paper)
        if ct == 1:
            result_1 = np.sum(paper)

    pageprint(paper)

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day13.txt")
        test_answer_1 = 17
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
    d = load_data("day13.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
