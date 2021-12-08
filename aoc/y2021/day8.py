""" Day 8 Solutions

I AM NOT A PROUD MAN TODAY, BUT IT WORKS.

"""

import sys
import numpy as np
from aoc.y2021.utils import load_data


def count_segments(l, vals=[1, 4, 7, 8]):
    vals = [n_segments_per_number[v] for v in vals]
    ans = sum([1 for d in l if len(d) in vals])
    return ans


n_segments_per_number = {
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

number_to_pattern = {
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


def get_matching_lengths(patterns, length):
    pattern_lens = [len(p) for p in patterns]
    return [patterns[idx] for idx in np.where(np.array(pattern_lens) == length)[0]]


def get_common(segments):
    if not segments:
        return set()
    segments = [set(s) for s in segments]
    common = segments[0]
    for segment in segments[1:]:
        common = common.intersection(segment)
    return common


def intersect(a, b):
    return set(a).intersection(set(b))


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    rows = []
    for r in d:
        patterns, output = r.split("|")
        patterns = [p.strip() for p in patterns.strip().split(" ")]
        output = [o.strip() for o in output.strip().split(" ")]
        rows.append((patterns, output))
    result_1 = sum([count_segments(y) for (x, y) in rows])
    # print("INPUT DATA:")
    # print(rows)

    for patterns, output in rows:
        # track a mapping of true segment to set of possible remaining segments
        seg_cands = {
            "a": set("abcdefg"),
            "b": set("abcdefg"),
            "c": set("abcdefg"),
            "d": set("abcdefg"),
            "e": set("abcdefg"),
            "f": set("abcdefg"),
            "g": set("abcdefg"),
        }

        pattern_lens = [len(p) for p in patterns]
        one = get_matching_lengths(patterns, 2)[0]
        seven = get_matching_lengths(patterns, 3)[0]
        four = get_matching_lengths(patterns, 4)[0]
        eight = get_matching_lengths(patterns, 7)[0]
        top_line = list(set(seven) - set(one))[0]

        # we know one letter for sure!
        seg_cands["a"] = top_line
        # we at least narrowed this down to two!
        seg_cands["c"] = set(one)
        seg_cands["f"] = set(one)
        # let's remove all of the letters these can't be:
        for letter in number_to_pattern[7]:
            seg_cands[letter] = intersect(seg_cands[letter], seven)
        for letter in number_to_pattern[4]:
            seg_cands[letter] = intersect(seg_cands[letter], four)
        for letter in number_to_pattern[8]:
            seg_cands[letter] = intersect(seg_cands[letter], eight)
        # we know c and f from "one" so it they can't be anywhere else:
        for letter in "abdeg":
            seg_cands[letter] = seg_cands[letter] - set(one)
        # we know b and d have been narrowed to a pair, so remove those from everywhere else:
        for letter in "acefg":
            seg_cands[letter] = seg_cands[letter] - seg_cands["d"]

        # zero/six/nine have 6 edges, and "b" is in all of them, but "d" is not!
        # so find b as the common of the two and deduce d:
        pattern_lens = np.array(pattern_lens)
        zero_six_nine = get_matching_lengths(patterns, 6)

        for letter in seg_cands["b"]:
            common = get_common(zero_six_nine)
            if letter in common:
                seg_cands["b"] = set([letter])
                seg_cands["d"] = seg_cands["d"] - set([letter])

        # two/three/five all have "5" edges and "b" is only in "5", so find it and know five
        two_three_five = get_matching_lengths(patterns, 5)
        for pattern in two_three_five:
            if list(seg_cands["b"])[0] in pattern:
                five = pattern

        # now you have two and three:
        two_three = two_three_five
        two_three.pop(two_three.index(five))
        # "c" is in both 2 and 3, but "f" is not, and they're now down to a pair of letters
        # so find "c" and know was "f" is:
        for letter in seg_cands["c"]:
            if letter in get_common(two_three):
                seg_cands["c"] = set([letter])
                seg_cands["f"] = seg_cands["f"] - set([letter])

        #  wipe the known ones:
        for letter in "bcdefg":
            seg_cands[letter] = seg_cands[letter] - seg_cands["a"]

        # now we just need to deduce g vs e which is down to a pair:
        # 0/6/9 all have "g" but not "e", so find "g" and know "e"
        zero_six_nine = get_matching_lengths(patterns, 6)
        for letter in seg_cands["g"]:
            common = get_common(zero_six_nine)
            if letter in common:
                seg_cands["g"] = set([letter])
                seg_cands["e"] = seg_cands["e"] - set([letter])

        # now we do lots of manipulations to map these back to their real numbers in a really awkward way:

        # seg_cands has a length 1 set of the correct answer at each location
        # convert to a simple letter to letter map:
        seg_cands = {l: next(iter(seg_cands[l])) for l in seg_cands}

        # we need more maps!
        pattern_to_number = {v: k for k, v in number_to_pattern.items()}
        mixed_seg_to_true_seg = {v: k for k, v in seg_cands.items()}

        mixed_pattern_to_number = dict()
        for mixed_pattern in patterns:
            # swap the letters:
            actual_pattern = [mixed_seg_to_true_seg[seg] for seg in mixed_pattern]
            # convert to alphabetical strings:
            actual_pattern = "".join(sorted(actual_pattern))
            mixed_pattern = "".join(sorted(mixed_pattern))
            # store it:
            mixed_pattern_to_number[mixed_pattern] = pattern_to_number[actual_pattern]

        # and now we can get the numbers:
        digits = []
        for pattern in output:
            pattern = "".join(sorted(pattern))
            digits.append(mixed_pattern_to_number[pattern])
        result_2 += int("".join([str(d) for d in digits]))

    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        test_answer_1 = 26
        d = load_data("test_day8.txt")
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"

        d = load_data("test_day8_p2.txt")
        test_answer_2 = 5353
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("Test Answer 2a: ", test_answer_2)
        print("My Test Answer 2a: ", test_solution_2)

        test_answer_2 = 61229
        d = load_data("test_day8.txt")
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2b: ", test_answer_2)
        print("My Test Answer 2b: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day8.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
