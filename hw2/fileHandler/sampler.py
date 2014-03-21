'''
Created on Mar 20, 2014

@author: Tuan
'''

class Sampler(object):
    '''
    A Sampler class read two parallel corpus and generate a set of n parallel sentences
    '''
    
    @classmethod
    def sample(clr, input_file_name_1,
                 input_file_name_2,
                 output_file_name_1,
                 output_file_name_2,
                 no_of_parralel_sentences):
        '''
        Constructor
        '''
        counter = 0
        with (open(input_file_name_1, 'r'),
              open(input_file_name_2, 'r'),
              open(output_file_name_1, 'w'),
              open(output_file_name_2, 'w')) as (file_handler_1,
                                            file_handler_2,
                                            file_handler_3,
                                            file_handler_4):
            for (line_1, line_2) in zip(file_handler_1, file_handler_2):
                if counter > no_of_parralel_sentences:
                    return
                counter += 1
                file_handler_3.write(line_1)
                file_handler_4.write(line_2)
