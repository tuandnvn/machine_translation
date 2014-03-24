'''
Created on Mar 20, 2014

@author: Tuan
'''
from collections import defaultdict

from hw2.database.connection import DatabaseConnector
from hw2.dictionary.dictionary import Dictionary
from hw2.training.model_handler import Model_Handler
from hw2.util import *
import numpy as np


class Trainer(Model_Handler):
    '''
    classdocs
    '''
    
    def __init__(self, target_lan_file_name,
                 target_lang,
                 source_lan_file_name,
                 source_lang):
        '''
        Arguments:
        target_lan_file_name -- string, file name of target language  
        target_lang -- string, target language string 
        source_lan_file_name -- string, file name of source language  
        source_lang -- string, source language string
        '''
        Model_Handler.__init__(self, target_lan_file_name, target_lang, 
                               source_lan_file_name, source_lang)
        self.list_of_parallel_sentences = []
        self.t_e_f = None
    
    def init_list_of_parallel_sentences(self):
        """
        Init parallel sentences for training data only
        """
        with (codecs.open(self.target_lan_file_name, 'r', CODEC),
              codecs.open(self.source_lan_file_name, 'r', CODEC)) as (target_file_handler,
                                            source_file_handler):
            """
            Only work with reasonable inputs, as I'm gonna load the input files into the memory
            """
            for (target_line, source_line) in zip(target_file_handler, source_file_handler):
                self.list_of_parallel_sentences.append((target_line, source_line))
                
    def buildDictionary(self):
        self.list_of_parallel_bag_of_indexes = []
        for (target_line, source_line) in self.list_of_parallel_sentences:
            target_tokens, source_tokens = (target_line.split(' '), source_line.split(' '))
            self.dictionary[self.target_lang].feedTokens(target_tokens)
            self.dictionary[self.source_lang].feedTokens(source_tokens)
            (target_token_indices, source_token_indices) = (self.getIndexes(target_tokens, self.target_lang),
                                                  self.getIndexes(source_tokens, self.lang_))
                                                
            self.list_of_parallel_bag_of_indexes.append((target_token_indices, source_token_indices))
        self.target_lexicon_size = self.dictionary[self.target_lang].getDictSize()
        self.source_lexicon_size = self.dictionary[self.source_lang].getDictSize()
    
    def buildDictionarySaveToFile(self, target_lang_dictionary_file_name, source_lang_dictionary_file_name):
        '''
        dictionary_file_name_1 is corresponding to target language (english), 
        dictionary_file_name_2 is corresponding to source language (spanish)
        '''
        self.buildDictionary()
        self.saveDictionary(target_lang_dictionary_file_name, source_lang_dictionary_file_name)
        
    def save_to_model_file(self, model_file_name):
        self.model_database_connect(model_file_name)
        
        input_data = []
        for i in xrange(self.target_lexicon_size):
            for j in xrange(self.source_lexicon_size):
                input_data.append((j, i, float(self.t_e_f[i,j])))
        self.database.insertMany(input_data)
        
    def _default_check(self):
        '''
        Check the condition of convergence
        '''
        if 't_e_f' not in self.__dict__:
            raise Exception('Translation model has not been built yet. Only use with training.')
    
    def training(self, no_of_iterations, convergence_check = _default_check):
        '''
        '''
        """
        t(e|f) is t_e_f
        we assume that target (e) is english, f is foreign (spanish)
        """
        self.t_e_f = np.zeros((self.target_lexicon_size,self.source_lexicon_size))
        
        """
        Uniformly initiated
        """
        self.t_e_f.fill(1/(self.target_lexicon_size*self.source_lexicon_size))
        
        """
        count(e|f) is c_e_f
        """
        self.c_e_f = np.zeros((self.target_lexicon_size,self.source_lexicon_size))
        self.total_f = np.zeros(self.source_lexicon_size)
        
        for i in xrange(len(no_of_iterations)):
            for (target_token_indices, source_token_indices) in self.list_of_parallel_bag_of_indexes:
                s_total = defaultdict(float)
                for target_token_index in target_token_indices:
                    for source_token_index in source_token_indices:
                        s_total[target_token_index] += self.t_e_f[target_token_index, source_token_index]
                for target_token_index in target_token_indices:
                    for source_token_index in source_token_indices:
                        self.c_e_f[target_token_index, source_token_index] +=\
                                 self.t_e_f[target_token_index, source_token_index]/s_total[target_token_index]
                        self.total_f[source_token_index] +=\
                                 self.t_e_f[target_token_index, source_token_index]/s_total[target_token_index]
                        
            self.t_e_f = self.c_e_f/self.total_f
