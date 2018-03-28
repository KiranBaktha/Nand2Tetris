class CodeWriter:
    '''
    CodeWriter class contains the reference table betwen VM code and the assembly code. It is used as a reference for every
    VM line.
    '''
    def __init__(self):
        self.table = {'sub': '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n'+'M=M-D'+'\n',
      'neg': '@SP' + '\n' + 'A=M-1' + '\n' + 'M=-M' +'\n',
      'add': '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n'+'M=M+D'+'\n',
      'gt': '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n'+ 'D=M-D' + '\n' + '@FALSENO' + '\n' + 'D;JLE' + '\n' + '@SP' + '\n' + 'A=M-1' + '\n' + 'M=-1' + '\n' + '@CONTINUENO' + '\n' + '0;JMP' + '\n' + '(FALSENO)' + '\n' + '@SP' + '\n' + 'A=M-1' + '\n' + 'M=0' + '\n' + '(CONTINUENO)' + '\n',
      'lt' : '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n'+ 'D=M-D' + '\n' + '@FALSENO' + '\n' + 'D;JGE' + '\n' + '@SP' + '\n' + 'A=M-1' + '\n' + 'M=-1' + '\n' + '@CONTINUENO' + '\n' + '0;JMP' + '\n' + '(FALSENO)' + '\n' + '@SP' + '\n' + 'A=M-1' + '\n' + 'M=0' + '\n' + '(CONTINUENO)' + '\n',
      'eq': '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n'+ 'D=M-D' + '\n' + '@FALSENO' + '\n' + 'D;JNE' + '\n' + '@SP' + '\n' + 'A=M-1' + '\n' + 'M=-1' + '\n' + '@CONTINUENO' + '\n' + '0;JMP' + '\n' + '(FALSENO)' + '\n' + '@SP' + '\n' + 'A=M-1' + '\n' + 'M=0' + '\n' + '(CONTINUENO)' + '\n',
      'not' : '@SP' + '\n' + 'A=M-1' + '\n' + 'M=!M' + '\n',
      'and' : '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n'+'M=D&M'+'\n',
      'or' : '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n'+'M=D|M'+'\n',
      'push argument': 'D=A' + '\n' + '@ARG' + '\n' + 'A=D+M' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'push local': 'D=A' + '\n' + '@LCL' + '\n' + 'A=D+M' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'push constant': 'D=A' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n',
      'push this': 'D=A' + '\n' + '@THIS' + '\n' + 'A=D+M' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'push that': 'D=A' + '\n' + '@THAT' + '\n' + 'A=D+M' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'push temp': 'D=A' + '\n' + '@5' + '\n' + 'A=D+A' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'push pointer': 'D=A' + '\n' + '@R3' + '\n' + 'A=D+A' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'push static':  '@XXY' + '\n' + 'D=M' + '\n'+ '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'pop this': 'D=A' + '\n' + '@R3' + '\n' + 'D=D+M' + '\n' + '@R195' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R195' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop that': 'D=A' + '\n' + '@R4' + '\n' + 'D=D+M' + '\n' + '@R195' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R195' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop pointer': 'D=A' + '\n' + '@3' + '\n' + 'D=D+A' + '\n' + '@R195' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R195' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop temp': 'D=A' + '\n' + '@5' + '\n' + 'D=D+A' + '\n' + '@R195' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R195' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop argument': 'D=A' + '\n' + '@ARG' + '\n' + 'D=D+M' + '\n' + '@R195' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R195' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop local': 'D=A' + '\n' + '@LCL' + '\n' + 'D=D+M' + '\n' + '@R195' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R195' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop static': '@SP' + '\n' + 'A=M-1' + '\n' + 'D=M' + '\n' + '@XXY' + '\n' + 'M=D' +  '\n' + '@SP' + '\n' + 'M=M-1' + '\n'}
        self.counter = 0
        self.fcounter = 0
    
    def getAssemblyCode(self,command,fname):
        '''
        Function that recieves the VM code and returns the respective assembly code.
        '''
        word = command.split(' ')[0]
        if 'label' == word:
            return self.writeLabel(command.split(' ')[1])
        elif 'if-goto' == word:
            return self.writeIf(command.split(' ')[1])
        elif 'goto' == word:
            return self.writeGoto(command.split(' ')[1])
        elif 'function' == word:
            li = command.split(' ')
            return self.writeFunction(li[1],li[2])
        elif 'call' ==word:
            li = command.split(' ')
            return self.writeCall(li[1],li[2])
        elif 'return' ==word:
            return self.writeReturn()
        command = command.rsplit(' ',1) #Split from right once
        if len(command) ==1:
            if command[0] in ['gt','lt','eq']:
                code = self.table[command[0]].replace('NO',str(self.counter))
                self.counter+=1
                return code
            else:
                code = self.table[command[0]]
                return code
        else:
            if 'static' in command[0]:
                code = (self.table[command[0]]).replace('XXY',fname + '.' + command[1])
            else:
                code = '@' + command[1] + '\n' + self.table[command[0]]
            return code
    
    def wrt(self):
        return 'NEXT LINE' + '\n'
            
    def writeInit(self):
        '''
        Initial Code. Initialize Stack Pointer and Call Sys.init
        '''
        code1 = '@256' + '\n' + 'D=A' + '\n' +  '@SP' + '\n' + 'M=D' + '\n'
        code2 = self.writeCall('Sys.init',0)
        return code1 + code2
    
    def push_Stack(self,register):
        '''
        Pushes the input register to the stack
        '''
        code = '@SP' + '\n' + 'A=M' + '\n' + 'M=' + register + '\n' + '@SP' + '\n' + 'M=M+1' + '\n'
        return code
        
    def writeCall(self,Name,arguments):
        '''
        Writes assembly code that effects the call command.
        '''
        self.fcounter +=1
        code = '@return' + str(self.fcounter) + '\n' + 'D=A' + '\n'
        code+=self.push_Stack('D')
        code+= '@LCL' + '\n' + 'D=M' + '\n' + self.push_Stack('D')
        code+= '@ARG' + '\n' + 'D=M' + '\n' + self.push_Stack('D')
        code+= '@THIS' + '\n' + 'D=M' + '\n' + self.push_Stack('D')
        code+= '@THAT' + '\n' + 'D=M' + '\n' + self.push_Stack('D')
        code+= '@SP' + '\n' + 'D=M' + '\n' + '@' + str(int(arguments) + 5) + '\n' +'D=D-A' + '\n' + '@ARG' + '\n' + 'M=D' + '\n' # ARG = SP-n-5
        code+= '@SP' + '\n' + 'D=M' + '\n' + '@LCL' + '\n' + 'M=D' + '\n' #LCL = SP
        code += self.writeGoto(Name)
        code +=self.writeLabel('return' + str(self.fcounter))
        return code
    
    def restore(self,segment):
        '''
        Restores the segment after function call return
        '''
        code1 = '@R99' +  '\n' + 'M=M-1' + '\n' + 'A=M' + '\n' + 'D=M' + '\n' + '@' + segment + '\n' + 'M=D' + '\n'
        return code1
    
    def writeReturn(self):
        '''
        Writes assembly code that effects the return command.
        '''
        code = '@LCL' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'M=D' + '\n' +  '@5' + '\n' + 'D=A' + '\n' + '@R99' + '\n' + 'D=M-D' + '\n'
        code+= 'A=D' + '\n' + 'D=M' + '\n' + '@R100' + '\n' + 'M=D' + '\n'
        code+= '@0' + '\n' + 'D=A' + '\n' + '@ARG' + '\n' + 'A=M' + '\n' + 'D=A+D' + '\n' + '@R13' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + 'A=M' + '\n' + 'D=M' + '\n' + '@R13' + '\n' + 'A=M' + '\n' + 'M=D' + '\n'
        code+= '@ARG' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'M=D+1' + '\n'
        code += self.restore('THAT')
        code += self.restore('THIS')
        code += self.restore('ARG')
        code += self.restore('LCL')
        code += '@R100' + '\n' + 'A=M' + '\n' +'0;JMP' + '\n'
        return code
        
        
    
    def writeLabel(self,label):
        '''
        Writes assembly code that effects the label command.
        '''
        code = '(' + label + ')' + '\n'
        return code
        
    def writeFunction(self,Name,numLocals):
        '''
        Writes assembly code that effects the function command.
        '''
        code1 = self.writeLabel(Name)
        code2  = ''
        for i in range(int(numLocals)):
            code2 +=  '@SP' + '\n' + 'A=M' + '\n' + 'M=0' + '\n' + '@SP' + '\n' + 'M=M+1' +'\n'
        return code1 + code2
            
            
    def writeIf(self,label):
        '''
        Writes assemby code that effects the if-goto command.
        '''
        code = '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + '@' + label + '\n' + 'D;JNE' + '\n'
        return code
    
    def writeGoto(self,label):
        '''
        Writes assemby code that effects the if-goto command.
        '''
        code = '@' + label + '\n' + '0;JEQ' + '\n'
        return code
    
    def wrtn(self):
        '''
        Debug purpose
        '''
        return 'NEXT FILE' + '\n'
        
