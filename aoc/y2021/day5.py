""" Day 5 Solutions """

from aoc.y2021.utils import load_data


def main():
    """ Main function """
    # load data:
    d = load_data("day5.txt")
    print("INPUT DATA:")
    print(d)
    print("Day 5 Stub!")
    lines = []
    for line in d:
        a, b, c = line.split()
        x1, y1 = a.split(',')
        x2, y2 = c.split(',')
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        lines.append(((x1, y1), (x2, y2)))

    straight_lines = list(filter(lambda x: x[0][0]==x[1][0] or x[0][1]==x[1][1], lines))
    diagonal_lines = list(filter(lambda x: not x[0][0]==x[1][0] and not x[0][1]==x[1][1], lines))
    import numpy as np

    max_n = np.max(np.array(straight_lines))+1
    grid = np.zeros((max_n, max_n))
    for line in straight_lines:
        ((x1, y1), (x2, y2)) = line
        grid[min(x1,x2):max(x1,x2)+1, min(y1,y2):max(y1,y2)+1] += 1

    print("Answer 1", np.sum(grid>=2))

    for line in diagonal_lines:
        ((x1, y1), (x2, y2)) = line
        xdir = 1 if x1 < x2 else -1
        ydir = 1 if y1 < y2 else -1

        grid[x1, y1] += 1
        while True:
            x1 += xdir
            y1 += ydir
            grid[x1, y1] += 1
            if x1 == x2 or y1 == y2:
                break

    print("Answer 2", np.sum(grid>=2))



if __name__ == "__main__":
    main()
