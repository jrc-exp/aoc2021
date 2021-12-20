""" Day 19 Solutions """
from math import perm
import sys
from collections import defaultdict, Counter
import numpy as np
from aoc.y2021.utils import load_data
from itertools import permutations


def ints(x):
    return list(map(int, x))


EULER_ROTS = [
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
    [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
    [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
    [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
    [[0, 0, -1], [1, 0, 0], [0, -1, 0]],
    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
    [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
    [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
    [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
    [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
    [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
    [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
    [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
    [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
    [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
    [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
    [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
    [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
    [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
    [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
]


def rotate(beacon, rotation):
    return rotation @ beacon


def rotate_array(beacons, rotation):
    return np.array([rotation @ m for m in beacons])


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    scanners = []
    ct = 0
    beacons = []
    for row in d[1:]:
        if "scanner" in row:
            ct += 1
            scanners.append(beacons)
            beacons = []
        if "," in row:
            beacons.append(np.array(ints(row.split(","))))
    scanners.append(np.array(beacons))
    scanners = np.array(scanners)

    beacon_diffs = []
    for scanner in scanners:
        beacon_pairs = permutations(scanner, 2)
        beacon_diff = set(np.prod(np.abs(a - b)) for (a, b) in beacon_pairs)
        beacon_diffs.append(beacon_diff)

    pair_maps = {k: {j: list() for j in range(len(scanners))} for k in range(len(scanners))}
    rotation_maps = {k: {j: list() for j in range(len(scanners))} for k in range(len(scanners))}
    offset_maps = {k: {j: list() for j in range(len(scanners))} for k in range(len(scanners))}

    matched = []
    for idx, d1 in enumerate(beacon_diffs):
        for idy, d2 in enumerate(beacon_diffs):
            if idx == idy:
                continue
            d1: set
            d2: set
            matches = d1.intersection(d2)
            if len(matches) >= (11 * 12 / 2):
                # if (idy, idx) not in matched:
                #     matched.append((idx, idy))
                matched.append((idx, idy))
                beacon_pairs_x = permutations(scanners[idx], 2)
                beacon_diff_x = [(np.prod(np.abs(a - b)), a, b) for (a, b) in beacon_pairs_x if np.prod(np.abs(a - b)) in matches]

                beacon_pairs_y = permutations(scanners[idy], 2)
                beacon_diff_y = [(np.prod(np.abs(a - b)), a, b) for (a, b) in beacon_pairs_y if np.prod(np.abs(a - b)) in matches]
                for bdx in beacon_diff_x:
                    for bdy in beacon_diff_y:
                        if bdx[0] == bdy[0]:
                            pair_maps[idx][idy].append(((bdx[1], bdx[2]), (bdy[1], bdy[2])))

    found = []
    from_to = defaultdict(list)
    for (x, y) in matched:
        for (a, b), (c, d) in pair_maps[x][y]:
            rotated = False
            for rot in EULER_ROTS:
                if np.all((a - b) == (rotate(c, rot) - rotate(d, rot))):
                    rotation_maps[x][y] = rot
                    rotated = True
                if np.all((a - b) == (rotate(d, rot) - rotate(c, rot))):
                    rotation_maps[x][y] = rot
                    rotated = True
            if not rotated:
                continue
            c = rotate(c, rotation_maps[x][y])
            d = rotate(d, rotation_maps[x][y])
            if np.all((a - c) == (b - d)):
                offset_maps[x][y] = a - c
            elif np.all((a - d) == (b - c)):
                offset_maps[x][y] = a - d
            found.append((x, y, rotation_maps[x][y], offset_maps[x][y]))
            from_to[(y, x)] = (rotation_maps[x][y], offset_maps[x][y])
            break

    for f in found:
        print(f)

    for x in range(1, len(scanners) + 1):
        pass

    def find_goal(start, path, from_to, n_nodes):
        if from_to[(start, 0)]:
            return path + [(start, 0)]
        for idx in range(n_nodes):
            visited = set(a for a, b in path)
            if start != idx and idx not in visited:
                if from_to[(start, idx)]:
                    goal_path = find_goal(idx, path + [(start, idx)], from_to, n_nodes)
                    if goal_path is not None:
                        return goal_path
        return None

    paths = []
    for idx in range(1, len(scanners)):
        path = find_goal(idx, [], from_to, len(scanners))
        print(idx, path)
        paths.append((idx, path))

    for (loc, path) in paths:
        origin = np.array([0, 0, 0])
        total_rot = np.eye(3)
        for p in path:
            (rot, offset) = from_to[p]
            origin = rot @ origin + offset
            total_rot = rot @ total_rot
        from_to[(loc, 0)] = (total_rot, origin)

    s = set([tuple(n) for n in scanners[0]])
    for idx, scanner in enumerate(scanners[1:], start=1):
        rot, off = from_to[(idx, 0)]
        s.update({tuple(rot @ np.array(n) + off) for n in scanner})

    result_1 = len(s)

    from_to[(0, 0)] = 0, np.array((0, 0, 0))
    maxd = 0
    for idx in range(len(scanners)):
        for idy in range(len(scanners)):
            r, o1 = from_to[(idx, 0)]
            r, o2 = from_to[(idy, 0)]
            if np.sum(np.abs(o2 - o1)) > maxd:
                maxd = np.sum(np.abs(o2 - o1))

    result_2 = maxd
    return result_1, result_2


def main():
    """Main function"""
    # load data:
    skip_test = False
    if not skip_test:
        print("**** TEST DATA ****")
        d = load_data("test_day19.txt")
        test_answer_1 = 79
        test_answer_2 = 3621
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day19.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
