'''
Created on Mar 23, 2014

@author: Tuan
'''
from hw2.database.connection import DatabaseConnector
from hw2.dictionary.dictionary import Dictionary
from hw2.util import SOURCE_KEY
import numpy as np
from hw2.util import *


class MTModelHandler():
    '''
    A handler for machine translation, handling input corpus of parallel sentences,
    dictionary files to map between lexicons and indices. 
    '''
    
    def __init__(self, target_lan_file_name,
                 target_lang,
                 target_dict_file_name,
                 source_lan_file_name,
                 source_lang,
                 source_dict_file_name,
                 model_file_name,
                 verbatim):
        '''
        we assume that language_1 is target (english), language_2 is foreign (spanish)
        '''
        self.target_lan_file_name = target_lan_file_name
        self.target_lang = target_lang
        self.target_dict_file_name = target_dict_file_name
        
        self.source_lan_file_name = source_lan_file_name
        self.source_lang = source_lang
        self.source_dict_file_name = source_dict_file_name
        
        self.model_file_name = model_file_name
        self.dictionary = {self.target_lang:Dictionary(), self.source_lang:Dictionary()}
        self.verbatim = verbatim
    
    def saveDictionary(self):
        '''
        target_lang_dictionary_file_name is corresponding to target language (english), 
        source_lang_dictionary_file_name is corresponding to source language (spanish)
        '''
        self.dictionary[self.target_lang].saveToFile(self.target_dict_file_name)
        self.dictionary[self.source_lang].saveToFile(self.source_dict_file_name)
        
    def loadDictionary(self):
        '''
        target_lang_dictionary_file_name is corresponding to target language (english), 
        source_lang_dictionary_file_name is corresponding to source language (spanish)
        '''
        self.dictionary[self.target_lang].loadFromFile(self.target_dict_file_name)
        self.dictionary[self.source_lang].loadFromFile(self.source_dict_file_name)
        
    def getIndices(self, tokens, language):
        '''
        Parameters: 
            - tokens: A sentence of either source or target language
            - language: language of line
        Return:
            - token_indices: token indices of line
        ''' 
        if 'dictionary' not in self.__dict__:
            raise Exception('Dictionary has not been built or loaded yet.')
        return [t for t in [self.dictionary[language].getIndex(token) 
                                for token in tokens] if t != None]
    
    def calculateTranslationProbability(self, target_length,
                                        target_token_indices,
                                        source_length,
                                        source_token_indices):
        '''
        Calcualte the translation probability based on the IBM model
        log( target_sentence| source_sentence ) = - len(target_sentence)*log( len(source_sentence) ) 
                                                + SUM_over_target ( log ( SUM_over_source( t_target_source )))
                                                
        Note that target_length is different from len(target_token_indices) 'cause 
        target_token_indices might doesn't include some tokens which lack in the training.
        
        Arguments:
        target_length -- length of the target sentence
        target_token_indices -- indices of token given in the target sentence
        source_length -- length of the source sentence
        source_token_indices -- indices of token given in the source sentence
        '''
        sum_over_target = 0
        for target_token_index in target_token_indices:
            sum_over_source = 0
            for source_token_index in source_token_indices:
                sum_over_source += self.t_e_f[target_token_index, source_token_index]
            sum_over_target += np.log(sum_over_source)
        
        """
        Here instead of using source_length + 1, I use source_length 
        only and assume that source_length would already include the NULL token
        """
        translation_prob_log = sum_over_target - target_length * np.log(source_length)
        return translation_prob_log
       
    def modelDatabaseConnect(self, model_file_name):
        '''
        '''
        self.database = DatabaseConnector(model_file_name)
        try:
            open(model_file_name, 'r')
        except Exception:
            self.database.createDatabase()
        self.database.setupConnection()
    
    def lineTokenizer(self, line, language, language_option ):
        line_tokens = line.split(' ')
        line_length = len(line_tokens)
        return (line_length, line_tokens)
    
    @staticmethod
    def cleanLine(line):
        line = line.strip()
        for ENDING_STR in ENDING_STRS:
            if line.endswith(ENDING_STR):
                line = line[:-len(ENDING_STR)]
        for BEGINNING_STR in BEGINNING_STRS:
            if line.startswith(BEGINNING_STR):
                line = line[len(BEGINNING_STR) + 1:]
        return line
