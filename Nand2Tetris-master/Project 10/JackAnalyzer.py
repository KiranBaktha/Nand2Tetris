from JackTokenizer import JackTokenizer
from CompilationEngine import CompliationEngine
import sys


class JackAnalyzer(object):
    '''
    JackAnalyzer, top-level module that initializes and invokes the other modules
    '''


    def __init__(self, file_name):
        '''
        Constructor
        '''
        self._file_name = file_name
        self._tokenizer = None
    
    def tokenize(self):
        '''
        Tokenize and Compile
        '''
        self._tokenizer = JackTokenizer(self._file_name)
        self._tokenizer.removeNoise() # Remove white space and comments
        xx = self._tokenizer.prepare_tokens()
        #self._tokenizer.print_tokens()
        compilation_engine = CompliationEngine(self._tokenizer,  self._file_name.replace('.jack', '.xml'))
        compilation_engine.Compile()        
        return xx
    
if __name__=='__main__':
    jack_analyzer = JackAnalyzer(sys.argv[1])
    jack_analyzer.tokenize()
    print('Completed')




