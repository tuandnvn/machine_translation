'''
Created on Mar 20, 2014

@author: Tuan
'''
import math

import random as rd
from hw2.util import *


class TrainDevTest(object):
    '''
    classdocs
    '''
    FILE_NAME_INDEX = 0
    PERCENTAGE_INDEX = 1
    @classmethod
    def partition(clr, input_file_name_1,
                 input_lang_1,
                 input_file_name_2,
                 input_lang_2,
                 partioned_file_names_and_percentages):
        '''
        Parameters: 
            - string input_file_name_1: file name of the first language 
            - string input_lang_1: name of the first language
            - string input_file_name_2: file name of the second language
            - string input_lang_2: name of the second language
            - list partioned_file_names_and_percentages: something like:
                    [(['target.train','source.train'],0.8), 
                    (['target.dev','source.dev'],0.1), 
                    (['target.test','source.test'],0.8)]
        '''
        input_file_names = []
        input_langs = []
        input_file_names.append(input_file_name_1)
        input_file_names.append(input_file_name_2)
        input_langs.append(input_lang_1)
        input_langs.append(input_lang_2)
        
        if type(partioned_file_names_and_percentages) != list:
            raise Exception('Partioned_file_names_and_percentages is a list of (filename, partition_percentage)')
        if sum([e[clr.PERCENTAGE_INDEX] for e in partioned_file_names_and_percentages]) != 1:
            raise Exception("You need to support a simplex: train_percentage + dev_percentage + test_percentage = 1")
        parallel_sentences = {input_lang_1:[], input_lang_2: []}
        with tuple([codecs.open(input_file_name, 'r', CODEC)] 
                   for input_file_name in input_file_names) as file_handler:
            """
            Only work with reasonable inputs, as I'm gonna load the input files into the memory
            """
            counter = [0,0] 
            for i in xrange(2):
                for line in file_handler[i]:
                    counter[i] += 1
                    parallel_sentences[input_langs[i]].append(line)
            
            if counter[0] != counter[1]:
                raise Exception('Number of aligned sentences are not the same')
            t = range(counter[0])
            rd.shuffle(t)
            
            no_of_output_files = len(partioned_file_names_and_percentages)
            percentage_sum = 0
            def acc(value):
                percentage_sum += value
                return percentage_sum
            acc_percentages = [0] + [acc(e[clr.PERCENTAGE_INDEX]) for e in partioned_file_names_and_percentages]
            acc_percentage_ranges = [(acc_percentages[i],
                                      acc_percentages[i + 1]) for i in xrange(no_of_output_files)]
            
            for output_file_counter in xrange(no_of_output_files):
                for i in xrange(2):
                    partioned_file = partioned_file_names_and_percentages[output_file_counter][clr.FILE_NAME_INDEX][i]
                    file_handler = codecs.open(partioned_file, 'w', CODEC)
                    [file_handler.write(sentence) for 
                        sentence in parallel_sentences[input_langs[i]][acc_percentage_ranges[0]:
                                                                        acc_percentage_ranges[1]]]
