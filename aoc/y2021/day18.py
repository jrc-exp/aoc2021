""" Day 18 Solutions """

from copy import deepcopy
import sys
from collections import defaultdict, Counter
from ast import literal_eval
import numpy as np
from aoc.y2021.utils import load_data


def add(a, b):
    return [a, b]


def explode(a, quiet=True):
    """EXPLOSIONS"""
    a = deepcopy(a)
    # a,b,c,d / k,j,l.m
    if not quiet:
        print("EXPLODING", a)
    left_digit = None
    right_digit = None
    boom = False
    done = False
    for idb, b in enumerate(a):
        if done:
            break
        # depth 1
        if isinstance(b, int):
            if not boom:
                left_digit = (idb,)
            else:
                if not quiet:
                    print("right", right_digit, "val", b, done)
                right_digit = (idb,)
                done = True
            continue
        for idc, c in enumerate(b):
            if done:
                break
            # depth 2
            if isinstance(c, int):
                if not boom:
                    left_digit = (idb, idc)
                else:
                    right_digit = (idb, idc)
                    if not quiet:
                        print("right", right_digit, "val", c, done)
                    done = True
                continue
            for idd, d in enumerate(c):
                if done:
                    break
                # depth 3
                if isinstance(d, int):
                    if not boom:
                        left_digit = (idb, idc, idd)
                    else:
                        right_digit = (idb, idc, idd)
                        if not quiet:
                            print("right", right_digit, "val", d, done)
                        done = True
                    continue
                for ide, e in enumerate(d):
                    if done:
                        break
                    if isinstance(e, int):
                        if not boom:
                            left_digit = (idb, idc, idd, ide)
                        else:
                            right_digit = (idb, idc, idd, ide)
                            if not quiet:
                                print("right", right_digit, "val", e, done)
                            done = True
                    else:
                        # depth 4
                        if not boom:
                            boom = True
                            boom_box = (idb, idc, idd, ide)
                            if not quiet:
                                print("boom box", boom_box)
                        else:
                            right_digit = (idb, idc, idd, ide, 0)
                            if not quiet:
                                print("right", right_digit, "val", e[0], done)
                            done = True
    if not boom:
        return a
    left = get_idx(a, left_digit)
    boomer = get_idx(a, boom_box)
    right = get_idx(a, right_digit)
    if not quiet:
        print(left, boomer, right)
    x, y = boomer
    k, j, l, m = boom_box
    if right is not None:
        if len(right_digit) == 1:
            (q,) = right_digit
            a[q] = right + y
        if len(right_digit) == 2:
            q, w = right_digit
            a[q][w] = right + y
        if len(right_digit) == 3:
            q, w, e = right_digit
            a[q][w][e] = right + y
        if len(right_digit) == 4:
            q, w, e, r = right_digit
            a[q][w][e][r] = right + y
        if len(right_digit) == 5:
            q, w, e, r, t = right_digit
            a[q][w][e][r][t] = right + y
    if left is not None:
        if len(left_digit) == 1:
            (q,) = left_digit
            a[q] = left + x
        if len(left_digit) == 2:
            q, w = left_digit
            a[q][w] = left + x
        if len(left_digit) == 3:
            q, w, e = left_digit
            a[q][w][e] = left + x
        if len(left_digit) == 4:
            q, w, e, r = left_digit
            a[q][w][e][r] = left + x
    a[k][j][l][m] = 0
    return a


def split_int(a):
    return [int(np.floor(a / 2)), int(np.ceil(a / 2))]


def split(a, quiet=True):
    """DOING SPLITS"""
    a = deepcopy(a)
    # a,b,c,d / k,j,l.m
    if not quiet:
        print("SPLITTING", a)
    for idb, b in enumerate(a):
        # depth 1
        if isinstance(b, int):
            if b >= 10:
                a[idb] = split_int(b)
                return a
            continue
        for idc, c in enumerate(b):
            # depth 2
            if isinstance(c, int):
                if c >= 10:
                    a[idb][idc] = split_int(c)
                    return a
                continue
            for idd, d in enumerate(c):
                # depth 3
                if isinstance(d, int):
                    if d >= 10:
                        a[idb][idc][idd] = split_int(d)
                        return a
                    continue
                for ide, e in enumerate(d):
                    if isinstance(e, int):
                        if e >= 10:
                            a[idb][idc][idd][ide] = split_int(e)
                            return a
                        continue
    return a


def get_idx(a, idx_list):
    out = a
    if idx_list is None:
        return None
    for idx in idx_list:
        out = out[idx]
    return out


def reduce(a, quiet=True):
    while explode(a) != split(a):
        if explode(a) != a:
            a = explode(a, quiet)
        elif split(a) != a:
            a = split(a, quiet)
    return a


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    inputs = []
    for r in d:

        inputs.append(literal_eval(r))
        print(inputs[-1])

    """ # pylint: disable
    To reduce a snailfish number, you must repeatedly do the first action in this
    list that applies to the snailfish number:

    If any pair is nested inside four pairs, the leftmost such pair explodes.
    If any regular number is 10 or greater, the leftmost such regular number splits.

    To explode a pair, the pair's left value is added to the first regular number to the left
    of the exploding pair (if any), and the pair's right value is added to the first regular
    number to the right of the exploding pair (if any). Exploding pairs will always consist of
    two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.


    Here are some examples of a single explode action:

    [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4]
        (the 9 has no regular number to its left, so it is not added to any regular number).
    [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]]
        (the 2 has no regular number to its right, and so it is not added to any regular number).
    [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].
    [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
        (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].
    To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.


    Here is the process of finding the reduced result of [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]:

    after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
    after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
    after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
    after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

    Once no reduce actions apply, the snailfish number that remains is the actual
    result of the addition operation: [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

    """

    assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
    assert explode([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
    assert explode([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]) == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
    assert split([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
    assert split([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    assert explode([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    assert reduce(add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1])) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    test_list = [[1, 1], [2, 2], [3, 3], [4, 4]]
    out = test_list[0]
    for step, a in enumerate(test_list[1:]):
        out = add(out, a)
        out = reduce(out)
    print(out)

    assert out == [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]

    out = add(out, [5, 5])
    print("add 5,5", out)
    out = reduce(out)
    print("reduce", out)
    assert out == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]

    out = add(out, [6, 6])
    out = reduce(out)
    assert out == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]

    out = inputs[0]
    for step, a in enumerate(inputs[1:]):
        out = add(out, a)
        out = reduce(out)

    print(out)
    # assert out == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]

    def mag(a):
        if isinstance(a, int):
            return a
        if len(a) == 2:
            return mag(a[0]) * 3 + mag(a[1]) * 2

    assert mag([9, 1]) == 29, f"{mag([9, 1])} == 29"

    result_1 = mag(out)

    max_mag = 0
    from tqdm import tqdm

    inputs = list(inputs)
    for idx, a in tqdm(enumerate(inputs), total=len(inputs)):
        for idy, b in tqdm(enumerate(inputs), total=len(inputs), leave=False):
            if idx == idy:
                continue
            m = mag(reduce(add(a, b)))
            if m > max_mag:
                max_mag = m
            m = mag(reduce(add(b, a)))
            if m > max_mag:
                max_mag = m
    result_2 = max_mag

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
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


if __name__ == "__main__":
    main()
