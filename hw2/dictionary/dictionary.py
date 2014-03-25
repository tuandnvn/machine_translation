'''
Created on Mar 21, 2014

@author: Tuan
'''
import json
from hw2.util import *

class Dictionary(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
        self._token_to_index = {}
        self._index_to_token = []
    
    def feedTokens(self, list_of_tokens):
        for token in list_of_tokens:
            if token not in self._token_to_index:
                self._index_to_token.append(token)
                self._token_to_index[token] = len(self._index_to_token) - 1
    
    def getToken(self, index):
        try:
            return self._index_to_token[index]
        except IndexError as ie:
            return None
        
    def getIndex(self, token):
        try:
            return self._token_to_index[token]
        except KeyError as ke:
            return None
            
    def getDictSize(self):
        return len(self._index_to_token)
    
    def saveToFile(self, file_name):
        with codecs.open(file_name, 'w', CODEC) as file_handler:
            json.dump( self._index_to_token, file_handler )
    
    def loadFromFile(self, file_name):
        with codecs.open(file_name, 'r', CODEC) as file_handler:
            self._index_to_token = json.load( file_handler )
            self._token_to_index = {} 
            for i in xrange(len(self._index_to_token)):
                self._token_to_index[self._index_to_token[i]] = i 