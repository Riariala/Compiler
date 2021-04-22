import FileReader
import StatesTable

class Lexems(object):
    def __init__(self):
        self.keyWords = ['and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function', 'goto', 'if', 'in', 'label', 'mod', 'nil', 'not', 'of', 'or', 'packed', 'procedure', 'program', 'record', 'repeat', 'set', 'then', 'to', 'type', 'until', 'var', 'while', 'with']
        self.Delimiter = ['.', ';', ',', '(', ')',  '[', ']', ':', '{','}','$']
        #self.dobleDelimetr = ['<>',':=','>=','<=','+=','-=','/=','*=','(*','*)', '..']
        self.operators = ['+', '-', '*', '/', '=', '>', '<','<>',':=','>=','<=','+=','-=','/=','*=']
        self.separ = [' ','\n', '\t', '\0', '\r']
        self.state = "S" 
        self.fr = FileReader.FileReader('input.txt')
        self.fw = open('output.txt', 'w')
        self.currChar = ' '
        self.buf = ''
        self.lexStartsFrom = 0
        self.stateTable = StatesTable.StatesTable()
        self.EOF = False

    def getLex(self):
        if self.EOF:
            return "EOF"
        self.lexStartsFrom = self.fr.GetPos()
        prevState = self.state
        toReturm = ''
        while self.state != "F" and not self.EOF:
            self.currChar = self.fr.NextChar()
            if self.state == "S":
                self.buf = ''
            if self.state == "D":
                if self.currChar == '/':
                    if self.buf == '//':
                        self.state = "COM"
            if self.state == "COM":
                prevState = self.state
                if self.buf == '//':
                    stopList = ['\n', '\t', '\0', '\r']
                elif self.buf == '{':
                    stopList = ['}']
                else:
                    print("Ошибка с комментариями")
                    break
                self.buf += self.currChar
                self.currChar = self.fr.NextChar()
                self.buf += self.currChar
                while (not self.currChar in stopList) and self.currChar != "":
                    self.currChar = self.fr.NextChar()
                    if self.currChar not in ['\n', '\t', '\0', '\r']:
                        self.buf += self.currChar
                if  self.currChar == "":
                    self.EOF = True
                toReturm = "Comment"
                break
            if self.state == "STR":
                stopList = self.buf
                self.buf += self.currChar
                while self.currChar != stopList and self.currChar != "":
                    self.currChar = self.fr.NextChar()
                    self.buf += self.currChar
                if  self.currChar == "":
                    self.state = "ERR"
                else:
                    toReturm = "String"
                break
            if self.state == "NF":
                if self.currChar =='+' or self.currChar == '-':
                    if self.buf[-1] !='E' and self.buf[-1] !='e':
                        self.state = "F"
                if self.currChar =='E' or self.currChar =='e':
                    if self.buf.find(self.currChar) != -1 or self.buf[-1] =='.':
                        self.state = "ERR"
            if self.state == "ERR":
                self.fw.write("Ошибка в лексеме на символе  " + str(self.lexStartsFrom) +'\r')
                #print("Ошибка в лексеме на символе  ", self.lexStartsFrom)
                return "EOF" 
            prevState = self.state
            if self.currChar != "":
                self.state = self.stateTable.getNewState(self.state,self.currChar)
            else:
                self.EOF = True
                break
            if self.state != "F":
                self.buf += self.currChar
        #Для вывода:
        if prevState == "ID": 
            if self.buf in self.keyWords:
                toReturm = 'Key Word'
            else: toReturm = 'Identifier'
            self.fr.setPrev()
        if prevState == "N":
            toReturm = 'Number'
            self.fr.setPrev()
        if prevState == "NF":
            toReturm = 'Float Number'
            self.fr.setPrev()
        if prevState == "D":
            if self.buf in self.operators:
                toReturm = 'Operator'
            else: toReturm = 'Delimiter'
            self.fr.setPrev()
        self.state = "S"
        if self.buf != '':
            toReturm = str(self.buf) + ' ' + str(self.lexStartsFrom) + ' ' + toReturm
        self.fw.write(toReturm + '\r')
        return toReturm
