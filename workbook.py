import helpers

"""
Begin phase one - Read Input

Note: This phase will need slight tweaking for each data source as they do not follow a truly standard data format.
As a result, interfaces will likely need to be written for each source akin to read_ibrl_data()

Note: While I had originally intended to use Pandas DataFrame objects to store / manipulate the data I opted out as
it expects each column (sensor) to be of the same length (number of measurements) but that isn't the case with the IBRL
dataset. I could cast each column to a Pandas Series (1 dimensional vector object) and add each Series to the DataFrame
but that might be overkill. For know I am using a simple dictionary mapping each sensor to a list of tuples containing
temperature and humidity data.
"""
# location of IBRL sensor measurements dataset
ibrl_sensor_measurements_file = "/Users/hrybacki/git/csc490/data2.txt"

# Create dictionary of original sensors mapping to their measurements
measurements = helpers.read_ibrl_data(ibrl_sensor_measurements_file)

"""
Begin phase two - Process Data
"""

# 1A - Transformation

# Shuffle measurements
shuffled_measurements = helpers.randomize_readings(measurements)

# Calculate successive differences
differences = helpers.generate_differences(shuffled_measurements)


# 1B - Ellipsoid Boundary Modeling
print len(differences['11'])
print len(shuffled_measurements['11'])

# 1C - Inverse Transformation

"""
Begin phase four - Visually model data
"""

print "Completed..."