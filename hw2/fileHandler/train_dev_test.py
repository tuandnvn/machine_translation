'''
Created on Mar 20, 2014

@author: Tuan
'''
import random as rd
import math

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
            - string input_lang_1: name of the first language (should be in ASCII)
            - string input_file_name_2: file name of the second language
            - string input_lang_2: name of the second language (should be in ASCII)
            - list partioned_file_names_and_percentages: something like:
                    [('train.dat',0.8), ('dev.dat', 0.1), ('test.dat', 0.1)]
        '''
        if type(partioned_file_names_and_percentages) != list:
            raise Exception('Partioned_file_names_and_percentages is a list of (filename, partition_percentage)')
        if sum([e[clr.PERCENTAGE_INDEX] for e in partioned_file_names_and_percentages]) != 1:
            raise Exception("You need to support a simplex: train_percentage + dev_percentage + test_percentage = 1")
        parallel_sentences = {input_lang_1:[], input_lang_2: []}
        with (open(input_file_name_1, 'r'),
              open(input_file_name_2, 'r')) as (file_handler_1,
                                            file_handler_2):
            """
            Only work with reasonable inputs, as I'm gonna load the input files into the memory
            """
            counter = 0 
            for (line_1, line_2) in zip(file_handler_1, file_handler_2):
                counter += 1
                parallel_sentences[input_lang_1].append(line_1)
                parallel_sentences[input_lang_2].append(line_2)
            t = range(counter)
            rd.shuffle(t)
            
            no_of_output_files = len(partioned_file_names_and_percentages)
            percentage_sum = 0
            def acc(value):
                percentage_sum += value
                return percentage_sum
            acc_percentages = [0] + [acc(e[clr.PERCENTAGE_INDEX]) for e in partioned_file_names_and_percentages]
            acc_percentage_ranges = [(acc_percentages[i],
                                      acc_percentages[i + 1]) for i in xrange(no_of_output_files)]
            for i in xrange(no_of_output_files):
                partioned_file = partioned_file_names_and_percentages[i][clr.FILE_NAME_INDEX]
                file_handler = open(partioned_file, 'w')
                [file_handler.write(sentence) for sentence in t[acc_percentage_ranges[0]:
                                                                acc_percentage_ranges[1]]]
