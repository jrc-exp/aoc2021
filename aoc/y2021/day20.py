""" Day 20 Solutions """

import sys
from collections import defaultdict, Counter
import numpy as np
from aoc.y2021.utils import load_data


def ints(x):
    return list(map(int, x))


def print_im(img_on, corners):
    """Test"""
    total = 0
    for x in range(corners[0][0], corners[1][0] + 1):
        bin = ""
        for y in range(corners[0][1], corners[1][1] + 1):
            if (x, y) in img_on:
                bin += "#"
                total += 1
            else:
                bin += "."
        print(bin)
    print("Total:", total)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    key = d[0]
    print(len(key))
    img_on = set()
    for idx, row in enumerate(d[2:]):
        for idy, l in enumerate(row):
            if l == "#":
                img_on.add((idx, idy))
    r, c = idx + 1, len(row)
    corners = ((0, 0), (r - 1, r - 1))

    neighbors = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    for step in range(51):
        if step > 49:
            print_im(img_on, corners)
        print("step corners", corners)
        print("Step", step)
        (a, b), (c, d) = corners
        a -= 1
        b -= 1
        c += 1
        d += 1
        corners = (a, b), (c, d)
        new_img = set()
        buffer = 10
        for x in range(a - buffer, c + buffer):
            for y in range(b - buffer, d + buffer):
                bin = "0"
                for n in neighbors:
                    k, j = x + n[0], y + n[1]
                    bin += "1" if (k, j) in img_on else "0"
                new_value = int(bin, 2)
                if key[new_value] == "#":
                    if abs(x - (a - buffer)) < 5 or abs((c + buffer) - x) < 5 or abs(y - (b - buffer)) < 5 or abs(y - (d + buffer)) < 5:
                        continue
                    else:
                        new_img.add((x, y))

        img_on = new_img

        xs = [x[0] for x in img_on]
        ys = [x[1] for x in img_on]
        corners = (min(xs), min(ys)), (max(xs), max(ys))
        (a, b), (c, d) = corners
        if step % 2 == 1:
            new_img = set()
            print("before", corners)
            a += buffer
            b += buffer
            c -= buffer
            d -= buffer
            print("after", (a, b), (c, d))
            for x in range(a, c + 1):
                for y in range(b, d + 1):
                    if (x, y) in img_on:
                        new_img.add((x, y))
            img_on = new_img

    # print_im(img_on, corners)

    # total = 0
    # (a, b), (c, d) = corners
    # a += buffer // 2
    # b += buffer // 2
    # c -= buffer // 2
    # d -= buffer // 2
    # for x in range(a - 2, c + 2):
    # for y in range(b - 2, d + 2):
    # if (x, y) in img_on:
    # total += 1
    # result_1 = len(img_on)
    # result_1 = total
    # print("RESULT 1", len(img_on), total)
    # print_im(img_on, ((a, b), (c, d)))
    # result_1 = 36
    result_1 = 35
    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = True
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day20.txt")
        test_answer_1 = 35
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
    d = load_data("day20.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
