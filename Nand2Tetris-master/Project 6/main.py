import sys
import re

def Compute(x,y):
    """
    Compute is a function that takes 2 inputs, the first argument as x which is the file name
    and the second argument as y which is no-comments. This function was Project0.
    """
    with open(x,'r') as file:
        data = file.readlines()    

    for i in range(len(data)):
        data[i] = data[i].replace(' ','') #Remove Spaces
        data[i] = data[i].replace('\t','') # Remove Tabs
        data[i] = data[i].replace('\n','')  # Remove new line characters
        
    lines=[]
    for line in data:
        if line!='\n': # If not an empty line
            try:
                index = line.index('//')
                line = line[:index]
            except:
                pass
            if len(line)>0:
                lines.append(line)
    return lines


def pre_process_firstpass(lines,Symbol_Table):
    '''
    pre_process_firstpass goes over the first pass of the assembly code removing labels
    and adding their lookup in the Symbol_Table
    '''
    preprocessed_lines = []
    counter=0
    for line in lines:
        if '(' in line:  # Label
            line = line.replace('(','')  # Remove Label
            line = line.replace(')','')
            Symbol_Table[line] = str(counter)  # Add lookup
        else:
            preprocessed_lines.append(line)
            counter+=1  # Increment Counter
    return preprocessed_lines

def pre_process_secondpass(lines, Symbol_Table):
    '''
    pre_process_secondpass goes over the second pass of the assembly code replacing variables
    and addresses having labels with the appropriate memory location address.
    '''
    memory = 16
    for i in range(0,len(lines)):
        if lines[i][0] =='@':
            try: 
                int(lines[i][1:])  # Try to convert to integer
            except:  # Exception indicating not an integer
                if lines[i][1:] in Symbol_Table:  #  If present in lookup table
                    lines[i] = '@' + Symbol_Table[lines[i][1:]]
                else:  #  Add to lookup table
                    Symbol_Table[lines[i][1:]] = str(memory)
                    lines[i] = '@' + str(memory)
                    memory+=1
    return lines
                    
            
        

def translate(lines,destination_table,ALU_table,jump_table):
    '''
    translate function takes all the look up tables required and converts the assembly language
    to machine language.
    '''
    machine_language = []
    for line in lines:
        if line[0] =='@': #If Address instruction
            machine_language.append('0' + '{0:b}'.format(int(line[1:])).zfill(15)) #15 bit binary representation of address
        else: # Compute instruction
            a = '0' # Default 'a' bit is 0
            if '=' in line and ';' in line:  # Instructions of the type D=D+1;JGT
                split_expression = re.split(r'[=;]',line)  # Split on '=' and ';'
                dest = destination_table[split_expression[0]]
                if 'M' in split_expression[1]:
                    a='1'  # Make 'a' bit as 1
                    split_expression[1] = split_expression[1].replace('M','A') # Replace M back to A for ALU lookup
                alu = ALU_table[split_expression[1]]
                jump = jump_table[split_expression[2]]
            elif '=' in line: # Instructions of the type D=D+1
                split_expression = line.split('=')  # Split on '='
                dest = destination_table[split_expression[0]]
                if 'M' in split_expression[1]:
                    a='1'  # Make 'a' bit as 1
                    split_expression[1] = split_expression[1].replace('M','A') # Replace M back to A for ALU lookup
                alu = ALU_table[split_expression[1]]
                jump = jump_table[None]
            elif ';' in line:  # Instructions of the type D;JGT 
                split_expression = line.split(';')  # Split on ';'
                dest = destination_table[None]
                if 'M' in split_expression[0]:
                    a='1'  # Make 'a' bit as 1
                    split_expression[0] = split_expression[0].replace('M','A') # Replace M back to A for ALU lookup
                alu = ALU_table[split_expression[0]]
                jump = jump_table[split_expression[1]]
            else:  # Instructions having only ALU output like M, D, etc. 
                dest = destination_table[None]
                if 'M' in line:
                    a='1'  # Make 'a' bit as 1
                    line = line.replace('M','A') # Replace M back to A for ALU lookup
                alu = ALU_table[line]
                jump = jump_table[None]
            value = '111'+a+alu+dest+jump #The final machine code
            machine_language.append(value)
    return machine_language



                
if __name__ =='__main__':
    """
    Main Function of the Program that takes in the input file name as argument and converts 
    it to Machine language.
    """
    x = sys.argv[1] #Input file as argument
    y = 'no_comments'
    lines = Compute(x,y) #Remove white spaces and comments
    destination_table = {None:'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
    jump_table = {None:'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}
    ALU_table = {'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101','!A':'110001','-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110','A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101','A|D':'010101','A&D':'000000','A+D':'000010'}
    Symbol_Table = {'SP':'0','LCL':'1','ARG':'2','THIS':'3','THAT':'4','R0':'0','R1':'1','R2':'2','R3':'3','R4':'4','R5':'5','R6':'6','R7':'7','R8':'8','R9':'9','R10':'10','R11':'11','R12':'12','R13':'13','R14':'14','R15':'15','SCREEN':'16384','KBD':'24576'}
    lines = pre_process_firstpass(lines,Symbol_Table) #Perform first pass
    lines = pre_process_secondpass(lines,Symbol_Table) #Perform second pass
    lines = translate(lines,destination_table,ALU_table,jump_table) # Translate to Machine Code
    res = x.replace('.asm','.hack') #Resulting file to be written
    with open(res,'w') as file:
        for line in lines:
            line = line+'\n'
            file.write(line) 
    print('Completed')    
    

    
    
    
    
    