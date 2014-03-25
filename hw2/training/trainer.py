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
                 target_dict_file_name,
                 source_lan_file_name,
                 source_lang,
                 source_dict_file_name,
                 no_of_iterations,
                 model_file_name):
        '''
        Arguments:
        target_lan_file_name -- string, file name of target language  
        target_lang -- string, target language string 
        source_lan_file_name -- string, file name of source language  
        source_lang -- string, source language string
        '''
        Model_Handler.__init__(self, target_lan_file_name, target_lang,
                               target_dict_file_name,
                               source_lan_file_name, source_lang,
                               source_dict_file_name)
        self.list_of_parallel_sentences = []
        self.t_e_f = None
        self.log_likelihood = None
        
        self.no_of_iterations = no_of_iterations
        self.model_file_name = model_file_name
    
    def train(self):
        self.init_list_of_parallel_sentences()
        self.buildDictionarySaveToFile()
        self.runEMTrainingLoop()
        self.saveToModelFile()
        
    def init_list_of_parallel_sentences(self):
        """
        Init parallel sentences for runEMTrainingLoop data only
        """
        temporary = [[], []]
        with codecs.open(self.target_lan_file_name, 'r', CODEC) as target_file_handler:
            for target_line in target_file_handler:
                target_line = Trainer.cleanLine(target_line)
                temporary[0].append(target_line)
        with codecs.open(self.source_lan_file_name, 'r', CODEC) as source_file_handler:
            for source_line in source_file_handler:
                source_line = Trainer.cleanLine(source_line)
                temporary[1].append(source_line)
        if len(temporary[0]) != len(temporary[1]):
            raise Exception('Two files doesn\'t have the same number of sentences')
        
        for i in xrange(len(temporary[0])):
            self.list_of_parallel_sentences.append((temporary[0][i], temporary[1][i]))
                
    def buildDictionary(self):
        self.list_of_parallel_indices = []
        for (target_line, source_line) in self.list_of_parallel_sentences:
            target_tokens, source_tokens = (target_line.split(' '), source_line.split(' '))
            self.dictionary[self.target_lang].feedTokens(target_tokens)
            self.dictionary[self.source_lang].feedTokens(source_tokens)
            (target_token_indices, source_token_indices) = (self.getIndices(target_tokens, self.target_lang),
                                                  self.getIndices(source_tokens, self.source_lang))
            self.list_of_parallel_indices.append((len(target_tokens), target_token_indices,
                                                  len(source_tokens), source_token_indices))
        self.target_lexicon_size = self.dictionary[self.target_lang].getDictSize()
        self.source_lexicon_size = self.dictionary[self.source_lang].getDictSize()
        print 'self.target_lexicon_size '+ str(self.target_lexicon_size)
        print 'self.source_lexicon_size '+ str(self.source_lexicon_size)
    
    def buildDictionarySaveToFile(self):
        '''
        dictionary_file_name_1 is corresponding to target language (english), 
        dictionary_file_name_2 is corresponding to source language (spanish)
        '''
        self.buildDictionary()
        self.saveDictionary()
        
    def saveToModelFile(self):
        self.model_database_connect(self.model_file_name)
        
        input_data = []
        for i in xrange(self.target_lexicon_size):
            for j in xrange(self.source_lexicon_size):
                input_data.append((j, i, float(self.t_e_f[i, j])))
        self.database.insertMany(input_data)
        
    def _defaultCheck(self):
        '''
        Check the condition of convergence
        '''
        if 't_e_f' not in self.__dict__:
            raise Exception('Translation model has not been built yet. Only use with runEMTrainingLoop.')
    
    def checkConvergence(self):
        '''
        We will calculate the log-likelihood
        log P ( target sentences | source sentences, model parameters) = 
                        SUM ( log (target sentence | source sentence, model parameters) )
        '''
        log_likelihood = 0
        for (target_length, target_token_indices,
            source_length, source_token_indices) in self.list_of_parallel_indices:
            log_likelihood += self.calculateTranslationProbability(target_length, 
                                                                   target_token_indices, 
                                                                   source_length, 
                                                                   source_token_indices)
        
        print 'log_likelihood ' + log_likelihood
        if self.log_likelihood == None:
            self.log_likelihood = log_likelihood
            return False
        if np.abs(log_likelihood - self.log_likelihood) < CONVERGENCE_DIFFERENCE:
            self.log_likelihood = log_likelihood
            return False
        self.log_likelihood = log_likelihood
        
    def runEMTrainingLoop(self, convergence_check=_defaultCheck):
        '''
        '''
        """
        t(e|f) is t_e_f
        we assume that target (e) is english, f is foreign (spanish)
        """
        self.t_e_f = np.zeros((self.target_lexicon_size, self.source_lexicon_size))
        
        """
        Uniformly initiated
        """
        self.t_e_f.fill(1 / (self.target_lexicon_size * self.source_lexicon_size))
        
        """
        count(e|f) is c_e_f
        """
        self.c_e_f = np.zeros((self.target_lexicon_size, self.source_lexicon_size))
        self.total_f = np.zeros(self.source_lexicon_size)
        
        for i in xrange(self.no_of_iterations):
            print 'Iteration ' + str(i)
            for (target_length, target_token_indices,
                 source_length, source_token_indices) in self.list_of_parallel_indices:
                s_total = defaultdict(float)
                for target_token_index in target_token_indices:
                    for source_token_index in source_token_indices:
                        s_total[target_token_index] += self.t_e_f[target_token_index, source_token_index]
                for target_token_index in target_token_indices:
                    for source_token_index in source_token_indices:
                        self.c_e_f[target_token_index, source_token_index] += \
                                 self.t_e_f[target_token_index, source_token_index] / s_total[target_token_index]
                        self.total_f[source_token_index] += \
                                 self.t_e_f[target_token_index, source_token_index] / s_total[target_token_index]
                        
            self.t_e_f = self.c_e_f / self.total_f
