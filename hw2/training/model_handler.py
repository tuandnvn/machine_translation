'''
Created on Mar 23, 2014

@author: Tuan
'''
from hw2.database.connection import DatabaseConnector
from hw2.dictionary.dictionary import Dictionary
from util import *
from hw2.util import SOURCE_KEY


class Model_Handler():
    def __init__(self, target_lan_file_name,
                 target_lang,
                 source_lan_file_name,
                 source_lang):
        '''
        we assume that language_1 is target (english), language_2 is foreign (spanish)
        '''
        self.target_lan_file_name = target_lan_file_name
        self.target_lang = target_lang
        self.source_lan_file_name = source_lan_file_name
        self.source_lang = source_lang     
        self.dictionary = {self.target_lang:Dictionary(), self.source_lang:Dictionary()}
    
    def saveDictionary(self, target_lang_dictionary_file_name, source_lang_dictionary_file_name):
        '''
        target_lang_dictionary_file_name is corresponding to target language (english), 
        source_lang_dictionary_file_name is corresponding to source language (spanish)
        '''
        self.dictionary[self.target_lang].saveToFile(target_lang_dictionary_file_name)
        self.dictionary[self.source_lang].saveToFile(source_lang_dictionary_file_name)
        
    def loadDictionary(self, target_lang_dictionary_file_name, source_lang_dictionary_file_name):
        '''
        target_lang_dictionary_file_name is corresponding to target language (english), 
        source_lang_dictionary_file_name is corresponding to source language (spanish)
        '''
        self.dictionary[self.target_lang].loadFromFile(target_lang_dictionary_file_name)
        self.dictionary[self.source_lang].loadFromFile(source_lang_dictionary_file_name)
        
    def getIndexes(self, tokens, language):
        '''
        Parameters: 
            - tokens: A sentence of either source or target language
            - language: language of line
        Return:
            - token_indices: token indices of line
        ''' 
        if 'dictionary' not in self.__dict__:
            raise Exception('Dictionary has not been built or loaded yet.')
        return [t for t in [self.dictionary[self.language].getIndex(token) 
                                for token in tokens] if t != None]
        
    def model_database_connect(self, model_file_name):
        self.database = DatabaseConnector(model_file_name)
        try:
            open(model_file_name, 'r')
        except Exception:
            self.database.createDatabase()
        self.database.setupConnection()
