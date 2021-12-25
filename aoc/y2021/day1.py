""" Day 1 Solutions """

import numpy as np

from aoc.y2021.utils import load_data
import os

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def main():
    """Main function"""
    # load data:
    d = load_data("day1.txt", "int")

    # answer 1:
    answer_1 = np.sum(np.diff(d) > 0)

    # answer 2:
    win_d = np.convolve(d, np.ones(3))[2:-2]
    answer_2 = np.sum(np.diff(win_d) > 0)

    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)


if __name__ == "__main__":
    main()
