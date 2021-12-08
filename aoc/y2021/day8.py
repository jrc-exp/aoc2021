""" Day 8 Solutions

I AM NOT A PROUD MAN TODAY, BUT IT WORKS.

"""

import sys
import numpy as np
from aoc.y2021.utils import load_data


def count_lens(l, vals=[1, 4, 7, 8]):
    vals = [digit_to_lines[v] for v in vals]
    ans = sum([1 for d in l if len(d) in vals])
    return ans


digit_to_lines = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}

letters_in_number = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    rows = []
    for r in d:
        patterns, output = r.split("|")
        patterns = [p.strip() for p in patterns.strip().split(" ")]
        output = [o.strip() for o in output.strip().split(" ")]
        rows.append((patterns, output))
    result_1 = sum([count_lens(y) for (x, y) in rows])
    print("INPUT DATA:")
    print(rows)

    for patterns, output in rows:
        map_to_new = {
            "a": set("abcdefg"),
            "b": set("abcdefg"),
            "c": set("abcdefg"),
            "d": set("abcdefg"),
            "e": set("abcdefg"),
            "f": set("abcdefg"),
            "g": set("abcdefg"),
        }

        lens = [len(p) for p in patterns]
        one = patterns[lens.index(2)]
        seven = patterns[lens.index(3)]
        four = patterns[lens.index(4)]
        eight = patterns[lens.index(7)]
        top_line = list(set(seven) - set(one))[0]
        map_to_new["a"] = top_line
        map_to_new["c"] = set(one)
        map_to_new["f"] = set(one)
        for letter in letters_in_number[7]:
            map_to_new[letter] = set(map_to_new[letter]).intersection(set(seven))
        for letter in letters_in_number[4]:
            map_to_new[letter] = set(map_to_new[letter]).intersection(set(four))
        for letter in letters_in_number[8]:
            map_to_new[letter] = set(map_to_new[letter]).intersection(set(eight))
        for letter in "abdeg":
            map_to_new[letter] = map_to_new[letter] - set(one)
        for letter in "acefg":
            map_to_new[letter] = map_to_new[letter] - map_to_new["d"]

        lens = np.array(lens)
        zero_six_nine = [patterns[idx] for idx in np.where(np.array(lens) == 6)[0]]
        for letter in map_to_new["b"]:
            common = set(zero_six_nine[0]).intersection(set(zero_six_nine[1])).intersection(set(zero_six_nine[2]))
            if letter in common:
                map_to_new["b"] = set([letter])
                map_to_new["d"] = map_to_new["d"] - set([letter])

        two_three_five = [patterns[idx] for idx in np.where(np.array(lens) == 5)[0]]
        for case in two_three_five:
            if list(map_to_new["b"])[0] in case:
                five = case

        two_three = two_three_five
        two_three.pop(two_three.index(five))
        for letter in map_to_new["c"]:
            if letter in set(two_three[0]).intersection(set(two_three[1])):
                map_to_new["c"] = set([letter])
                map_to_new["f"] = map_to_new["f"] - set([letter])
        for letter in "bcdefg":
            map_to_new[letter] = map_to_new[letter] - map_to_new["a"]

        zero_six_nine = [patterns[idx] for idx in np.where(np.array(lens) == 6)[0]]
        for letter in map_to_new["g"]:
            common = set(zero_six_nine[0]).intersection(set(zero_six_nine[1])).intersection(set(zero_six_nine[2]))
            if letter in common:
                map_to_new["g"] = set([letter])
                map_to_new["e"] = map_to_new["e"] - set([letter])

        for l in map_to_new:
            map_to_new[l] = list(map_to_new[l])[0]

        inverted_letters_in_number = dict()
        for letter in letters_in_number:
            inverted_letters_in_number[letters_in_number[letter]] = letter
        inverted_map_to_new = dict()
        for letter in map_to_new:
            inverted_map_to_new[map_to_new[letter]] = letter

        weird_to_true = dict()
        for case in patterns:
            new_case = ""
            for letter in sorted(case):
                new_case += inverted_map_to_new[letter]
            new_case = "".join(sorted(new_case))
            weird_to_true["".join(sorted(case))] = inverted_letters_in_number[str(new_case)]

        digits = []
        for case in output:
            case = "".join(sorted(case))
            digits.append(weird_to_true[case])
        result_2 += int("".join([str(d) for d in digits]))

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        test_answer_1 = 26
        # d = load_data("test_day8.txt")
        # test_solution_1, test_solution_2 = solve(d)
        # assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"

        d = load_data("test_day8_p2.txt")
        test_answer_2 = 5353
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"

        test_answer_2 = 61229
        d = load_data("test_day8.txt")
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day8.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
