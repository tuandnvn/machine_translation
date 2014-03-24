'''
Created on Feb 4, 2014

@author: Tuan
'''
import sqlite3
from sqlite3 import IntegrityError

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
                     (Src_word text, Des_word text, Prob real, PRIMARY KEY(Src_word, Des_word))''')
        
    def update(self, src, tar, prob):
        ## Insert team information into Team table
        try:
            self.c.execute("INSERT INTO Word_pair_prob VALUES ('%s','%s',%d)" %(src, tar, prob) )
        except IntegrityError:
            try:
                self.c.execute("UPDATE Word_pair_prob SET Prob=%d WHERE Src_word='%s' AND Des_word='%s'" %(prob, src, tar) )
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
                self.c.execute("UPDATE Word_pair_prob SET Prob=? WHERE Src_word=? AND Des_word=?" , values)
                self.commit()
    
    def printAll(self):
        self.c.execute('''SELECT * FROM Word_pair_prob''')
        results = self.c.fetchall()
        for result in results:
            print result
            
    def select(self, src, des):
        if src == None:
            self.c.execute('''SELECT SUM(Prob) FROM Word_pair_prob WHERE Des_word=?''',(des,))
        elif des == None:
            self.c.execute('''SELECT SUM(Prob) FROM Word_pair_prob WHERE Src_word=? ''',(src,))
        else:
            self.c.execute('''SELECT Prob FROM Word_pair_prob WHERE Src_word=? AND Des_word=?''',(src,des))
        result = self.c.fetchone()
        if result != None:
            prob = result[0]
            return prob