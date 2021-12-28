""" Day 4 Solutions """

import os

import numpy as np

from aoc.y2021.utils import load_data

if os.environ.get("AOC_QUIET", None):

    # pylint: disable
    def print(*args, **kwargs):
        pass


def main():
    """Main function"""
    # load data:
    # d = load_data("test_day4.txt")
    d = load_data("day4.txt")
    print("INPUT DATA:")
    print(d)
    print("Day 4 Stub!")
    draws = list(map(int, d[0].split(",")))
    boards = []
    n_boards = (len(d) - 1) // 6
    for b in range(n_boards):
        d_board = d[2 + b * 6 : 7 + b * 6]
        d_board = [list(map(int, row.split())) for row in d_board]
        boards.append(d_board)
    boards = np.array(boards)
    marks = np.zeros_like(boards)
    for draw in draws:
        idx = np.where(boards == draw)
        marks[idx] = 1
        boards[idx] = 0
        # dims boards x rows x cols
        rows = np.sum(marks, axis=1)
        cols = np.sum(marks, axis=2)
        if np.any(rows == 5):
            board_win = np.argwhere(rows == 5)
            break
        if np.any(cols == 5):
            board_win = np.argwhere(cols == 5)
            break
    win = board_win[0][0]
    board = boards[win]
    mark = marks[win]
    # board[mark]=0
    # print(board_win, board, mark)
    print(np.sum(board), draw, np.sum(board) * draw)

    d = load_data("day4.txt")
    print("INPUT DATA:")
    print(d)
    print("Day 4 Stub!")
    draws = list(map(int, d[0].split(",")))
    boards = []
    n_boards = (len(d) - 1) // 6
    for b in range(n_boards):
        d_board = d[2 + b * 6 : 7 + b * 6]
        d_board = [list(map(int, row.split())) for row in d_board]
        boards.append(d_board)
    boards = np.array(boards)
    marks = np.zeros_like(boards)
    n_wins = 0
    for draw in draws:
        idx = np.where(boards == draw)
        marks[idx] = 1
        boards[idx] = 0
        # dims boards x rows x cols
        checking = True
        winner = False
        while checking:
            rows = np.sum(marks, axis=1)
            cols = np.sum(marks, axis=2)
            if np.any(rows == 5):
                board_win = np.argwhere(rows == 5)
                print("winner", draw, board_win)
                n_wins += 1
                winner = True
            elif np.any(cols == 5):
                print("winner", draw, board_win)
                board_win = np.argwhere(cols == 5)
                n_wins += 1
                winner = True
            else:
                checking = False
                winner = False
            if n_wins < n_boards and winner:
                win = board_win[0][0]
                board = boards[win]
                print("winning board", board)
                boards[win] = 0
                marks[win] = 0
            elif winner:
                win = board_win[0][0]
                board = boards[win]
                print("DONE")
                print(np.sum(board), draw, np.sum(board) * draw)
                import sys

                sys.exit()
    # board[mark]=0
    # print(board_win, board, mark)


if __name__ == "__main__":
    main()
