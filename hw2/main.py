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
from hw2.training import *
from util import *


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='IBM Model 1 Machine Translator')
    parser.add_argument('-m', '--%s' % MODE_OPTION, default=EVALUATION_MODE, nargs=1,
                        choices=[EVALUATION_MODE, TRAIN_MODE, SAMPLING_MODE, DIVIDING_MODE],
                        help='Specify either runEMTrainingLoop or evaluating mode.')
    parser.add_argument('-s', '--%s' % SOURCE_OPTION, default=None, nargs=2, required=True,
                        help='Specify the source language (the foreign language in IBM model) and source file.')
    parser.add_argument('-t', '--%s' % TARGET_OPTION, default=None, nargs=2, required=True,
                        help='Specify the target language (the English language in IBM model) and target file.')
    parser.add_argument('-i', '--%s' % ITERATION_OPTION, default=None, nargs=1, type=int,
                        help='Specify the maximum iteration.')
    
    parser.add_argument('-x', '--%s' % SAMPLING_OPTION, default=None, nargs=1, type=int,
                        help='Specify the number of sentences should be sampled.')
    parser.add_argument('-p', '--%s' % TDT_PROP_OPTION, default=None, nargs=3, type=float,
                        help='Specify the proportion of sentences should be divided into \
                                train - dev - test')
    
    parser.add_argument('-D', '--%s' % DICTIONARY_OPTION, default=None, nargs=2, 
                        help='Specify the dictionary files to be saved for training, or loaded \
                             for testing. The file name should be in the order source dictionary file name \
                             then target dictionary file name')
    
    """
    If the mode is runEMTrainingLoop, model file is to stored the trained model
    If the mode is evaluating, 
    """
    parser.add_argument('-d', '--%s' % MODEL_OPTION, default=None, nargs=1,
                      help='Specify model file name.')
    begin_time = time.time()
    
    
    args = vars(parser.parse_args())
    print args
    mode = args[MODE_OPTION][0]
    
    source_lan = args[SOURCE_OPTION][LANG_INDEX]
    source_file = args[SOURCE_OPTION][FILE_INDEX]
    target_lan = args[TARGET_OPTION][LANG_INDEX]
    target_file = args[TARGET_OPTION][FILE_INDEX]

    if mode == TRAIN_MODE:
        """
        Training the IBM 1 model and insert into the database
        """
        no_of_iterations = None
        if args[ITERATION_OPTION] != None:
            no_of_iterations = args[ITERATION_OPTION][0]
        if args[MODEL_OPTION] != None:
            model_file_name = args[MODEL_OPTION][0]
        else:
            raise Exception('Model file is not specified.')
        
        if args[DICTIONARY_OPTION] != None:
            source_dictionary_file, target_dictionary_file = args[DICTIONARY_OPTION]
        else:
            raise Exception('Dictionary files are not specified.')
        trainer_handler = Trainer(target_file, target_lan, target_dictionary_file,
                                  source_file, source_lan, source_dictionary_file,
                                  no_of_iterations, model_file_name)
        trainer_handler.train()
        
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
            no_of_sentences = args[SAMPLING_OPTION][0]
        else:
            raise Exception('The number of samples is not specified.')
        Sampler.sample(source_file,
                       source_file + '.' + str(no_of_sentences) + SAMPLING_EXT,
                       no_of_sentences)
        Sampler.sample(target_file, 
                       target_file + '.' + str(no_of_sentences) + SAMPLING_EXT,
                       no_of_sentences)
    elif mode == DIVIDING_MODE:
        if args[TDT_PROP_OPTION] != None:
            prob = args[TDT_PROP_OPTION]
        else:
            raise Exception('The number of samples is not specified.')
        TrainDevTest.partition(target_file, 'en', source_file, 'es',
                               [(target_file + TRAIN_EXT, source_file + TRAIN_EXT , prob[0]),
                                (target_file + DEV_EXT, source_file + DEV_EXT, prob[1]),
                                (target_file + TEST_EXT, source_file + TEST_EXT, prob[2])])
    print str(time.time() - begin_time)
