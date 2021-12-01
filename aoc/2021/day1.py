# Day 1

import numpy as np

#load data:
d = np.loadtxt('inputs/day1.txt')

# answer 1:
answer_1 = np.sum(np.diff(d) > 0)

# answer 2:
win_d = np.convolve(d, np.ones(3))[2:-2]
answer_2 = np.sum(np.diff(win_d)>0)

print("Answer 1: ", answer_1)
print("Answer 2: ", answer_2)
