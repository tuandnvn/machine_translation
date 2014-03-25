'''
Created on Mar 20, 2014

@author: Tuan
'''
from hw2.util import *


class Sampler(object):
    '''
    A Sampler class read two parallel corpus and generate a set of n parallel sentences
    '''
    
    @classmethod
    def sample(clr, input_file_name,
                 output_file_name,
                 no_of_parralel_sentences):
        '''
        Class method sample to sample a number of sentences from a file
        '''
        with codecs.open(input_file_name, 'r', CODEC) as input_file_handler:
            with codecs.open(output_file_name, 'w', CODEC) as output_file_handler:
                counter = 0
                for line in input_file_handler:
                    if counter > no_of_parralel_sentences:
                            return
                    counter += 1
                    output_file_handler.write(line)
        
