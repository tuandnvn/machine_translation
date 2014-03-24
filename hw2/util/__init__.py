import codecs

"""
Options for command line
"""
SOURCE_OPTION = 'source'
TARGET_OPTION = 'target'
MODE_OPTION = 'mode'
ITERATION_OPTION = 'max-iter'
MODEL_OPTION = 'model-file'

SAMPLING_OPTION = 'sampling-number'
TDT_PROP_OPTION = 'train-dev-test-prob'


EVALUATION_MODE = 'evaluate'
TRAIN_MODE = 'train'
SAMPLING_MODE = 'sample'
DIVIDING_MODE ='train-dev-test'

"""
Sqlite constants
"""
SOURCE_KEY = 'source_index'
TARGET_KEY = 'target_index'
PROBABILITY_KEY = 'prob'

"""
File specifications
"""
CODEC = 'utf-8'
SAMPLING_EXT = '.sampling'
TRAIN_EXT = '.train'
DEV_EXT = '.dev'
TEST_EXT = '.test'