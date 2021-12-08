""" Day 6 Solutions """

from aoc.y2021.utils import load_data


def main():
    """Main function"""
    # load data:
    d = load_data("test_day6.txt")
    d = load_data("day6.txt")
    d = list(map(int, d[0].split(",")))
    fish = [0] * 9
    for f in d:
        fish[f] += 1
    for _ in range(256):
        fish = fish[1:] + fish[0:1]
        fish[6] += fish[8]
        if _ == 79:
            print("Answer 1", sum(fish))
    print("Answer 2", sum(fish))


if __name__ == "__main__":
    main()
