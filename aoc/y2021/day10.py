""" Day 10 Solutions """

import sys
import numpy as np
from aoc.y2021.utils import load_data


VALID = 0
CORRUPT = 1
INVALID = 2

OPENS = "[({<"
CLOSES = "])}>"
PAIRS = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">",
    "": "",
}
SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

P2_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def validate_chunk(chunk, start=""):
    # print("start", start, "chunk", chunk)
    if not chunk and not start:
        # end of strings
        return VALID, ""
    if not chunk and start:
        # still have one open
        return INVALID, PAIRS[start]

    char = chunk[0]
    if char in OPENS:
        out, chunk = validate_chunk(chunk[1:], start=char)
        if out == VALID:
            return validate_chunk(chunk, start)
        if out == CORRUPT:
            return CORRUPT, chunk
        if out == INVALID:
            return INVALID, chunk + PAIRS[start]

    if char == PAIRS[start]:
        # found a valid closing
        return VALID, chunk[1:]
    if char in CLOSES:
        # print("corrupt: expected", PAIRS[start], "got", char)
        score = SCORES[char]
        return CORRUPT, score


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    points = 0
    print("*****************************")
    scores_2 = []

    for chunk in d:
        # print("CHECKING CHUNK:", chunk)
        case, score = validate_chunk(chunk)
        if case == INVALID:
            # print("INVALID", score, chunk)
            s = 0
            for l in score:
                s *= 5
                s = int(s)
                s += P2_SCORES[l]
            scores_2.append(s)
        elif case == CORRUPT:
            # print("CORRUPT", score, chunk)
            points += score

    result_1 = points
    result_2 = np.median(scores_2)
    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day10.txt")
        test_answer_1 = 26397
        test_answer_2 = 288957
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day10.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
