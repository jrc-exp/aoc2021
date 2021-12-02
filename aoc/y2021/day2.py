""" Day 2 Solutions """

from aoc.y2021.utils import load_data


def calculate_moves_one(d):
    x, depth = 0, 0
    for move in d:
        direction, dist = move.split(' ')
        if direction == 'forward':
            x += int(dist)
        if direction == 'up':
            depth -= int(dist)
        if direction == 'down':
            depth += int(dist)
    return x, depth

def calculate_moves_two(d):
    x, depth, aim = 0, 0, 0
    for move in d:
        direction, dist = move.split(' ')
        if direction == 'forward':
            x += int(dist)
            depth += aim*int(dist)
        if direction == 'up':
            aim -= int(dist)
        if direction == 'down':
            aim += int(dist)
    return x, depth

def main():
    """ Main function """
    # load data:
    d = load_data("day2.txt")
    x, depth = calculate_moves_one(d)
    print('x', x, 'depth', depth)
    print('answer 1:', x*depth)

    x, depth = calculate_moves_two(d)
    print('x', x, 'depth', depth)
    print('answer 2:', x*depth)


if __name__ == "__main__":
    main()
