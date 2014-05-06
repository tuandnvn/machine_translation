'''
Created on Mar 20, 2014

@author: Tuan
'''
from collections import defaultdict
import json
import time

from hw2.database.connection import DatabaseConnector
from hw2.dictionary.dictionary import Dictionary
from hw2.training.model_handler import MTModelHandler
from hw2.util import *
import numpy as np


class Trainer(MTModelHandler):
    '''
    Trainer class handle all training routines.
    Inherit from MTModelHandler because it needs to deal with a model file 
        *(train the model and save into the model file)* 
    '''
    
    def __init__(self, target_lan_file_name,
                 target_lang,
                 target_dict_file_name,
                 source_lan_file_name,
                 source_lang,
                 source_dict_file_name,
                 no_of_iterations,
                 model_file_name,
                 convergence_difference,
                 verbatim):
        '''
        Arguments:
        target_lan_file_name -- string, file name of target language  
        target_lang -- string, target language string 
        source_lan_file_name -- string, file name of source language  
        source_lang -- string, source language string
        '''
        MTModelHandler.__init__(self, target_lan_file_name, target_lang,
                               target_dict_file_name,
                               source_lan_file_name, source_lang,
                               source_dict_file_name,
                               model_file_name,
                               verbatim)
        self.no_of_iterations = no_of_iterations
        self.convergence_difference = convergence_difference
        
        
        self.list_of_parallel_sentences = []
        self.t_e_f = None
        self.log_likelihood = None
    
    def isVerbatim(self):
        '''
        Return if the trainer is verbatim or not.
        '''
        return self.verbatim
    
    def train(self):
        '''
        Train the model given the input parallel corpus
        '''
        begin_time = time.time()
        self.initListOfParallelSentences()
        self.buildDictionarySaveToFile()
        print 'Time to build Dictionaries ' + str(time.time() - begin_time)
        
        begin_time = time.time()
        self.runEMTrainingLoop()
        print 'Time to run EM algorithm ' + str(time.time() - begin_time)
        
        begin_time = time.time()
        self.saveToNpyModelFile()
        print 'Time to save to model file ' + str(time.time() - begin_time)
        
    def initListOfParallelSentences(self):
        """
        Init parallel sentences for runEMTrainingLoop data
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
    
    def generateTokens(self, target_line, source_line):
        '''
        Given input of two lines, generate the tokens and length of sentence
        '''
        target_length, target_tokens = self.lineTokenizer(target_line, self.target_lang,
                                                          TARGET_LANGUAGE_OPTION)
        source_length, source_tokens = self.lineTokenizer(source_line, self.source_lang,
                                                          SOURCE_LANGUAGE_OPTION)
        return target_length, target_tokens, source_length, source_tokens    
    
             
    def buildDictionary(self):
        '''
        Feed the tokens from the training corpus to create two dictionaries 
        that match each token with an index
        '''
        self.list_of_parallel_indices = []
        for (target_line, source_line) in self.list_of_parallel_sentences:
            target_length, target_tokens, source_length, source_tokens = \
                            self.generateTokens(target_line, source_line)
            
            self.dictionary[self.target_lang].feedTokens(target_tokens)
            self.dictionary[self.source_lang].feedTokens(source_tokens)
            (target_token_indices, source_token_indices) = (self.getIndices(target_tokens, self.target_lang),
                                                  self.getIndices(source_tokens, self.source_lang))
            self.list_of_parallel_indices.append((target_length, target_token_indices,
                                                  source_length, source_token_indices))
        self.target_lexicon_size = self.dictionary[self.target_lang].getDictSize()
        self.source_lexicon_size = self.dictionary[self.source_lang].getDictSize()
        
        if self.isVerbatim():
            print 'self.target_lexicon_size ' + str(self.target_lexicon_size)
            print 'self.source_lexicon_size ' + str(self.source_lexicon_size)
    
    def buildDictionarySaveToFile(self):
        '''
        dictionary_file_name_1 is corresponding to target language (english), 
        dictionary_file_name_2 is corresponding to source language (spanish)
        '''
        self.buildDictionary()
        self.saveDictionary()
    
    def saveToDatabaseModelFile(self):
        self.modelDatabaseConnect(self.model_file_name)
        
        input_data = []
        for i in xrange(self.target_lexicon_size):
            for j in xrange(self.source_lexicon_size):
                input_data.append((j, i, float(self.t_e_f[i, j])))
        self.database.insertMany(input_data)
    
    def saveToNpyModelFile(self):
        np.save(self.model_file_name, self.t_e_f)
    
    def isConvergent(self):
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
        if self.isVerbatim():
            print 'log_likelihood ' + str(log_likelihood)
        if self.log_likelihood == None:
            self.log_likelihood = log_likelihood
            return False
        if np.abs(log_likelihood - self.log_likelihood) < self.convergence_difference:
            self.log_likelihood = log_likelihood
            return True
        self.log_likelihood = log_likelihood
        
    def runEMTrainingLoop(self):
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
        self.t_e_f.fill(float(1) / (self.target_lexicon_size))
        
        """
        count(e|f) is c_e_f
        """
        
        
        for i in xrange(self.no_of_iterations):
            self.c_e_f = np.zeros((self.target_lexicon_size, self.source_lexicon_size))
            self.total_f = np.zeros(self.source_lexicon_size)
            if self.isVerbatim():
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
            if self.isConvergent():
                break
            

class TrainerWithNull(Trainer):
    """
    Only to take into account the NULL token added into SOURCE sentence 
    when matching SOURCE and TARGET sentences.
    """
    def __init__(self, target_lan_file_name,
                 target_lang,
                 target_dict_file_name,
                 source_lan_file_name,
                 source_lang,
                 source_dict_file_name,
                 no_of_iterations,
                 model_file_name,
                 convergence_difference, 
                 isVerbatim):
        Trainer.__init__(self, target_lan_file_name, target_lang, 
                         target_dict_file_name, source_lan_file_name, 
                         source_lang, source_dict_file_name, 
                         no_of_iterations, model_file_name,
                         convergence_difference,
                         isVerbatim)
    
    """
    Overriding
    """
    def lineTokenizer(self, line, language, language_option ):
        line_tokens = line.split(' ')
        line_length = len(line_tokens)
        """
        Adding the NULL token here
        """
        if language_option == SOURCE_LANGUAGE_OPTION:
            line_tokens.append(None)
            line_length += 1
        return (line_length, line_tokens)