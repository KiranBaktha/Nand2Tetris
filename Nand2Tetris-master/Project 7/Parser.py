class parser:
    '''
    parser class goes throught the VM code and removes tabs, new line characters and comments. It also trims the corner spaces.
    It checks if any VM commands are presents and if present, returns to the main program.
    '''
    def __init__(self,filename):
        with open(filename,'r') as file:
            self.data = file.readlines()
    def RemoveCommentsAndSpace(self):
        '''
        Function that removes comments and spaces. 
        '''
        for i in range(len(self.data)):
            self.data[i] = self.data[i].replace('\t','') # Remove Tabs
            self.data[i] = self.data[i].replace('\n','')  # Remove new line characters
        self.lines=[]
        for line in self.data:
            if line!='\n': # If not an empty line
                try:
                    index = line.index('//')
                    line = line[:index]
                except:
                    pass
                if len(line)>0:
                    self.lines.append(line.strip())
    def HasAnyMoreCommands(self):
        '''
        Function that returns a boolean indicating if any more VM commands are present.
        '''
        if len(self.lines)>0:
            return True
        else:
            return False
    def advance(self):
        '''
        Function that returns the next VM command to be translated.
        '''
        return self.lines.pop(0)