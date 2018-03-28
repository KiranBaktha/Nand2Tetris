from Parser import parser
from codewriter import CodeWriter
import sys
import os


def translate(filename):
    code = []
    p = parser(filename)
    p.RemoveCommentsAndSpace()
    codewriter = CodeWriter()
    while(p.HasAnyMoreCommands()):
        line = p.advance()
        code.append(codewriter.getAssemblyCode(line))
    return code
    

        
if __name__=='__main__':
    filename = sys.argv[1]
    if '.vm' in filename:
        result = filename.replace('.vm','.asm')
        code = translate(filename)
        with open(result,'w') as file:
            for element in code:
                file.write(element)
        print('Completed')

    else:
        code = []
        for root,dirs,files in os.walk(filename):
            for name in files:
                if '.vm' in name:
                    result = os.path.join(filename,name.replace('.vm','.asm'))
                    code += translate(os.path.join(filename,name))
        with open(result,'w') as file:
            for element in code:
                file.write(element)
        print('Completed')
                
        
    