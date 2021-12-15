""" Day 14 Solutions """

import sys
from typing import Counter
from aoc.y2021.utils import load_data


def digraphs_in(s):
    return [s[idx : idx + 2] for idx in range(len(s) - 1)]


def solve(d):
    """actual solution with puzzle input"""
    from time import time
    from collections import defaultdict

    now = time()
    result_1, result_2 = 0, 0
    initial_str = d[0]
    transforms = []
    for row in d[2:]:
        transforms.append(row.split(" -> "))

    """
    PART 1 THE INEFFICIENT WAY
    string: str = d[0]
    for _ in range(10):
        holder = [
            "",
        ] * len(string)
        for pair, letter in transforms:
            try:
                for idx in range(len(string) - 1):
                    if string[idx : idx + 2] == pair:
                        holder[idx] = letter
            except ValueError:
                pass
        string = "".join([k + l for (k, l) in zip(string, holder)])
    counts = sorted([string.count(x) for x in set(string)])
    result_1 = counts[-1] - counts[0]
    """

    """
    PART 2 THE EFFICIENT WAY
    """
    di_list = digraphs_in(initial_str)
    counts = Counter(di_list)
    transform_map = {pair: letter for (pair, letter) in transforms}
    for step in range(0, 1000):

        new_counts = defaultdict(lambda: 0)
        for digraph in counts:
            insertion = transform_map[digraph]
            new_counts[digraph[0] + insertion] += counts[digraph]
            new_counts[insertion + digraph[1]] += counts[digraph]
        counts = new_counts

        if step in [9, 39, 999]:
            # if step in [9, 39, 1000]:
            letters = set(out for _, out in transforms)
            count_per_letter = {l: 0 for l in letters}
            for digraph in counts:
                for letter in count_per_letter:
                    count_per_letter[letter] += counts[digraph] * digraph.count(letter)
            totals = sorted(v for _, v in count_per_letter.items())
        if step == 9:
            result_1 = (totals[-1] - totals[0]) // 2 + 1
        if step == 39:
            result_2 = (totals[-1] - totals[0]) // 2 + 1
    letters = set(out for _, out in transforms)
    count_per_letter = {l: 0 for l in letters}
    for digraph in counts:
        for letter in count_per_letter:
            count_per_letter[letter] += counts[digraph] * digraph.count(letter)
    totals = sorted(v for _, v in count_per_letter.items())
    print(f"After {step+1} Iterations:")
    print((totals[-1] - totals[0]) // 2 + 1)

    print(f"Core Alg: Elapsed {time() - now:.3f}s")

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day14.txt")
        test_answer_1 = 1588
        test_answer_2 = 2188189693529
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day14.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
