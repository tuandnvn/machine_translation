'''
Created on Feb 4, 2014

@author: Tuan
'''
"""
Get rid of UTF-8 BOM
"""

import argparse
import time

from database.connection import DatabaseConnector


UTF_8_BOM = '\xef\xbb\xbf'
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--database', default=None, nargs = 1,
                      help='Specify dictionary database file name.')
    parser.add_argument('--create', default=None, action='store_false',
                      help='Create a new database.')
    parser.add_argument('--lookup', default=None, action='store_false',
                      help='Look up value from database.')
    parser.add_argument('--update', default=None, action='store_false',
                      help='Update a databse.')
    parser.add_argument('-i', '--input', default=None,  nargs = 1,
                      help='Input file.')
    
    begin_time = time.time()
    
    args = vars(parser.parse_args())
    dictionary_file = args['database'][0]
    input_file = args['input'][0]
    
    database = DatabaseConnector(dictionary_file)
    print dictionary_file
    try:
        open(dictionary_file,'r')
    except Exception:
        database.create_database()
    database.set_up_connection()
    
    
    if args['create'] != None or args['update'] != None:
        """
        Insert into database or update database
        """
        with open(input_file, 'r') as input_file:
            input_data = []
            for line in input_file:
                src_word, des_word, prob = line.split('\t')
                if src_word[:len(UTF_8_BOM)] == UTF_8_BOM:
                    src_word = src_word[len(UTF_8_BOM):]
                src_word = src_word.strip()
                des_word = des_word.strip()
                prob = prob.strip()
                input_data.append( (src_word, des_word, float(prob)) )
            if args['create'] != None:
                database.insert_many(input_data)
            else:
                database.update_many(input_data)
                
    if args['lookup'] != None:
        """
        Look up some values
        """
        with open(input_file, 'r') as input_file:
            input_data = []
            for line in input_file:
                src_word, des_word = line.split('\t')
                if src_word[:len(UTF_8_BOM)] == UTF_8_BOM:
                    src_word = src_word[len(UTF_8_BOM):]
                src_word = src_word.strip()
                des_word = des_word.strip()
                if src_word == '':
                    src_word = None
                elif des_word == '':
                    des_word = None
                result = database.select(src_word, des_word)
    
    print str(time.time() - begin_time)