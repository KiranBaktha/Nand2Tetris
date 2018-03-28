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
      'push static': 'D=A' + '\n' + '@16' + '\n' + 'A=D+A' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1'+'\n',
      'pop this': 'D=A' + '\n' + '@R3' + '\n' + 'D=D+M' + '\n' + '@R99' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop that': 'D=A' + '\n' + '@R4' + '\n' + 'D=D+M' + '\n' + '@R99' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop pointer': 'D=A' + '\n' + '@3' + '\n' + 'D=D+A' + '\n' + '@R99' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop temp': 'D=A' + '\n' + '@5' + '\n' + 'D=D+A' + '\n' + '@R99' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop argument': 'D=A' + '\n' + '@ARG' + '\n' + 'D=D+M' + '\n' + '@R99' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop local': 'D=A' + '\n' + '@LCL' + '\n' + 'D=D+M' + '\n' + '@R99' + '\n' + 'M=D' + '\n' + '@SP' + '\n' +'AM=M-1' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'A=M' + '\n' + 'M=D' + '\n',
      'pop static': 'D=A' + '\n'+'@16'+ '\n' + 'D=D+A' + '\n' + '@R99' +'\n' + 'M=D' + '\n' + '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + '@R99' + '\n' + 'A=M' + '\n' + 'M=D' + '\n'}
        self.counter = 0
    
    def getAssemblyCode(self,command):
        '''
        Function that recieves the VM code and returns the respective assembly code.
        '''
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
            code = '@' + command[1] + '\n' + self.table[command[0]]
            return code
            




