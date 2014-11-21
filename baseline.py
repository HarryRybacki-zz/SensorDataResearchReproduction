""" This file contains the baseline functions for detecting anomalies from
sensor data using the ellipsoid boundary modeling techniques outlined by
Dr. Suthaharan et al. They are accessible via the IPython notebook
at the root of the repository and can be interchanged with custom functions
for exploratory analysis of the algorithm(s)

These baseline functions can be replaced with other ellipsoid boundary
modeling techniques to work with the respective IPython notebook.
"""

import math
import numpy
import random


"""Begin data input functions"""
def read_ibrl_data(data_file):
    """Reads IBRL data from file and returns dict mapping
    temp./humidity sensor data to the node that collected them

    :param data_file: string representing path to ibrl dataset
    :return: dictionary mapping sensor node to list of tuples containing sensor data
    """
    with open(data_file, 'r') as fp:
        row_count = 0
        bad_count = 0
        input_readings = {}
        for line in fp:

            row_count = row_count + 1
            line = line.strip() # remove edge whitespace
            tokens = line.split(',') # segregate each section

            try:
                if len(tokens) == 5: #
                    temp_reading = tokens[0]
                    humidity_reading = tokens[1]
                    sensor_id = tokens[3]

                    # if sensor id is in the input_readings dict
                    if sensor_id in input_readings:
                        # add the temp and humidity values
                        input_readings[sensor_id]['temp_readings'].append(temp_reading)
                        input_readings[sensor_id]['humidity_readings'].append(humidity_reading)
                    else:
                        # add the sensor id and new temp and humidity values
                        input_readings[sensor_id] = {
                            'temp_readings': [tokens[0]],
                            'humidity_readings': [tokens[1]]
                        }
                else: # Note and dump bad data
                    bad_count = bad_count + 1

            except Exception as e:
                raise e

        # Convert data points to numpy arrays
        measurements = {sensor: numpy.array([readings['temp_readings'], readings['humidity_readings']], float)
                        for (sensor, readings) in input_readings.iteritems()}

        print "Total rows: %s" % row_count
        print "Total incomplete rows: %s" % bad_count

    return measurements

"""Begin data transformation functions"""
def randomize_readings(sensors):
    """ Pseudo randomly shuffles location of each pair of temperature and
    humidity observations

    :param sensors: Dictionary of sensors containing temp. and humidity readings
    :return: Dictionary of sensors containing shuffled temp. and humid. readings
    """
    for sensor in sensors:
        tuples = [(sensors[sensor][0][i],sensors[sensor][1][i])
                  for i in range(len(sensors[sensor][0]))]
        random.shuffle(tuples)
        sensors[sensor] = numpy.array([[reading[0] for reading in tuples], [reading[1] for reading in tuples]], float)

    return sensors

def generate_differences(sensors):
    """Generates a dictionary mapping sensors to a 2D array containing
    the successive differences of temp. and humidity measurements as well as
    a look up table mapping the resulting differences to their original
    measurements.

    :param sensor: Dictionary mapping sensors to original arrays of temp.
       and humidity readings
    :return: tuple containing dictionary mapping sensors to successive
       differences and look up table mapping the results to their original
       measurements
    """
    differences = {}
    lookup_table = {}

    for sensor in sensors:
        differences[sensor] = calc_succ_diff(sensors[sensor])

    return (differences, lookup_table)

def calc_succ_diff(sensor):
    """ Calculates the successive differences of for a given sensor

    :param sensor: Sensor to be operated on
    :return: numpy array of successive differences
    """
    sensor = [
        successive_diff(sensor[0]),
        successive_diff(sensor[1])
    ]

    return numpy.array(sensor, float)

def successive_diff(array):
    """ Calculates the successive differences for an array

    :param array: Array to be operated on
    :return: Array of resulting successive differences
    """

    return [array[i+1] - array[i] for i in range(len(array) - 1)]

"""Begin ellipsoid modeling functions"""
def generate_regional_ellipsoid_parameters(sensors_ellipsoid_parameters):
    """ Generates the aggregate ellipsoid parameters from a list of ellipsoids
     within a region

    :param ellipsoid_parameters: list of dictionaries representing ellipsoid
    parameters from individual sensors
    :return: dictionary representing the aggregate ellipsoid parameters for a
    given region
    """
    num_of_ellipsoids = len(sensors_ellipsoid_parameters)
    ave_a = sum([sensors_ellipsoid_parameters[ellipsoid]['a'] for ellipsoid in sensors_ellipsoid_parameters]) / num_of_ellipsoids
    ave_b = sum([sensors_ellipsoid_parameters[ellipsoid]['b'] for ellipsoid in sensors_ellipsoid_parameters]) / num_of_ellipsoids
    ave_theta = sum([sensors_ellipsoid_parameters[ellipsoid]['theta'] for ellipsoid in sensors_ellipsoid_parameters]) / num_of_ellipsoids

    return (ave_a, ave_b, ave_theta)

