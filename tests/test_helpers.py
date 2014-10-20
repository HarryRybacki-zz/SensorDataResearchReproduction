"""Test cases for helper code."""

import random
import unittest

import helpers


class testHelpers(unittest.TestCase):

    def setUp(self):

        self.original_dict = original_dict = {
            '1': [(1, 5), (3, 5), (2, 4), (6, 3)],
            '2': [(3, 3), (8, 1), (3, 8), (1, 6)],
            '3': [(1, 3), (9, 5), (6, 9), (4, 7)],
            '4': [(8, 4), (3, 4), (3, 9), (4, 9)]
        }

    def test_randomize_readings(self):

        fixed_seed = 1
        random.seed(fixed_seed)

        expected_output = {
            '1': [(6, 3), (3, 5), (2, 4), (1, 5)],
            '2': [(8, 1), (3, 3), (1, 6), (3, 8)],
            '3': [(6, 9), (1, 3), (4, 7), (9, 5)],
            '4': [(3, 4), (4, 9), (3, 9), (8, 4)]
        }

        assert helpers.randomize_readings(self.original_dict) == expected_output

    def test_generate_differences(self):

        expected_differences = {
            '1': [(2, 0), (-1, -1), (4, -1)],
            '2': [(5, -2), (-5, 7), (-2, -2)],
            '3': [(8, 2), (-3, 4), (-2, -2)],
            '4': [(-5, 0), (0, 5), (1, 0)]
        }
        differences, lookup_table = helpers.generate_differences(self.original_dict)
        assert differences == expected_differences

    def test_calculate_humidity_mean(self):

        expected_mean = 3

        assert helpers.calculate_humidity_mean(self.original_dict['1']) == expected_mean

    def test_calculate_temp_mean(self):

        expected_mean = (19 / 4)

        assert helpers.calculate_temp_mean(self.original_dict['1']) == expected_mean