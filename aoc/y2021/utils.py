"""
Utility Functions
"""

import os

import numpy as np

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "inputs")


def load_data(file_name, load_as="text"):
    if load_as == "text":
        return np.loadtxt(os.path.join(INPUT_DIR, file_name))
    else:
        raise ValueError(f'Unsupported type "{load_as}"')