def generate_ellipsoid(sensor, a, b, theta=None):
    """ Calculates points representing an ellipsoid for a given a and b
    over from sensor readings.

    :param sensor: sensor mapped to a 2D array of temp. and humidity readings
    :param a: a parameter used in calculating ellipsoid parameters
    :param b: b parameter used in calculating ellipsoid parameters
    :param theta: optional hardcoded theta value
    :return: ellipsoid_parameters: dictionary containing parameters used in creation of
    as well as results from modeling ellipsoid boundaries
    """
    if theta is None:
        theta = calculate_ellipsoid_orientation(sensor)
    A = calc_A(a, b, theta) # A is independent of the temperatures

    ellipsoid_parameters = {
        'a': a,
        'b': b,
        'theta': theta,
        'original_sensor_readings': sensor,
        'ellipsoid_points': []
    }

    for temp_reading in sensor[0]:
        B = calc_B(a, b, temp_reading, theta)
        C = calc_C(a, b, temp_reading, theta)
        hi1 = calc_hi1(A, B, C)
        ellipsoid_parameters['ellipsoid_points'].append((temp_reading, hi1))
        hi2 = calc_hi2(A, B, C)
        ellipsoid_parameters['ellipsoid_points'].append((temp_reading, hi2))

    return ellipsoid_parameters

def calculate_ellipsoid_orientation(sensor):
    """ Calculates the orientation of raw sensor data points
    :param sensor: sensor mapped to a 2D array of temp. and humidity readings
    :return: float, theta of ellipsoid orientation
    """
    n = len(sensor[0])
    temperature_readings = sensor[0]
    humidity_readings = sensor[1]

    #FIXME(hrybacki): Come up with a better way of breaking this components down

    # part_one
    part_one_multiplicands = [temperature_readings[i]*humidity_readings[i] for i in range(n)]
    part_one_value = n * sum(part_one_multiplicands)

    # part two
    part_two_value = sum(temperature_readings) * sum(humidity_readings)

    # part three
    part_three_value = n * sum([math.pow(temp, 2) for temp in temperature_readings])

    # part four
    part_four_value = math.pow(sum(temperature_readings), 2)

    # arctan(theta)
    tan_theta = (part_one_value - part_two_value) / (part_three_value - part_four_value)

    #return math.atan(tan_theta)
    # @FIXME(hrybacki): Dr. Shan want's this to be absolute value. Do we need that? Why?
    #return math.fabs(math.atan(tan_theta))
    return math.atan(tan_theta)


def calc_A(a, b, theta):
    """ Returns the A value used in ellipsoid boundary modeling

    :param a: represents the major axis of the ellipsoid
    :param b: represents the mini axis os the ellipsoid
    :param theta: represents the orientation of the raw measurements
    :return: A value used in ellipsoid boundary modeling
    """
    A = (math.pow(math.sin(theta), 2) / math.pow(a, 2)) + (math.pow(math.cos(theta), 2) / math.pow(b, 2))

    return A

def calc_B(a, b, ti, theta):
    """ Returns the B value used in ellipsoid boundary modeling

    :param a: represents the major axis of the ellipsoid
    :param b: represents the mini axis os the ellipsoid
    :param ti: temperature (independent variable) used in calculation
    :param theta: represents the orientation of the raw measurements
    :return: B value used in ellipsoid boundary modeling
    """
    B = ((1/math.pow(a, 2)) - (1/math.pow(b, 2))) * ti * math.sin(2*theta)

    return B

def calc_C(a, b, ti, theta):
    """ Returns the C value used in ellipsoid boundary modeling

    :param a: represents the major axis of the ellipsoid
    :param b: represents the mini axis os the ellipsoid
    :param ti: temperature (independent variable) used in calculation
    :param theta: represents the orientation of the raw measurements
    :return: C value used in ellipsoid boundary modeling
    """
    C = ((math.pow(ti, 2) * math.pow(math.cos(theta), 2)) / math.pow(a, 2)) + \
        ((math.pow(ti, 2) * math.pow(math.sin(theta), 2)) / math.pow(b, 2)) - 1

    return C

def calc_hi1(A, B, C):
    """ Calculates the upper point for a given temp modeling an ellipsoid

    :param A: A value used in ellipsoid boundary modeling
    :param B: B value used in ellipsoid boundary modeling
    :param C: C value used in ellipsoid boundary modeling
    :return: Upper point for given temperature
    """
    try:
        return (-B + math.sqrt(math.pow(B, 2) - (4*A*C))) / (2*A)
    except ValueError:
        pass # skip domain errors

def calc_hi2(A, B, C):
    """ Calculates the lower point for a given temp modeling an ellipsoid

    :param A: A value used in ellipsoid boundary modeling
    :param B: B value used in ellipsoid boundary modeling
    :param C: C value used in ellipsoid boundary modeling
    :return: Lower point for given temperature
    """
    try:
        return (-B - math.sqrt(math.pow(B, 2) - (4*A*C))) / (2*A)
    except ValueError:
        pass # ignore domain errors

"""Begin incomplete functions"""
def inverse_transformation(lookup_table, aggregate_ellipsoid):
    """ Generates a tuple of two dicts mapping sensors to anomalies and true measurements

    :param lookup_table: dictionary mapping difference readings to their raw measurements
    :param aggregate_ellipsoid: 3-tuple containing aggregate ellipsoid parameters
    :return: tuple containing two dicts, one of true measurements and another of anomalies
    each mapped to their original sensors
    """
    pass

def is_anomaly(reading, aggregate_ellipsoid):
    """ Determines if reading is anomaly with respect to an ellipsoid

    :param reading: temperature and humidity readings
    :param aggregate_ellipsoid: parameters for aggregate ellipsoid
    :return: True if an anomaly, else False
    """
    pass
