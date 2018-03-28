from Parser import parser
from codewriter import CodeWriter
import sys
import os


def translate(filename,codewriter,check):
    '''
    Translates the code.
    '''
    code = []
    p = parser(filename)
    filename = os.path.basename(os.path.normpath(filename)).replace('.vm','')  # Filename for static variable handling.
    p.RemoveCommentsAndSpace()
    if check:
        code.append(codewriter.writeInit())
    while(p.HasAnyMoreCommands()):
        line = p.advance()
        code.append(codewriter.getAssemblyCode(line,filename))
        #code.append(codewriter.wrt())
    return code
    

        
if __name__=='__main__':
    filename = sys.argv[1]    
    if '.vm' in filename:
        result = filename.replace('.vm','.asm') # Resulting file to be written
        codewriter = CodeWriter()
        code = translate(filename,codewriter,True)  # Make this False if no bootstrap code.
        with open(result,'w') as file:
            for element in code:
                file.write(element)
        print('Completed')

    else:
        code = []
        codewriter = CodeWriter()
        di = os.path.basename(os.path.normpath(filename))
        result = os.path.join(filename,di + '.asm') # Resulting file to be written
        for root,dirs,files in os.walk(filename):
            for name in files:
                if '.vm' in name:
                    if len(code) ==0:
                        code += translate(os.path.join(filename,name),codewriter,True)  # Make this False if no bootstrap code.
                    else:
                        code += translate(os.path.join(filename,name),codewriter,False)
                    #code+= 'NEXT FILE' + '\n'
        with open(result,'w') as file:
            for element in code:
                file.write(element)
        print('Completed')
                


     
    