'''
Created on Mar 20, 2014

@author: Tuan
'''
import numpy as np
from hw2.dictionary.dictionary import Dictionary

class Trainer(object):
    '''
    classdocs
    '''
    
    def __init__(self, input_file_name_1,
                 input_lang_1,
                 input_file_name_2,
                 input_lang_2):
        '''
        Constructor
        '''
        self.input_file_name_1 = input_file_name_1
        self.lang_1 = input_lang_1
        self.input_file_name_2 = input_file_name_2
        self.lang_2 = input_lang_2     
        self.list_of_parallel_sentences = []
        
    def init_list_of_parallel_sentences(self):
        with (open(self.input_file_name_1, 'r'),
              open(self.input_file_name_2, 'r')) as (file_handler_1,
                                            file_handler_2):
            """
            Only work with reasonable inputs, as I'm gonna load the input files into the memory
            """
            counter = 0 
            for (line_1, line_2) in zip(file_handler_1, file_handler_2):
                self.list_of_parallel_sentences.append((line_1, line_2))
    
    def build_dictionary(self):
        self.dictionary = {self.lang_1:Dictionary(), self.lang_2:Dictionary()}
        self.tokenized_
        for (line_1, line_2) in self.list_of_parallel_sentences:
            tokens_1, tokens_2 = (line_1.split(' '), line_2.split(' '))
            self.dictionary[self.lang_1].feedWords(tokens_1)
            self.dictionary[self.lang_2].feedWords(tokens_2)
        self.lexicon_size_1 = self.dictionary[self.lang_1].getDictSize()
        self.lexicon_size_2 = self.dictionary[self.lang_2].getDictSize()
        
    def training(self):
        '''
        '''
        """
        t(e|f) is t_e_f
        we assume that language_1 is english, language_2 is foreign
        """
        if 'dictionary' not in self.__dict__:
            raise Exception('Dictionary has been built yet. Use build_dictionary() to build.')
        t_e_f = np.zeros((self.lexicon_size_1,self.lexicon_size_2))
        
        """
        Uniformly initiated
        """
        t_e_f.fill(1/(self.lexicon_size_1*self.lexicon_size_2))
        
        """
        count(e|f) is c_e_f
        """
        c_e_f = np.zeros((self.lexicon_size_1,self.lexicon_size_2))
        total_f = np.zeros(self.lexicon_size_2)
        