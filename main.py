"""This module consists of a method to 
    - sum up two values
    - check if a value is positive
    - calculate absolute of a value
"""
import numpy as np


def sum_values(a, b):
    return a + b


def is_positive(a):
    """
    a is a scalar -> return if sign is positive.
    a is a vector -> return if sings of *all elements* are positive.
    """
    # return a > 0 if not isinstance(a, np.ndarray) else (a > 0).all()
    return a > 0 if not isinstance(a, np.ndarray) else (a > 0).any()
    # this causes a failure in test only when a is a vector containing at least one negative element
    # and all remaining elements are positive.


def absolute(a):
    if not isinstance(a, np.ndarray):
        return abs(a)
    else:
        return np.linalg.norm(a)
