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


    def test_calculate_mean(self):

        assert helpers.calculate_mean([1, 2, 3]) == 2.0

    def test_calculate_std_dev(self):

        expected_sd = (1.8708286933869707, 0.82915619758884995)
        assert helpers.calculate_std_dev(self.original_dict['1']) == expected_sd

    # TODO(hrybacki): unfinished
    def test_calculate_dist(self):

        # FIXME: Random seed 11 produces a positive distance
        fixed_seed = 11
        random.seed(fixed_seed)

        shuffled_measurements = helpers.randomize_readings(self.original_dict)

        differences, lookup_table = helpers.generate_differences(shuffled_measurements)

        sigma_temp, sigma_humidity = helpers.calculate_std_dev(differences['1'])

        p1 = differences['1'][0]
        p2 = differences['1'][1]

        dist = helpers.calculate_dist(p1, p2, sigma_temp, sigma_humidity)

        '''
        print differences
        print sigma_temp
        print sigma_humidity
        print p1
        print p2
        print dist
        '''
        assert True

    # TODO(hrybacki): unfinished
    def test_calculate_ellipsoid_orientation(self):

        fixed_seed = 11
        random.seed(fixed_seed)

        shuffled_measurements = helpers.randomize_readings(self.original_dict)
        differences, lookup_table = helpers.generate_differences(shuffled_measurements)

        helpers.calculate_ellipsoid_orientation(differences['1'])

        assert True


    def test_get_min_max_temp(self):

        assert helpers.get_min_max_temp(self.original_dict['1']) == (1, 6)


    # TODO(hrybacki)
    def test_genererate_lookup_table(self):
        pass

    # TODO(hrybacki)
    def test_model_ellipsoid_of_single_sensor(self):
        pass

    # TODO(hrybacki)
    def test_model_region_aggregate(self):
        pass

    # TODO(hrybacki)
    def test_model_inverse_transformation(self):
        pass

    # TODO(hrybacki)
    def test_model_is_anomaly_true(self):
        pass

    # TODO(hrybacki)
    def test_model_is_anomaly_false(self):
        pass