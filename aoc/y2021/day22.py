""" Day 22 Solutions """

import sys
from collections import defaultdict, Counter
from itertools import permutations, product
from typing import List
import numpy as np
from aoc.y2021.utils import load_data
import os

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def ints(x):
    return list(map(int, x))


class Cube:
    """Cube"""

    def __init__(self, x, y, z, action):
        self.x = x
        self.y = y
        self.z = z
        self.coords = ((x[0], x[1]), (y[0], y[1]), (z[0], z[1]))
        assert (x[1] - x[0]) > -1, f"width must be positive {self.coords}"
        assert (y[1] - y[0]) > -1, f"width must be positive {self.coords}"
        assert (z[1] - z[0]) > -1, f"width must be positive {self.coords}"
        self.action = 1 if action == "on" else 0
        self.exposed = False
        self.off_cubes = []
        self.covered = False

    def __repr__(self):
        return f"Cube({self.coords}), vol={self.vol}, on_vol={self.on_vol}, #off_cubes={len(self.off_cubes)}"

    @property
    def off_ct(self):
        if self.covered:
            return self.vol
        return sum([c.vol for c in self.off_cubes])

    @property
    def vol(self):
        return (self.x[1] - self.x[0] + 1) * (self.y[1] - self.y[0] + 1) * (self.z[1] - self.z[0] + 1)

    @property
    def on_vol(self):
        return self.vol - self.off_ct

    def inside(self, c):
        """true self is inside of c"""
        return all(self.inside_1d(c, dim) for dim in ["x", "y", "z"])

    def overlap(self, c):
        return all(self.overlap_1d(c, dim) for dim in ["x", "y", "z"])

    def inside_1d(self, c, dim):
        (a1, a2) = self.__getattribute__(dim)
        (b1, b2) = c.__getattribute__(dim)
        if b1 <= a1 and a2 <= b2:
            return True
        return False

    def overlap_1d(self, c, dim):
        (a1, a2) = self.__getattribute__(dim)
        (b1, b2) = c.__getattribute__(dim)
        if b2 < a1 or b1 > a2:
            return False
        return True

    def intersection(self, c):
        (x1, y1, z1) = self.coords
        (x2, y2, z2) = c.coords
        x = (max(x1[0], x2[0]), min(x1[1], x2[1]))
        y = (max(y1[0], y2[0]), min(y1[1], y2[1]))
        z = (max(z1[0], z2[0]), min(z1[1], z2[1]))
        return Cube(x, y, z, "off")

    def calc_on_volume(self, cubes):
        if not self.action:
            return
        for c in cubes:
            if self.inside(c):
                self.covered = True
                return
        for c in cubes:
            if self.overlap(c):
                self.add_off_cube(self.intersection(c))

    def add_off_cube(self, c):
        """and an off cube inside of this cube"""
        for cube in self.off_cubes:
            if c.inside(cube):
                return
        for cube in self.off_cubes:
            if cube.inside(c):
                # if existing off_cube is INSIDE c, swallow it!
                self.off_cubes.remove(cube)
                # and start again
                return self.add_off_cube(c)
            if c.overlap(cube):
                cubes = c.nonintersection(cube)
                for tiny_cube in cubes:
                    self.add_off_cube(tiny_cube)
                return
        self.off_cubes.append(c)

    def nonintersection(self, c):
        """return list of cubes of the remainder after removing c of self"""
        (x1, y1, z1) = self.coords
        (x2, y2, z2) = c.coords
        # have to return the cube on each of the six faces...
        x = (max(x1[0], x2[0]), min(x1[1], x2[1]))
        y = (max(y1[0], y2[0]), min(y1[1], y2[1]))
        z = (max(z1[0], z2[0]), min(z1[1], z2[1]))
        # take the x-face first:
        # print("nonintersect", "\nA:", self, "\nB:", c)
        cubes = []
        if x[0] - x1[0] > 0:
            cubes.append(Cube((x1[0], x[0] - 1), y1, z1, "off"))
            # print("Left X", cubes[-1])
        if x1[1] - x[1] > 0:
            cubes.append(Cube((x[1] + 1, x1[1]), y1, z1, "off"))
            # print("Right X", cubes[-1])
        if y[0] - y1[0] > 0:
            cubes.append(Cube(x, (y1[0], y[0] - 1), z1, "off"))
            # print("Left Y", cubes[-1])
        if y1[1] - y[1] > 0:
            cubes.append(Cube(x, (y[1] + 1, y1[1]), z1, "off"))
            # print("Right Y", cubes[-1])
        if z[0] - z1[0] > 0:
            cubes.append(Cube(x, y, (z1[0], z[0] - 1), "off"))
            # print("Left Z", cubes[-1])
        if z1[1] - z[1] > 0:
            cubes.append(Cube(x, y, (z[1] + 1, z1[1]), "off"))
            # print("Right Z", cubes[-1])

        # print()
        return cubes


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    # print(d)
    xs, ys, zs = [], [], []
    actions = []
    for row in d:
        action = row.split(" ")[0]
        actions.append(action)
        x = row[row.index("x") + 2 : row.index("y") - 1]
        y = row[row.index("y") + 2 : row.index("z") - 1]
        z = row[row.index("z") + 2 :]
        xs.append(ints((x.split(".")[0], x.split(".")[-1])))
        ys.append(ints((y.split(".")[0], y.split(".")[-1])))
        zs.append(ints((z.split(".")[0], z.split(".")[-1])))

    # part 1
    grid = np.zeros((150, 150, 150))
    offset = 50
    for (x, y, z, action) in zip(xs, ys, zs, actions):
        if np.all(np.abs(x) <= 50) and np.all(np.abs(y) <= 50) and np.all(np.abs(z) <= 50):
            grid[x[0] + offset : x[1] + offset + 1, y[0] + offset : y[1] + offset + 1, z[0] + offset : z[1] + offset + 1,] = (
                1 if action == "on" else 0
            )
        else:
            result_1 = int(np.sum(grid))
            break

    cubes = []
    on_cubes = []
    for (x, y, z, action) in reversed(list(zip(xs, ys, zs, actions))):
        c = Cube(x, y, z, action)
        c.calc_on_volume(cubes)
        if c.action:
            on_cubes.append(c)
        cubes.append(c)

    result_2 = sum([c.on_vol for c in on_cubes])

    return result_1, result_2


def main():
    """Main function"""
    from argparse import ArgumentParser

    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day22.txt")
        test_answer_1 = 590784
        test_answer_2 = 0
        test_solution_1, _ = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        test_answer_2 = 2758514936282235
        d = load_data("test_day22p2.txt")
        _, test_solution_2 = solve(d)
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day22.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)
    assert answer_1 == 591365
    assert answer_2 == 1211172281877240


if __name__ == "__main__":
    main()
