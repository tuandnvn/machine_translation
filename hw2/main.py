'''
Created on March 23, 2014

@author: Tuan
'''
"""
Get rid of UTF-8 BOM
"""

import argparse
import time

from hw2.fileHandler.sampler import Sampler
from hw2.fileHandler.train_dev_test import TrainDevTest
from training import *
from util import *


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='IBM Model 1 Machine Translator')
    parser.add_argument('-m', '--%s' % MODE_OPTION, default=EVALUATION_MODE, nargs=1,
                        choices=[EVALUATION_MODE, TRAIN_MODE, SAMPLING_MODE, DIVIDING_MODE],
                        help='Specify either training or evaluating mode.')
    parser.add_argument('-s', '--%s' % SOURCE_OPTION, default=None, nargs=2, required=True,
                        help='Specify the source language (the foreign language in IBM model) and source file.')
    parser.add_argument('-t', '--%s' % TARGET_OPTION, default=None, nargs=2, required=True,
                        help='Specify the target language (the English language in IBM model) and target file.')
    parser.add_argument('-i', '--%s' % ITERATION_OPTION, default=None, nargs=1,
                        help='Specify the maximum iteration.')
    
    SAMPLING_OPTION = 'sampling-number'
    TDT_PROP_OPTION = 'train-dev-test-prob'

    parser.add_argument('-x', '--%s' % SAMPLING_OPTION, default=None, nargs=1,
                        help='Specify the number of sentences should be sampled.')
    parser.add_argument('-d', '--%s' % TDT_PROP_OPTION, default=None, nargs=3,
                        help='Specify the proportion of sentences should be divided into \
                                train - dev - test')
    """
    If the mode is training, model file is to stored the trained model
    If the mode is evaluating, 
    """
    parser.add_argument('-d', '--%s' % MODEL_OPTION, default=None, nargs=1,
                      help='Specify model file name.')
    begin_time = time.time()
    
    args = vars(parser.parse_args())
    mode = args[MODE_OPTION][0]
    source_lan = args[SOURCE_OPTION][0]
    source_file = args[SOURCE_OPTION][1]
    target_lan = args[TARGET_OPTION][0]
    target_file = args[TARGET_OPTION][1]

    if mode == TRAIN_MODE:
        """
        Training the IBM 1 model and insert into the database
        """
        no_of_iterations = None
        if args[ITERATION_OPTION] != None:
            no_of_iterations = args[ITERATION_OPTION][0]
        if args[MODEL_OPTION] != None:
            model_file = args[MODEL_OPTION][0]
        else:
            raise Exception('Model file is not specified.')
        
        trainer_handler = Trainer(target_file, target_lan, source_file, source_lan)
        trainer_handler.training(no_of_iterations)
    elif mode == EVALUATION_MODE:
        """
        Testing the trained IBM 1 model using the data
        """
        if args[MODEL_OPTION] != None:
            model_file = args[MODEL_OPTION][0]
        else:
            raise Exception('Model file is not specified.')
        evaluator_handler = Evaluator(target_file, target_lan, source_file, source_lan)
        evaluator_handler.evaluate()
    elif mode == SAMPLING_MODE:
        if args[SAMPLING_OPTION] != None:
            model_file = args[SAMPLING_OPTION][0]
        else:
            raise Exception('The number of samples is not specified.')
        sampling_handler = Sampler(target_file, source_file, 
                                   target_file + SAMPLING_EXT,
                                   source_file + SAMPLING_EXT,
                                   )
    elif mode == DIVIDING_MODE:
        if args[SAMPLING_OPTION] != None:
            model_file = args[SAMPLING_OPTION][0]
        else:
            raise Exception('The number of samples is not specified.')
        TrainDevTest.partition(target_file, 'en', source_file, 'es',
                               [( target_file+TRAIN_EXT, source_file + TRAIN_EXT ,0.8), 
                                (target_file+DEV_EXT, source_file + DEV_EXT, 0.1), 
                                (target_file+TEST_EXT, source_file + TEST_EXT, 0.1)])
    print str(time.time() - begin_time)
