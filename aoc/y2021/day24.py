""" Day 24 Solutions """

import os
from argparse import ArgumentParser
from math import trunc

import numpy as np

from aoc.y2021.utils import load_data

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
            except ValueError:
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

    # I'm not entirely sure why this worked, but it did:
    # if you search the digits in order from left to right and 1 to 10 per digit,
    # you need to start from 11111111111111, butif you search each iterator "reversed"
    # you have to start from 99999999999999! I don't know why!
    # But ironically this seems to always find... the minimum number!
    best_z = np.inf
    best_num = int("".join(["1"] * 14))
    for stop_input in range(1, 15):
        best_z = run_program(d, best_num).z
        for digit in range(stop_input):
            for n in range(1, 10):
                num = list(str(best_num))
                num[digit] = str(n)
                num = int("".join(num))
                alu = run_program(d, num, stop_input=stop_input)
                if alu.z < best_z:
                    best_num = num
                    best_z = alu.z
                    if alu.z == 0:
                        print("Found a zero at:", best_num)

    # But once we have a "zero" number we can deduce the rules!
    linked_digits = set()
    for d1 in range(14):
        for d2 in range(14):
            if d1 == d2:
                continue
            num = list(str(best_num))
            if num[d1] == "9" or num[d2] == "9":
                num[d1] = str(int(num[d1]) - 1)
                num[d2] = str(int(num[d2]) - 1)
            else:
                num[d1] = str(int(num[d1]) + 1)
                num[d2] = str(int(num[d2]) + 1)
            num = int("".join(num))
            alu = run_program(d, num, stop_input=stop_input)
            if alu.z == 0:
                linked_digits.add((min(d1, d2), max(d1, d2)))
                break

    # Use the rules:
    min_number = [0] * 14
    max_number = [0] * 14
    for pair in sorted(list(linked_digits)):
        a, b = pair
        num = str(best_num)
        rule = int(num[b]) - int(num[a])
        print(f"Rule: D[{a}] {' ' if a+1 < 10 else ''}{'+' if rule>0 else '-'} {abs(rule)} = D[{b}]")
        if rule > 0:
            min_number[a] = 1
            min_number[b] = 1 + rule
            max_number[a] = 9 - rule
            max_number[b] = 9
        else:
            min_number[b] = 1
            min_number[a] = 1 - rule
            max_number[b] = 9 + rule
            max_number[a] = 9

    # Make sure something wasn't d[x] + 8 = d[y]:
    # if it was it can't big wiggled and it's a 1 paired with a 9
    if len(linked_digits) < 7:
        zero_num = str(best_num)
        for digit in range(14):
            for pair in linked_digits:
                break
            else:
                min_number[digit] = zero_num[digit]
                max_number[digit] = zero_num[digit]

    result_1 = sum(x * 10 ** p for p, x in enumerate(reversed(max_number)))
    result_2 = sum(x * 10 ** p for p, x in enumerate(reversed(min_number)))

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
    assert answer_1 == 59998426997979
    assert answer_2 == 13621111481315


if __name__ == "__main__":
    main()
