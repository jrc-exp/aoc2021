""" Day 18 Solutions """

from copy import deepcopy
import sys
from collections import defaultdict, Counter
from ast import literal_eval
import numpy as np
from aoc.y2021.utils import load_data

import os

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def add(a, b):
    return [a, b]


def explode(a):
    """EXPLOSIONS"""
    left_digit = None
    right_digit = None
    boom = False
    done = False
    for idb, b in enumerate(a):
        if done:
            break
        # depth 1
        idx = (idb,)
        if isinstance(b, int):
            if not boom:
                left_digit = idx
            else:
                right_digit = idx
                done = True
            continue
        for idc, c in enumerate(b):
            if done:
                break
            # depth 2
            idx = (idb, idc)
            if isinstance(c, int):
                if not boom:
                    left_digit = idx
                else:
                    right_digit = idx
                    done = True
                continue
            for idd, d in enumerate(c):
                if done:
                    break
                idx = (idb, idc, idd)
                # depth 3
                if isinstance(d, int):
                    if not boom:
                        left_digit = idx
                    else:
                        right_digit = idx
                        done = True
                    continue
                for ide, e in enumerate(d):
                    if done:
                        break
                    idx = (idb, idc, idd, ide)
                    if isinstance(e, int):
                        if not boom:
                            left_digit = idx
                        else:
                            right_digit = idx
                            done = True
                    else:
                        # depth 4
                        idx = (idb, idc, idd, ide)
                        if not boom:
                            boom = True
                            boom_box = idx
                        else:
                            # special case because we know it can't be any deeper
                            right_digit = tuple(list(idx) + [0])
                            done = True
    if not boom:
        return a, boom
    left = get_idx(a, left_digit)
    boomer = get_idx(a, boom_box)
    right = get_idx(a, right_digit)
    x, y = boomer
    if right is not None:
        set_idx(a, right_digit, right + y)
    if left is not None:
        set_idx(a, left_digit, left + x)
    set_idx(a, boom_box, 0)
    return a, boom


def split_int(a):
    return [int(np.floor(a / 2)), int(np.ceil(a / 2))]


def split(a):
    """Recursive split"""
    if isinstance(a, int):
        if a >= 10:
            return split_int(a), True
        else:
            return a, False
    change = False
    for idb, _ in enumerate(a):
        a[idb], changed = split(a[idb])
        if changed:
            # we only split once and need to return!
            change = True
            break

    return a, change


def get_idx(a, idx_list):
    out = a
    if idx_list is None:
        return None
    for idx in idx_list:
        out = out[idx]
    return out


def set_idx(a, idx_list, val):
    if idx_list is None:
        return
    for idx in idx_list[:-1]:
        a = a[idx]
    a[idx_list[-1]] = val


def reduce(a):
    change = True
    while change:
        a, change = explode(a)
        if not change:
            a, change = split(a)
    return a


def mag(a):
    if isinstance(a, int):
        return a
    return mag(a[0]) * 3 + mag(a[1]) * 2


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    # print("INPUT DATA:")
    # print(d)
    inputs = []
    for r in d:
        inputs.append(literal_eval(r))
    # pylint: disable=pointless-string-statement
    # All the tests:

    """
    assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
    assert explode([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])[0] == [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
    assert explode([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]])[0] == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
    assert split([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])[0] == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
    assert split([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]])[0] == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    assert explode([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])[0] == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    assert reduce(add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1])) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    test_list = [[1, 1], [2, 2], [3, 3], [4, 4]]
    out = test_list[0]
    for a in test_list[1:]:
        out = add(out, a)
        out = reduce(out)

    assert out == [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]

    out = add(out, [5, 5])
    out = reduce(out)
    assert out == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]

    out = add(out, [6, 6])
    out = reduce(out)
    assert out == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]

    assert mag([9, 1]) == 29
    """

    out = inputs[0]
    for a in inputs[1:]:
        out = add(out, a)
        out = reduce(out)

    result_1 = mag(out)

    max_mag = 0

    inputs = []
    for r in d:
        inputs.append(literal_eval(r))
    for idx, a in enumerate(inputs):
        for idy, b in enumerate(inputs):
            if idx == idy:
                continue
            m = mag(reduce(add(deepcopy(a), deepcopy(b))))
            if m > max_mag:
                max_mag = m

    result_2 = max_mag

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    from argparse import ArgumentParser

    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day18.txt")
        test_answer_1 = 4140
        test_answer_2 = 3993
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day18.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)
    assert answer_1 == 4116
    assert answer_2 == 4638


if __name__ == "__main__":
    main()
