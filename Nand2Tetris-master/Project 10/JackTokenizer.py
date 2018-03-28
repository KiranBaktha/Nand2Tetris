import re

Symbols = "{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"

Keywords = ['class', 'method', 'function', 'constructor', 
            'int', 'boolean', 'char', 'void', 
            'var', 'static', 'field', 'let', 
            'do', 'if', 'else', 'while', 
            'return', 'true', 'false', 'null', 
            'this']

Token_type =  { 
                'KEYWORD'       : 0,
                'SYMBOL'        : 1, 
                'IDENTIFIER'    : 2, 
                'INT_CONST'     : 3, 
                'STRING_CONST'  : 4
            }

Symbol_List = ['{', "}", '(', ')', 
                '[', ']', '.', ',', ';',
                '+', '-', '/', '&', '|', 
                '<', '>', '=', '~'
            ]

op = ['+', '-', '*', '/', '&', 
      '|', '<', '>', '=' ]

class JackTokenizer(object):
    '''
    Tokenizer that releases tokens to be compiled by the Compilation Engine
    '''
    
    def __init__(self, file_name):
        '''
        Constructor
        '''
        self._file_name = file_name
        self._file_object = open(file_name)
        self._lines = []
        self._tokens = []
        self._current_token = None
        self._current_token_index = 0
        self._len_tokens = 0

    def split(self, line):
        '''
        Splits input code by space and symbols. Returns a list.
        '''
        tokens = []
        space_septd = line.split() #Split on space
        for s_token in space_septd:
            tokens += re.split('(' + Symbols +  ')', s_token) #Split on Jack Symbols
        return [s for s in tokens if s != '']
        
    def removeNoise(self):
        '''
        Removes white space and comments
        '''
        comment = False
        for line in self._file_object.readlines():
            line = line.strip()
            if len(line) == 0:
                continue 
            elif line[0:3] == '/**' or line[0:2] == '/*': #Multiline comments
                comment = True
                continue
            elif line[0] == '*':
                continue
            elif line[0] == '*' and line[-2:] == '*/' and comment == True:
                comment = False
                continue
            elif line[-2:] == '*/' and comment == True:
                comment = False
                continue
            elif line.find('//') != -1:  #Single line comments
                if len(line[:line.find('//')]) == 0:
                    continue
                self._lines.append(line[:line.find('//')])
            else:
                self._lines.append(line)
    
    
    def print_tokens(self):
        '''
        Useful if we want to view the tokens.
        '''
        for idx in range(self._len_tokens):
            print (self._tokens[idx])
          
    def prepare_tokens(self):
        '''
        Prepares tokens for compilation engine. Takes care to tokens which should be treated
        as a String Constant.
        '''
        for line in self._lines:
            x = line.split('"')
            if len(x) ==1:
                self._tokens += self.split(x[0])  # No String Constant Present
            else:
                for i in range(len(x)):
                    if i%2==0:
                        self._tokens += self.split(x[i])
                    else:
                        self._tokens = self._tokens + ['"' +  x[i] + '"']
        
        self._len_tokens = len(self._tokens)
        return self._tokens
        
    def next_token(self,prev = False):
        '''
        Get the next token. prev is set when unary operators are used. 
        '''
        if prev:
            self._current_token_index-=2  # Go back a token. (Based on my logic in CompilationEngine)
        if self._current_token_index < self._len_tokens:
            token = self._tokens[self._current_token_index]
            self._current_token = token
            self._current_token_index += 1
            return token
        else:
            return 'NO_MORE_TOKENS'
        
    def expected_token(self):
        """
        Needed for subroutines and arrays when we want to look ahead.
        """
        if self._current_token_index < self._len_tokens:
            return self._tokens[self._current_token_index]
        else:
            return 'NO_MORE_TOKENS'
        
    def token_type(self):
        '''
        Returns the type of token.
        '''
        if self._current_token in Symbol_List:
            return 'SYMBOL'
        elif self._current_token in Keywords:
            return 'KEYWORD'
        elif self._current_token.isdigit():
            return 'INT_CONST'
        elif self._current_token.find('"') != -1 or self._current_token[0] == '-':
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'
        
    def identifier(self):
        return self._current_token
    
    def symbols(self):
        return self._current_token
    
    def intval(self):
        return self._current_token
    
    def stringval(self):
        return self._current_token
        
    def keyword(self):
        return self._current_token