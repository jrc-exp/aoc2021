""" Day 21 Solutions """

import sys
from collections import defaultdict, Counter
import numpy as np
from aoc.y2021.utils import load_data

import os

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def ints(x):
    return list(map(int, x))


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    pos = []
    scores = []
    for row in d:
        pos.append(int(row.split(" ")[-1]))
        scores.append(0)
    start_pos = tuple(pos)
    die = 0
    turn = 0
    win = False
    while turn < 1000 and not win:
        for player in range(2):
            if win:
                break
            roll = 0
            for _ in range(3):
                turn += 1
                die += 1
                if die == 101:
                    die = 1
                roll += die
            pos[player] += roll
            pos[player] = ((pos[player] - 1) % 10) + 1
            scores[player] += pos[player]
            if scores[player] >= 1000:
                result_1 = scores[(player + 1) % 2] * turn
                win = True

    # part 2
    rolls = [sum([k, j, m]) for k in range(1, 4) for j in range(1, 4) for m in range(1, 4)]
    roll_counts = Counter(rolls)
    states = {}
    states[((0, 0), start_pos)] = 1
    wins = [0, 0]
    while states:
        for player in [0, 1]:
            next_states = defaultdict(lambda: 0)
            for roll in roll_counts:
                for (scores, locs), count in states.items():
                    count = count * roll_counts[roll]
                    locs, scores = list(locs), list(scores)
                    locs[player] = (locs[player] + roll - 1) % 10 + 1
                    scores[player] += locs[player]
                    if scores[player] >= 21:
                        wins[player] += count
                    else:
                        next_states[(tuple(scores), tuple(locs))] += count
            states = next_states

    result_2 = max(wins)

    return result_1, result_2


def main():
    """Main function"""
    from argparse import ArgumentParser

    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day21.txt")
        test_answer_1 = 739785
        test_answer_2 = 444356092776315
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day21.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
