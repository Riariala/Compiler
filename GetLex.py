import StatesTable
import Lexem

class GetLex(object):
    def __init__(self, testname):
        self.keyWords = ['and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function', 'goto', 'if', 'in', 'label', 'mod', 'nil', 'not', 'of', 'or', 'packed', 'procedure', 'program', 'record', 'repeat', 'set', 'then', 'to', 'type', 'until', 'var', 'while', 'with']
        self.Delimiter = ['.', ';', ',', '(', ')',  '[', ']', ':', '{','}','$', '..']
        self.operators = ['+', '-', '*', '/', '=', '>', '<','<>',':=','>=','<=','+=','-=','/=','*=']
        self.separ = [' ','\n', '\t', '\0', '\r']
        self.state = "S" 
        self.fr = open(testname, 'r')
        self.currChar = ' '
        self.buf = ''
        self.lexStartsFrom = 0
        self.lexStartsFromLine = 0
        self.currIndexChar = 0
        self.currLine = 1
        self.stateTable = StatesTable.StatesTable()

    def getLex(self):
        toReturm = ''
        while True:
            if self.state == "S":
                self.buf = ''
                self.lexStartsFrom = self.currIndexChar
                self.lexStartsFromLine = self.currLine
            if self.state == 'BACK':
                self.state = 'D'
                numbuf = self.buf[:len(self.buf)-2]
                self.buf = self.buf[len(self.buf)-2:] 
                return Lexem.Lexem(numbuf, 'Integer', self.lexStartsFromLine, self.lexStartsFrom, False)
            if self.state == "ERR":
                return Lexem.Lexem(self.buf, toReturm, self.lexStartsFromLine, self.lexStartsFrom, True) 
            prevState = self.state
            self.state = self.stateTable.getNewState(self.state, self.currChar)
            if self.state != "F":
                self.buf += self.currChar
            else:
                break
            self.currChar = str(self.fr.read(1))
            self.currIndexChar +=1
            if self.currChar == '\n':
                self.currIndexChar = 0
                self.currLine += 1

        #Определение типа лексем:
        if prevState == "ENDSTR":
            toReturm = 'String'
        if prevState == "ID": 
            if self.buf in self.keyWords:
                toReturm = 'Key Word'
            else: toReturm = 'Identifier'
        if prevState == "N":
            toReturm = 'Integer'
        if prevState == "NFP" or prevState == "NFPORD" or prevState == "NFPE"or prevState == "NFPEO":
            toReturm = 'Float'
        if prevState == "D":
            if self.buf in self.operators:
                toReturm = 'Operator'
            elif self.buf in self.Delimiter: toReturm = 'Delimiter'
        self.state = "S"
        if self.buf != '':
            return Lexem.Lexem(self.buf, toReturm, self.lexStartsFromLine, self.lexStartsFrom, False)
        else: return ""