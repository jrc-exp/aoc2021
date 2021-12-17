""" Day 17 Solutions """

import sys
from collections import defaultdict, Counter
import numpy as np
from aoc.y2021.utils import load_data


def ints(x):
    return list(map(int, x))

def sim(vx, vy, xl, xh, yl, yh):
    """ Run a sim """
    above_or_in = True
    x, y = (0, 0)
    maxy = -np.inf
    went_in = False
    while above_or_in or vy > 0:
        x, y = x + vx, y + vy
        if y > maxy:
            maxy = y
        if vx > 0:
            vx -= 1
        if vx < 0:
            vx += 1
        vy -= 1
        if y >= min(yl, yh):
            above_or_in = True
        else:
            # could still be going up
            above_or_in = False
        if xl <= x <= xh and yl <= y <= yh:
            went_in = True
            break
    return went_in, maxy


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0

    print("INPUT DATA:")
    print(d)
    text = d[0]
    x, y = text[text.index("x") :].split(", ")
    x = ints(x.split("=")[1].split(".."))
    y = ints(y.split("=")[1].split(".."))
    xl, xh = x
    yl, yh = y
    # can solve directly for vxmin and vxmax:
    vx_min = int(np.ceil(-0.5 + np.sqrt(0.5 ** 2 + 4 * 0.5 * xl)))
    vx_max = xh
    # if larger than this vymax it will potentially jump over the area in one step of the fall, I believe
    # not sure if this would hold if the target area was somewhere up high though because you could fly way above and fall down into it...
    # but these are negative so...
    vymax = max(abs(yh), abs(yl))
    print(vx_min, vx_max)

    # try starting with the highest posssible until one goes in the zone:
    vy_try = vymax
    while True:
        vx = vx_min
        vy = vy_try
        x, y = (0, 0)
        went_in, maxy = sim(vx, vy, xl, xh, yl, yh)
        if went_in:
            break
        vy_try -= 1
    result_1 = maxy

    # find the x's that ever enter the zone:
    in_zone_vxs = []
    for vx in range(vx_min, vx_max + 1):
        vxi = vx
        x_pos = 0
        step = 0
        while vx > -1:
            step += 1
            x_pos += vx
            if xl <= x_pos <= xh:
                in_zone_vxs.append(vxi)
                break
            vx -= 1

    # check all possible y's for each x zone:
    vymin = yl if yl > 0 else yl
    in_set = set()
    for vx in in_zone_vxs:
        for vy in range(vymin, vymax):
            x, y = (0, 0)
            maxy = -np.inf
            went_in, _ = sim(vx, vy, xl, xh, yl, yh)
            if went_in:
                in_set.add((vx, vy))

    result_2 = len(in_set)

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day17.txt")
        test_answer_1 = 45
        test_answer_2 = 112
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day17.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
