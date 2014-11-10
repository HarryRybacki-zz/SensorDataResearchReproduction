"""Test cases for helper code."""

import copy
import random
import unittest

import helpers


class testHelpers(unittest.TestCase):

    def setUp(self):

        # Original test daa dict "Sensor: [(temp, humid), ...]"
        self.original_dict = {
            '1': [(1, 5), (3, 5), (2, 4), (6, 3)],
            '2': [(3, 3), (8, 1), (3, 8), (1, 6)],
            '3': [(1, 3), (9, 5), (6, 9), (4, 7)],
            '4': [(8, 4), (3, 4), (3, 9), (4, 9)]
        }

        # Permuted version of original measurements
        fixed_seed = 1 # Fix seed so we have deterministic 'shuffled' readings
        random.seed(fixed_seed)
        self.shuffled_dict = copy.deepcopy(self.original_dict) # shuffle is an in place function
        helpers.randomize_readings(self.shuffled_dict)

        # Successive differences and lookup table
        self.differences_dict, self.lookup_table = \
            helpers.generate_differences(self.shuffled_dict)

        # Standardized version of successive differences
        self.standardized_differences = helpers.standardize_readings(
            self.differences_dict)

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

    #def test_calculate_humidity_mean(self):

    #    expected_mean = 3


    #    assert helpers.calculate_humidity_mean(self.original_dict['1']) == expected_mean

    def test_standardize_readings(self):
        print "######"
        import pprint

        print "Differences"
        pprint.pprint(self.original_dict)
        print"\nStandardized"
        pprint.pprint(helpers.standardize_readings(self.original_dict))

        assert True


    def test_calculate_temp_mean(self):

        expected_mean = (12 / 4)

        assert helpers.calculate_temp_mean(self.original_dict['1']) == expected_mean

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

        expected_theta = 0.343023940421

        self.assertAlmostEqual(expected_theta,
                               helpers.calculate_ellipsoid_orientation(self.original_dict['1']),
                               7)

    def test_calc_A(self):

        a = 1.7601
        b = 4.1168
        theta = 0.717564
        expected_A = 0.17306

        self.assertAlmostEqual(expected_A,
                               helpers.calc_A(a, b, theta),
                               5)

    def test_calc_B(self):

        a = 1.7601
        b = 4.1168
        temp = 3.0
        theta = 0.717564
        expected_B = 0.784098

        self.assertAlmostEqual(expected_B,
                               helpers.calc_B(a, b, temp, theta),
                               5)

    def test_calc_C(self):

        a = 1.7601
        b = 4.1168
        temp = 3.0
        theta = 0.717564
        expected_C = 0.878646

        self.assertAlmostEqual(expected_C,
                               helpers.calc_C(a, b, temp, theta),
                               5)

    def test_calc_hi1(self):
        A = 0.17306
        B = 0.784098
        C = 0.878646
        expected_hi1 = -2.03111

        self.assertAlmostEqual(expected_hi1,
                               helpers.calc_hi1(A, B, C),
                               5)

    def test_calc_h21(self):
        A = 0.17306
        B = 0.784098
        C = 0.878646
        expected_hi2 = -2.49968

        self.assertAlmostEqual(expected_hi2,
                               helpers.calc_hi2(A, B, C),
                               5)

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