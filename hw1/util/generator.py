'''
Created on Feb 4, 2014

@author: Tuan
'''
import random
import string
import sys


class Generator():
    '''
    A generator to generate 100,000 word pairs
    '''


    def __init__(self, dict_input_file, dict_update_file, dict_lookup_file ):
        '''
        Constructor
        '''
        self.dict_input_file = dict_input_file
        self.dict_update_file = dict_update_file
        self.dict_lookup_file = dict_lookup_file
    
    def generate(self):
        self.src_number = 10000
        self.des_number = 10000
        self.src = set()
        self.des = set()
        letters = string.ascii_lowercase
        for i in xrange(self.src_number):
            no_of_letters = random.randint(3,8)
            new_str = ''.join(random.choice(letters) for x in range(no_of_letters))
            self.src.add(new_str)
        self.src = list(self.src)
        self.src_number = len(self.src)
        for i in xrange(self.des_number):
            no_of_letters = random.randint(3,8)
            new_str = ''.join(random.choice(letters) for x in range(no_of_letters))
            self.des.add(new_str)
        self.des = list(self.des)
        self.des_number = len(self.des)
        
        with open(self.dict_input_file, 'w') as dict_input_file: 
            with open(self.dict_update_file, 'w') as dict_update_file:
                with open(self.dict_lookup_file, 'w') as dict_lookup_file: 
                    for i in xrange(self.src_number):
                        deses = [self.des[t] for t in set([random.randint(0,self.des_number - 1) for x in range(10)])]
                        for des in deses:
                            dict_input_file.write( '%s\t%s\t%0.2f\n' % ( self.src[i] , des, random.random())) 
                            if random.randint(1,3) == 1:
                                dict_update_file.write( '%s\t%s\t%0.2f\n' % ( self.src[i] , des, random.random()))
                            if random.randint(1,5) == 1:
                                dict_lookup_file.write( '%s\t%s\n' % ( self.src[i] , des))
                        dict_lookup_file.write('%s\t \n' % ( self.src[i] ))
                        
if __name__ == '__main__':
    random_input, random_update, random_lookup = sys.argv[1:4]
    gen = Generator(random_input, random_update, random_lookup)
    gen.generate()