import unittest

import numpy as np

import main


class TestMain(unittest.TestCase):
    def test_sum_values_scalar(self):
        self.assertEqual(5, main.sum_values(2, 3))

    def test_sum_values_vector(self):
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        ret = main.sum_values(a, b)
        self.assertEqual(5, ret[0])
        self.assertEqual(7, ret[1])
        self.assertEqual(9, ret[2])

    def test_is_positive_all(self):
        all_positive = np.array([1, 2, 3])
        all_negative = np.array([-1, -2, -3])
        self.assertTrue(main.is_positive(all_positive))
        self.assertFalse(main.is_positive(all_negative))

    def test_is_positive_any(self):
        one_positive = np.array([1, -2, -3])
        self.assertFalse(main.is_positive(one_positive))

    def test_absolute_scalar(self):
        self.assertEqual(1, main.absolute(1))
        self.assertEqual(1, main.absolute(-1))
        self.assertEqual(0, main.absolute(0))

    def test_absolute_vector(self):
        self.assertEqual(5, main.absolute(np.array([4, 3])))
        self.assertEqual(5, main.absolute(np.array([-4, -3])))
