""" Day 20 Solutions """
from aoc.y2021.utils import load_data

NBR8 = [
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


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0

    key = d[0]
    img_on = set()
    for idx, row in enumerate(d[2:]):
        for idy, l in enumerate(row):
            if l == "#":
                img_on.add((idx, idy))

    # assuming square grid everywhere:
    grid_sz = len(d) - 1
    for step in range(50):
        low, high = -1 - step, grid_sz + step
        # if we have the '#' at zero, add two rings of "#'s":
        if key[0] == "#":
            for x in (low, low - 1, high, high + 1):
                for y in range(low - 1, high + 3):
                    if step % 2 == 1:
                        img_on.add((x, y))
                        img_on.add((y, x))
        new_img = set()
        # compute one step outward in x/y each step:
        # the infinite cells will not matter outside of this ring on the even steps:
        for x in range(low, high + 1):
            for y in range(low, high + 1):
                word = "".join(["1" if (x + n[0], y + n[1]) in img_on else "0" for n in NBR8])
                if key[int(word, 2)] == "#":
                    new_img.add((x, y))
        img_on = new_img

        if step == 1:
            result_1 = len(img_on)
    result_2 = len(img_on)

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
    assert answer_1 == 5291
    assert answer_2 == 16665
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
