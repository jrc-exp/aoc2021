""" Day 3 Solutions """

from aoc.y2021.utils import load_data
from collections import Counter
import os

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def main():
    """Main function"""
    # load data:
    d = load_data("day3.txt")
    # print("INPUT DATA:")
    # print(d)
    # print("Day 3 Stub!")

    bit_len = 12
    gamma = []
    epsilon = []
    for idx in range(bit_len):
        ctr = Counter([x[idx] for x in d])
        if ctr["1"] > ctr["0"]:
            gamma.append(1)
            epsilon.append(0)
        else:
            gamma.append(0)
            epsilon.append(1)
    gamma_val = sum([2 ** idx * x for (idx, x) in enumerate(gamma[::-1])])
    epsilon_val = sum([2 ** idx * x for (idx, x) in enumerate(epsilon[::-1])])
    print(gamma, epsilon)
    print(gamma_val, epsilon_val)
    print(gamma_val * epsilon_val)

    temp_d = d
    for idx in range(bit_len):
        ctr = Counter([x[idx] for x in temp_d])
        if ctr["1"] >= ctr["0"]:
            temp_d = [x for x in temp_d if x[idx] == "1"]
        else:
            temp_d = [x for x in temp_d if x[idx] == "0"]

    oxygen = temp_d[0]
    print("oxygen", temp_d[0])
    oxygen_val = sum([2 ** idx * int(x) for (idx, x) in enumerate(oxygen[::-1])])
    print("oxygen_val", oxygen_val)

    temp_d = d
    for idx in range(bit_len):
        if len(temp_d) == 1:
            break
        ctr = Counter([x[idx] for x in temp_d])
        if ctr["0"] > ctr["1"]:
            temp_d = [x for x in temp_d if x[idx] == "1"]
        else:
            temp_d = [x for x in temp_d if x[idx] == "0"]
    co2rating = temp_d[0]
    print("co2rating", temp_d[0])
    co2_val = sum([2 ** idx * int(x) for (idx, x) in enumerate(co2rating[::-1])])
    print("co2_val", co2_val)
    print(co2_val, oxygen_val, co2_val * oxygen_val)


if __name__ == "__main__":
    main()
