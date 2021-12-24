""" Day 24 Solutions """

from math import trunc
import sys
from argparse import ArgumentParser
from collections import defaultdict, Counter
from itertools import permutations, product
import numpy as np
from aoc.y2021.utils import load_data


def ints(x):
    return list(map(int, x))


class ALU:
    """ALU"""

    def __init__(self) -> None:
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def set(self, var, val):
        setattr(self, var, val)

    def run(self, op):
        func, a, b = op.split(" ")
        func = self.__getattribute__(func)
        func(a, b)

    def get(self, var):
        return self.__getattribute__(var)

    def parse(self, var1, var2):
        try:
            val2 = int(var2)
        except ValueError:
            val2 = self.get(var2)
        val1 = self.get(var1)
        return val1, val2

    def inp(self, var, val):
        self.set(var, int(val))

    def add(self, var1, var2):
        a, b = self.parse(var1, var2)
        val = a + b
        self.set(var1, val)

    def mul(self, var1, var2):
        a, b = self.parse(var1, var2)
        val = a * b
        self.set(var1, val)

    def div(self, var1, var2):
        a, b = self.parse(var1, var2)
        assert b > 0
        val = trunc(a / b)
        self.set(var1, val)

    def mod(self, var1, var2):
        a, b = self.parse(var1, var2)
        assert b > 0
        assert a >= 0
        val = a % b
        self.set(var1, val)

    def eql(self, var1, var2):
        a, b = self.parse(var1, var2)
        val = 1 if a == b else 0
        self.set(var1, val)

    def reset(self):
        for v in ["x", "y", "z", "w"]:
            self.set(v, 0)

    def __repr__(self):
        return f"ALU: x={self.x}, y={self.y}, z={self.z}, w={self.w}"


def run_program(program, input_num, stop_input=0):
    """run a program"""
    alu = ALU()
    input_off = 0
    input_num = str(input_num)
    input_ct = 0
    for op in program:
        if op.startswith("inp"):
            if stop_input and stop_input == input_ct:
                break
            op += " " + input_num[input_off]
            input_off += 1
            input_ct += 1
        alu.run(op)

    return alu


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)

    input_num = 13579246899999

    program = ["inp x", "mul x -1"]
    z = run_program(program, input_num)
    print(z, program)

    program = ["inp z", "inp x", "mul z 3", "eql z x"]
    z = run_program(program, input_num)
    print(z, program)

    program = [
        "inp w",
        "add z w",
        "mod z 2",
        "div w 2",
        "add y w",
        "mod y 2",
        "div w 2",
        "add x w",
        "mod x 2",
        "div w 2",
        "mod w 2",
    ]
    for num in range(1, 10):
        alu = run_program(program, num, False)
        bin_num = format(num, "04b")
        assert alu.z == int(bin_num[3]), "z"
        assert alu.w == int(bin_num[0]), "w"
        assert alu.x == int(bin_num[1]), "x"
        assert alu.y == int(bin_num[2]), "y"
    # pylint: disable=pointless-string-statement

    # I'm not sure why this worked, but it did:
    best_z = np.inf
    best_num = int("".join(["9"] * 14))
    for stop_input in range(1, 15):
        # print("stop after", stop_input)
        best_z = run_program(d, best_num).z
        for _ in range(10):
            for digit in reversed(range(14)):
                for n in reversed(range(1, 10)):
                    num = list(str(best_num))
                    num[digit] = str(n)
                    num = int("".join(num))
                    alu = run_program(d, num, stop_input=stop_input)
                    # print(num, alu.z)
                    if alu.z < best_z:
                        best_num = num
                        best_z = alu.z
                        print(best_num, best_z)
                        if best_z == 0:
                            print("found one!")

    # But once we have a "zero" number we can find the bigger and
    # smaller ones easily because the output is only ever affected by
    # pairs of digits at most - so wiggle two digits and stay at zero
    changed = True
    while changed:
        changed = False
        for d1 in range(14):
            for d2 in range(14):
                num = list(str(best_num))
                if num[d1] == "9" or num[d2] == "9":
                    continue
                num[d1] = str(int(num[d1]) + 1)
                num[d2] = str(int(num[d2]) + 1)
                num = int("".join(num))
                alu = run_program(d, num, stop_input=stop_input)
                if alu.z == 0:
                    changed = True
                    best_num = num
                    print(best_num, "bigger and better")
                    break
    print("Result 1", best_num)

    result_1 = best_num
    changed = True
    while changed:
        changed = False
        for d1 in range(14):
            for d2 in range(14):
                num = list(str(best_num))
                if num[d1] == "1" or num[d2] == "1":
                    continue
                num[d1] = str(int(num[d1]) - 1)
                num[d2] = str(int(num[d2]) - 1)
                num = int("".join(num))
                alu = run_program(d, num, stop_input=stop_input)
                if alu.z == 0:
                    best_num = num
                    print(best_num, "smaller and faster")
                    changed = True
    result_2 = best_num
    print("Result 2", best_num)

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    d = load_data("day24.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
