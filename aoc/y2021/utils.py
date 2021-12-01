"""
Utility Functions
"""

import os

import numpy as np

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "inputs")


def load_data(file_name, load_as="text"):
    """ Load data """
    full_path = os.path.join(INPUT_DIR, file_name)
    if load_as == "text":
        with open(full_path) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
        return lines
    elif load_as == "int":
        return np.loadtxt(full_path, dtype=np.int32)
    elif load_as == "float":
        return np.loadtxt(full_path, dtype=np.float)
    else:
        raise ValueError(f'Unsupported type "{load_as}"')
