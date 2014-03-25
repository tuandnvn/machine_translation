'''
Created on Mar 23, 2014

@author: Tuan
'''
from hw2.training.model_handler import Model_Handler
from hw2.util import *
import numpy as np


class Evaluator(Model_Handler):
    '''
    Class to handle evaluate the learned parameters using the input files. 
    The input files take in two files: one of target language (English) and 
    one of source language. The former should have multiple candidate translations
    for each source sentence in the later.
    Therefore, use the following format:
    - Target file
        1<tab>First candidate for source sentence 1.
        1<tab>Second candidate for source sentence 1.
        2<tab>First candidate for source sentence 2.
    - Source file
        1<tab>Source sentence 1.
        2<tab>Source sentence 2.
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
        self.dict_of_parallel_sentences = {}
    
    def init_dict_of_parallel_sentences(self):
        """
        Init parallel sentences for testing data
        self.dict_of_parallel_sentences will be initiated.
        
        The key is the first matching index in each sentence
        The value is a tuple of (list_of_target_sentences, source_sentence)  
        """
        with codecs.open(self.target_lan_file_name, 'r', CODEC) as target_file_handler:
            for  target_line in target_file_handler:
                """
                Source file need to be treated differently from target file
                """
                target_line = self.cleanLine(target_line)
                tab_index = target_line.find('\t')
                matching_index = target_line[:tab_index]
                self.dict_of_parallel_sentences[matching_index][0].append(target_line[tab_index + 1:])
        
        with codecs.open(self.source_lan_file_name, 'r', CODEC) as source_file_handler:
            for source_line in source_file_handler:
                """
                Source file need to be treated differently from target file
                """
                source_line = self.cleanLine(source_line)
                tab_index = source_line.find('\t')
                matching_index = source_line[:tab_index]
                self.dict_of_parallel_sentences[matching_index] = ([], source_line[tab_index + 1:])
            
    
    def load_from_model_file(self, model_file_name):
        '''
        Connect to the sqlite model file, and load the translation model from there.
        Arguments:
        model_file_name -- string, file name of model
        '''
        self.model_database_connect(model_file_name)
        self.target_lexicon_size = int(self.database.countNumberOfTargetIndices())
        self.source_lexicon_size = int(self.database.countNumberOfSourceIndices())
        model_values = self.database.selectAll()
        
        self.t_e_f = np.zeros((self.target_lexicon_size, self.source_lexicon_size))
        
        for value in model_values:
            self.t_e_f [value[TARGET_KEY], value[SOURCE_KEY]] = value[PROBABILITY_KEY]
            
    
    def evaluate(self):
        '''
        Evaluate the evaluation files
        '''
        evaluate_result = {}
        for matching_index in self.dict_of_parallel_sentences:
            """
            An auxillary function to tokenize the line and get the line length and line token indices
            """
            
            list_of_targets, source = self.dict_of_parallel_sentences[matching_index]
            source_length, source_token_indices = self.lineTokenizer(source, self.source_lang)
            
            best_translation = -1
            largest_translation_prob_log = None
            for i in xrange(len(list_of_targets)):
                target_length, target_token_indices = self.lineTokenizer(list_of_targets[i], self.target_lang)
                translation_prob_log = self.calculateTranslationProbability(target_length,
                                                                            target_token_indices,
                                                                            source_length,
                                                                            source_token_indices)
                if largest_translation_prob_log == None:
                    translation_prob_log = largest_translation_prob_log
                    best_translation = i
                if translation_prob_log > largest_translation_prob_log:
                    largest_translation_prob_log = translation_prob_log
                    best_translation = i
            evaluate_result[matching_index] = list_of_targets[best_translation]
        return evaluate_result