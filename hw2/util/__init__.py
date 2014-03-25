import codecs

"""
Options for command line
"""
SOURCE_OPTION = 'source'
TARGET_OPTION = 'target'
MODE_OPTION = 'mode'
ITERATION_OPTION = 'max_iter'
MODEL_OPTION = 'model_file'
NULL_OPTION = 'null'
VERBATIM_OPTION = 'verbatim'
SAMPLING_OPTION = 'sampling_number'
TDT_PROP_OPTION = 'train_dev_test_prob'
DICTIONARY_OPTION = 'dictionary'
CONVERGENCE_OPTION = 'convergence'

EVALUATION_MODE = 'evaluate'
TRAIN_MODE = 'train'
SAMPLING_MODE = 'sample'
# DIVIDING_MODE ='train-dev-test'

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
FILE_INDEX = 0
LANG_INDEX = 1
ENDING_STRS = ['.', '?', ')']
BEGINNING_STRS = ['(']

"""
Training and testing options
"""
TARGET_LANGUAGE_OPTION = 'target'
SOURCE_LANGUAGE_OPTION = 'source'
