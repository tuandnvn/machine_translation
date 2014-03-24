'''
Created on Feb 4, 2014

@author: Tuan
'''
from sqlite3 import IntegrityError
import sqlite3
from hw2.util import *


class DatabaseConnector(object):
    '''
    classdocs
    '''


    def __init__(self, database_file_name):
        '''
        Constructor
        '''
        self.database_file_name = database_file_name
    
    def setupConnection(self):
        self.conn = sqlite3.connect(self.database_file_name)
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        
    def closeConnection(self):
        self.conn.close()
        
    def createDatabase(self):
        # Create table
        self.setupConnection()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Word_pair_prob
                     (%s integer, %s integer, %s real, 
                     PRIMARY KEY(%s, %s))''' 
                     % (SOURCE_KEY, TARGET_KEY, PROBABILITY_KEY, 
                        SOURCE_KEY, TARGET_KEY))
        
    def update(self, src, tar, prob):
        ## Insert team information into Team table
        try:
            self.c.execute("INSERT INTO Word_pair_prob VALUES (%d,%d,%d)" %(src, tar, prob) )
        except IntegrityError:
            try:
                self.c.execute("UPDATE Word_pair_prob SET %s=%d WHERE %s=%d AND %s=%d" %(PROBABILITY_KEY, prob, SOURCE_KEY, src, TARGET_KEY, tar) )
            except IntegrityError as e:
                print e
    
    def commit(self):
        self.conn.commit()
        
    def insertMany(self, list_of_values ):
        try:
            self.c.executemany("INSERT INTO Word_pair_prob VALUES (?,?,?)", list_of_values )
            self.commit()
        except IntegrityError as e:
            print e
             
    def updateMany(self, list_of_values):
        for values in list_of_values:
            try:
                self.c.execute("INSERT INTO Word_pair_prob VALUES (?,?,?)", values )
                self.commit()
            except IntegrityError as e:
                self.c.execute("UPDATE Word_pair_prob SET %s=? WHERE %s=? AND %s=?" 
                               %(PROBABILITY_KEY, SOURCE_KEY, TARGET_KEY), values)
                self.commit()
    
    def printAll(self):
        self.c.execute('''SELECT * FROM Word_pair_prob''')
        results = self.c.fetchall()
        for result in results:
            print result
            
    def select(self, src, tar):
        if src == None:
            self.c.execute('''SELECT SUM(Prob) FROM Word_pair_prob WHERE %s=?''',(tar, TARGET_KEY))
        elif tar == None:
            self.c.execute('''SELECT SUM(Prob) FROM Word_pair_prob WHERE %s=? ''',(src, SOURCE_KEY))
        else:
            self.c.execute('''SELECT Prob FROM Word_pair_prob WHERE %s=? AND %s=?''',(src, tar, SOURCE_KEY, TARGET_KEY))
        result = self.c.fetchone()
        if result != None:
            prob = result[0]
            return prob
        
    def countNumberOfTargetIndices(self):
        self.c.execute('''SELECT COUNT(DISTINCT %s) FROM Word_pair_prob ''',( TARGET_KEY ))
        result = self.c.fetchone()
        if result != None:
            count = result[0]
            return count
    
    def countNumberOfSourceIndices(self):
        self.c.execute('''SELECT COUNT(DISTINCT %s) FROM Word_pair_prob ''',( SOURCE_KEY ))
        result = self.c.fetchone()
        if result != None:
            count = result[0]
            return count
        
    def selectAll(self):
        self.c.execute('''SELECT * FROM Word_pair_prob''')
        results = self.c.fetchall()
        for result in results:
            yield {SOURCE_KEY: result[0], TARGET_KEY: result[1], PROBABILITY_KEY: result[2]}