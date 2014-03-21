'''
Created on Mar 21, 2014

@author: Tuan
'''
import json

class Dictionary(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
        self._word_to_index = {}
        self._index_to_word = []
    
    def feedWords(self, list_of_words):
        for word in list_of_words:
            if word not in self._word_to_index:
                self._index_to_word.append(word)
                self._word_to_index[word] = len(self._index_to_word)
    
    def getDictSize(self):
        return len(self._index_to_word)
    
    def saveToFile(self, file_name):
        with open(file_name, 'w') as file_handler:
            json.dump( self._index_to_word, file_handler )
    
    def loadFromFile(self, file_name):
        with open(file_name, 'r') as file_handler:
            json.load( self._index_to_word, file_handler )
            self._word_to_index = {} 
            for i in xrange(len(self._index_to_word)):
                self._word_to_index[self._index_to_word[i]] = i 