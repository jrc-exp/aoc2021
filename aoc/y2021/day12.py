""" Day 12 Solutions """

import sys
from collections import defaultdict
import numpy as np
from aoc.y2021.utils import load_data
import os
from pprint import pprint

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass

    def pprint(*args, **kwargs):
        pass


def isBig(node: str):
    return node.upper() == node


def find_paths(node, traversed, nodes):
    traversed = traversed + [node]
    sub_paths = []
    if node == "end":
        return [traversed]
    for out in nodes[node]:
        if out == "start":
            pass
        elif out in traversed and not isBig(out):
            pass
        else:
            sub_paths += find_paths(out, traversed, nodes)
    return sub_paths


def find_paths_2(node, traversed, nodes):
    traversed = traversed + [node]
    too_visited = [n for n in traversed if not isBig(n) and traversed.count(n) == 2]
    double_visited = any(too_visited)
    sub_paths = []
    if node == "end":
        print(traversed)
        return [traversed]
    for out in nodes[node]:
        if out == "start":
            pass
        elif traversed.count(out) == 1 and double_visited and not isBig(out):
            pass
        elif traversed.count(out) >= 2 and not isBig(out):
            # print(traversed.count(out), out, traversed)
            pass
        else:
            sub_paths += find_paths_2(out, traversed, nodes)
    return sub_paths


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    nodes = defaultdict(list)
    for node in d:
        a, b = node.split("-")
        nodes[a].append(b)
        nodes[b].append(a)

    d = {}
    d.update(nodes)
    pprint(d)
    paths = find_paths("start", [], nodes)
    paths2 = find_paths_2("start", [], nodes)
    result_1 = len(paths)
    result_2 = len(paths2)
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
        d = load_data("test_day12.txt")
        test_answer_1 = 10
        test_answer_2 = 36
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        d = load_data("test_day12_2.txt")
        test_answer_1 = 19
        test_answer_2 = 103
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        d = load_data("test_day12_3.txt")
        test_answer_1 = 226
        test_answer_2 = 3509
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day12.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
