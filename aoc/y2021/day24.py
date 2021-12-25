""" Day 24 Solutions """

from math import trunc
import sys
from argparse import ArgumentParser
from collections import defaultdict, Counter
from itertools import permutations, product
import numpy as np
from aoc.y2021.utils import load_data

import os

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def ints(x):
    return list(map(int, x))


class ALU:
    """ALU"""

    def __init__(self) -> None:
        self.reset()
        self.func_map = {
            "inp": self.inp,
            "add": self.add,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "eql": self.eql,
        }

    @property
    def x(self):
        return self.vars["x"]

    @property
    def y(self):
        return self.vars["y"]

    @property
    def w(self):
        return self.vars["w"]

    @property
    def z(self):
        return self.vars["z"]

    def run(self, op):
        func, a, b = op
        func = self.func_map[func]
        func(a, b)

    def parse(self, var1, var2):
        val2 = self.vars.get(var2, var2)
        val1 = self.vars[var1]
        return val1, val2

    def inp(self, var, val):
        self.vars[var] = val

    def add(self, var1, var2):
        a, b = self.parse(var1, var2)
        val = a + b
        self.vars[var1] = val

    def mul(self, var1, var2):
        a, b = self.parse(var1, var2)
        val = a * b
        self.vars[var1] = val

    def div(self, var1, var2):
        a, b = self.parse(var1, var2)
        assert b > 0
        val = trunc(a / b)
        self.vars[var1] = val

    def mod(self, var1, var2):
        a, b = self.parse(var1, var2)
        assert b > 0
        assert a >= 0
        val = a % b
        self.vars[var1] = val

    def eql(self, var1, var2):
        a, b = self.parse(var1, var2)
        val = 1 if a == b else 0
        self.vars[var1] = val

    def reset(self):
        self.vars = {v: 0 for v in "xyzw"}

    def __repr__(self):
        return f"ALU: x={self.vars['x']}, y={self.vars['y']}, z={self.vars['z']}, w={self.vars['w']}"


def run_program(program, input_num, stop_input=0):
    """run a program"""
    alu = ALU()
    input_off = 0
    input_num = str(input_num)
    input_ct = 0
    for op in program:
        if op[0] == "inp":
            if stop_input and stop_input == input_ct:
                break
            op[-1] = int(input_num[input_off])
            input_off += 1
            input_ct += 1
        alu.run(op)

    return alu


def clean_program(d):
    """pre-compute some stuff for speed later"""
    for idx, row in enumerate(d):
        d[idx] = row.split(" ")
        for idy, c in enumerate(d[idx]):
            try:
                d[idx][idy] = int(c)
            except:
                pass
            if len(d[idx]) == 2:
                d[idx].append("")
    return d


def solve(d, skip_tests=False):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    d = clean_program(d)

    if not skip_tests:
        input_num = 13579246899999
        program = ["inp x", "mul x -1"]
        program = clean_program(program)
        alu = run_program(program, input_num)
        assert alu.z == 0
        program = ["inp z", "inp x", "mul z 3", "eql z x"]
        program = clean_program(program)
        alu = run_program(program, input_num)
        assert alu.z == 1

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
        program = clean_program(program)
        for num in range(1, 10):
            alu = run_program(program, num, False)
            bin_num = format(num, "04b")
            assert alu.z == int(bin_num[3]), "z"
            assert alu.w == int(bin_num[0]), "w"
            assert alu.x == int(bin_num[1]), "x"
            assert alu.y == int(bin_num[2]), "y"
    # pylint: disable=pointless-string-statement

    # I'm not entirely sure why this worked, but it did:
    best_z = np.inf
    # it doesn't actually matter what number you start with:
    # this seems to find the minimum number directly
    best_num = int("".join(["9"] * 14))
    for stop_input in range(1, 15):
        best_z = run_program(d, best_num).z
        for digit in reversed(range(14)):
            for n in reversed(range(1, 10)):
                num = list(str(best_num))
                num[digit] = str(n)
                num = int("".join(num))
                alu = run_program(d, num, stop_input=stop_input)
                if alu.z < best_z:
                    best_num = num
                    best_z = alu.z
                    if best_z == 0 and stop_input == 14:
                        print("Found a zero!")
                        print(best_num, best_z, alu)

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
                    break
    result_1 = best_num

    # now we search for the min, but it was apparently what we found
    # earlier!
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
                    changed = True
    result_2 = best_num

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
