import sys

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

class CompliationEngine(object):
    '''
    Compilation Engine that compiles tokens and writes them to a XML file.
    '''
    MAP = { '<' : "&lt;",
            '>' : "&gt;",
            '"' : "&quot;",
            '&' : "&amp;"
    }
    def __init__(self, tokenizer, out_file_name):
        '''
        Constructor
        '''
        self._tokenizer = tokenizer
        self._out_file_name = out_file_name
        self._out_file_object = open(out_file_name, 'w')  # File to be written to
         
    def Compile(self):
        '''
        Start compilation. Note: The Jack Program must start with a Class based on the book.
        '''
        token = str(self._tokenizer.next_token())
        if token == 'class':
            self.CompileClass(token)          
        
    def CompileClass(self, token):
        '''
        Compile a class.
        '''
        temp_buffer = '<class>\n<keyword>' + token +\
                      '</keyword>'
        temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>" #Class name
        self._out_file_object.write(temp_buffer)
        
        token = self._tokenizer.next_token()
        if token == '{':
            temp_buffer = "\n<symbol>" + str(token) + "</symbol>"
            self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
            
        token = self._tokenizer.next_token()
        
        # For declaring Class Level Variable
         
        while token in ['field', 'static']:
            token = self.CompileClassVarDec(token)        
        
        # Class Methods
        if token in ['function', 'method', 'constructor']:
            token = self.CompileSubroutine(token)
            
        temp_buffer = "\n<symbol>" + str(token) + "</symbol>\n</class>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        self._out_file_object.close()
        
    def CompileSubroutine(self, token): 
        '''
        Compiles a Subroutine Declaration as per the Jack grammer
        '''
        temp_buffer = "\n<subroutineDec>\n<keyword>" + token + "</keyword>"
        if token == "constructor": # If a constructor
            temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
        else:
            temp_buffer += "\n<keyword>" + str(self._tokenizer.next_token()) + "</keyword>"
        temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
        temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        # Compiling Parameter List
        token = str(self._tokenizer.next_token())
        temp_buffer = ""
        if token != ')':
            temp_buffer = "\n<parameterList>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()   
                     
            token = self.CompileParamList(token)
            
            temp_buffer = "\n</parameterList>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            temp_buffer = ""
        else:
            temp_buffer += "\n<parameterList> \n</parameterList>"
        temp_buffer += "\n<symbol>" + token + "</symbol>"
        temp_buffer += "\n<subroutineBody>\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        # Compiling variable Declaration
        token = str(self._tokenizer.next_token())
        
        if token ==  "var":
            token = self.CompileVarDec(token)
        
        # Compiling Statements
        temp_buffer = "\n<statements>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        while token != "}": #Execute all statements
            token = self.CompileStatement(token)
            
          
        temp_buffer = "\n</statements>\n<symbol>" + token + "</symbol>\n</subroutineBody>\n</subroutineDec>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token()) 
        if token in ['function', 'method', 'constructor']: #Subroutine present
            token = self.CompileSubroutine(token)
        return token
    
    def CompileStatement(self, token):
        '''
        Checks which type of statement and redirects it to the appropriate statement.
        If None is passed it is highly likely the syntax is incorrect.
        '''
        if token is None:
            print('Oops the syntax seems incorrect.')
            sys.exit(0)
        if token == 'let':
            return self.CompileLet(token)
        elif token == 'do':
            return self.CompileDo(token)
        elif token == 'return':
            return self.CompileReturn(token)
        elif token == "if":
            return self.CompileIf(token)
        elif token == "while":
            return self.CompileWhile(token)
        elif token =="else":
            return self.CompileElse(token)
    
    def CompileWhile(self, token):
        '''
        Compiles a while statement as per the Jack grammer.
        '''
        temp_buffer = "\n<whileStatement>\n<keyword>" + token + "</keyword>"
        temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        token = self.CompileExpression(token) #Handle Expression
        temp_buffer = "\n<symbol>" + token + "</symbol>"
        temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>\n<statements>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        while token != '}': #Execute all expressions inside.
            token = self.CompileStatement(token)
            
        temp_buffer = "\n</statements>\n<symbol>" + token + "</symbol>\n</whileStatement>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        return token
    
    def CompileIf(self, token):
        '''
        Compiles an If statement as per the Jack Grammer.
        '''
        temp_buffer = "\n<ifStatement>\n<keyword>" + token + "</keyword>"
        temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        token = self.CompileExpression(token)
        temp_buffer = "\n<symbol>" + token + "</symbol>"
        temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>\n<statements>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        while token != '}': #Execute all statements inside
            token = self.CompileStatement(token)
            
        temp_buffer = "\n</statements>\n<symbol>" + token + "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        # optional else Command
        token = str(self._tokenizer.next_token())
        if token == "else":
            token = self.CompileElse(token)
        
        temp_buffer = "\n</ifStatement>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        return token
    
    
    def CompileElse(self, token):
        '''
        Compiles an else statement. I have seperated else from if statement.
        '''
        temp_buffer = "\n<keyword>" + token + "</keyword>"
        temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>\n<statements>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
                
        token = str(self._tokenizer.next_token())
        while token != '}': #Execute all statements inside
            token = self.CompileStatement(token)
            
        temp_buffer = "\n</statements>\n<symbol>" + token + "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        
        temp_buffer = ""
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        return token
        
    def CompileReturn(self, token):
        '''
        Compiles a return statement as per the Jack grammer.
        '''
        temp_buffer = "\n<returnStatement>\n<keyword>" + token + "</keyword>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        if token != ';':             # Optional expression present
            token = self.CompileExpression(token)
        
        temp_buffer = "\n<symbol>" + token + "</symbol>\n</returnStatement>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        token = str(self._tokenizer.next_token())
        return token
        
    def CompileDo(self, token):
        '''
        Compiles a do statement as per the Jack grammer.
        '''
        temp_buffer = "\n<doStatement>\n<keyword>" + token + "</keyword>"
        temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
        token = str(self._tokenizer.next_token()) #Handle as per subroutineCall rule in Jack
        if token == ".":
            temp_buffer += "\n<symbol>" + token + "</symbol>"
            temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
            temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>\n<expressionList> "
        else:    
            temp_buffer += "\n<symbol>" + token + "</symbol>\n<expressionList> "
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        if token != ')':
            token = self.CompilerExpressionList(token) #Compile the Expression List
        
        temp_buffer = "\n</expressionList>\n<symbol>" + token + "</symbol>"
        temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>\n</doStatement>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        token = str(self._tokenizer.next_token())
        return token
        
    def CompileLet(self, token):
        '''
        Compiles a let statement as per the Jack Grammer.
        '''
        temp_buffer = "\n<letStatement>\n<keyword>" + token + "</keyword>"
        temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        if token == '[': #Optional parameterized expression present.
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            
            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token) #Compile Expression
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
        
        temp_buffer = "\n<symbol>" + token +\
                         "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        # Handles the expression after the '=' in letstatement.
        token = str(self._tokenizer.next_token())
        token = self.CompileExpression(token)
        
        temp_buffer = "\n<symbol>" + token +\
                         "</symbol>\n</letStatement>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        return token
        
    def CompileExpression(self, token):
        '''
        Compiles an expression in the Jack Grammer.
        '''
        temp_buffer = "\n<expression>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        token = self.CompileTerm(token) #Go to term
        
        temp_buffer = "\n</expression>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        return token
    
    def CompileTerm(self, token,check = False):
        '''
        Compiles a Term in the Jack Language. Check is set for Unary operators.
        '''
        temp_buffer = "\n<term>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        if token.isdigit():
            temp_buffer = "\n<integerConstant>" + token + "</integerConstant>"
        elif token[0] == '"':
            temp_buffer = "\n<stringConstant>" + token.replace('"','') + "</stringConstant>"
        elif token in ['true', 'false', 'null', 'this']:
            temp_buffer = "\n<keyword>" + token + "</keyword>"
        elif token == '-':
            #Unary Operator
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            temp_buffer = ""
            token = str(self._tokenizer.next_token())
            token = self.CompileTerm(token,True)
        elif token == "~": #Handle not seperately
            return self.CompileNotOperator(token)
        elif token == "(":  
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token)
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            temp_buffer = ""
        elif self._tokenizer.expected_token() == "[": #Check next token
            temp_buffer = "\n<identifier>" + token + "</identifier>"
            temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            
            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token) #Handle expression
            
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            temp_buffer = ""
        elif self._tokenizer.expected_token() == ".": #Check next token
            temp_buffer = "\n<identifier>" + token + "</identifier>"
            temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) + "</symbol>"
            temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
            temp_buffer += "\n<symbol>" + str(self._tokenizer.next_token()) +\
                             "</symbol>\n<expressionList>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            
            token = str(self._tokenizer.next_token())
            if token != ")":
                token = self.CompilerExpressionList(token)
            
            temp_buffer = "\n</expressionList>\n<symbol>" + token + "</symbol>"
        else:
            temp_buffer = "\n<identifier>" + token + "</identifier>"          
                        
        temp_buffer += "\n</term>"
        
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        token = str(self._tokenizer.next_token())
        if check == True: #Unary Operator
            token = str(self._tokenizer.next_token(True))
        if token in op:
            if token in ['<', '>', '"', "&"]: #Need to be mapped
                token_map = CompliationEngine.MAP[token]
                temp_buffer = "\n<symbol>" + token_map + "</symbol>"
            else:
                temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
            token = self.CompileTerm(token)
        return token
    
    def CompileNotOperator(self, token):
        '''
        Compiles not operator. I have handled it seperately.
        '''
        temp_buffer = "\n<symbol>" + token + "</symbol>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        token = str(self._tokenizer.next_token())
        if token != '(':
            token = self.CompileTerm(token)
            temp_buffer = "\n</term>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            return token
        else:
            temp_buffer = "\n<term>\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token)
            
            temp_buffer = "\n<symbol>" + token + "</symbol>\n</term>\n</term>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
            return token
            
    def CompilerExpressionList(self, token):
        '''
        Compiles an expression list
        '''
        token =  self.CompileExpression(token)
        while token == ",": # More symbols in a line
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token)
        return token            
    
    def CompileVarDec(self, token):
        '''
        Compiles a variable declaration
        '''
        var_modifer = str(token)
        var_type = str(self._tokenizer.next_token())

        temp_buffer = "\n<varDec>\n<keyword>" + var_modifer + "</keyword>"
        if var_type in ['int', 'boolean', 'char']:
            temp_buffer += "\n<keyword>" + var_type + "</keyword>"
        else:
            temp_buffer += "\n<identifier>" + var_type + "</identifier>"
        temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
        
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = self._tokenizer.next_token()
        
        while token == ',': # Multiple identifiers in one line
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"            
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
        
        temp_buffer = "\n<symbol>" + token + "</symbol>\n</varDec>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = self._tokenizer.next_token()
        if token == 'var': # More variables
            return self.CompileVarDec(token)
        return token
    
    def CompileParamList(self,token):
        '''
        Compiles a (possibly empty) parameter list.
        '''
        temp_buffer = "\n<keyword>" + token + "</keyword>"
        temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = str(self._tokenizer.next_token())
        if token == ',': # More parameters
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
            return self.CompileParamList(token)
        return token
    
    def CompileClassVarDec(self, token):
        '''
        Compiles Class Variable Declarations (static declaration or field declaration)
        '''
        class_var_modifer = str(token)
        class_var_type = str(self._tokenizer.next_token())

        temp_buffer = "\n<classVarDec>\n<keyword>" + class_var_modifer + "</keyword>"
        if class_var_type in ['int', 'boolean', 'char']:
            temp_buffer += "\n<keyword>" + class_var_type + "</keyword>"
        else:
            temp_buffer += "\n<identifier>" + class_var_type + "</identifier>"
        temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"
        
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = self._tokenizer.next_token()
        
        while token == ',':  #While more declarations
            temp_buffer = "\n<symbol>" + token + "</symbol>"
            temp_buffer += "\n<identifier>" + str(self._tokenizer.next_token()) + "</identifier>"            
            self._out_file_object.write(temp_buffer)
            self._out_file_object.flush()
            token = str(self._tokenizer.next_token())
        
        temp_buffer = "\n<symbol>" + token + "</symbol>\n</classVarDec>"
        self._out_file_object.write(temp_buffer)
        self._out_file_object.flush()
        
        token = self._tokenizer.next_token()
        
        if token in ['field', 'static']:
            return self.CompileClassVarDec(token)
        
        return token       