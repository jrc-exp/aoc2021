""" Day 11 Solutions """

import os

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
    for k in d:
        print(k)
    lights = np.zeros((12, 12))
    idx = (slice(1, 11), slice(1, 11))  # syntax helper
    lights[idx] = [[int(k) for k in r] for r in d]

    flashes = 0
    for step in range(10000):
        flashed = np.zeros_like(lights)
        lights += 1
        while np.any((lights[idx] > 9) & (flashed[idx] == 0)):
            (x, *_), (y, *_) = np.where(lights[idx] > 9)
            x += 1
            y += 1
            lights[x - 1 : x + 2, y - 1 : y + 2] += 1
            flashed[x, y] = 1
            flashes += 1
            lights[flashed == 1] = 0

        if np.all(flashed[idx]):
            result_2 = step + 1
            break

        if step == 100 - 1:
            result_1 = flashes

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day11.txt")
        test_answer_1 = 1656
        test_answer_2 = 195
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day11.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
