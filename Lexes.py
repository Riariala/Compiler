import Lexems
import FileReader
import StatesTable

class Lexes(object):

    def __init__(self):
        self.keyWords = ['and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function', 'goto', 'if', 'in', 'label', 'mod', 'nil', 'not', 'of', 'or', 'packed', 'procedure', 'program', 'record', 'repeat', 'set', 'then', 'to', 'type', 'until', 'var', 'while', 'with']
        self.Delimiter = ['.', ';', ',', '(', ')', '+', '-', '*', '/', '=', '>', '<', '[', ']', ':', '{','}','$']
        self.dobleDelimetr = ['<>',':=','>=','<=','+=','-=','/=','*=','(*','*)', '..']
        self.separ = [' ', '\n', '\t', '\0', '\r']
        self.state = "S" #S - стартовый, N - число, ID - идентификатор, C - комментарий, D - , F - конец, ST - ковычки
        self.allLemems = []
        #self.fw = 'input.txt'
        self.fr = FileReader.FileReader('input.txt')
        self.currChar = ''
        self.buf = ''
        self.lexStartsFrom = 0
        self.stateTable = StatesTable.StatesTable()
        self.PrState = ''

    def Analistic(self):
        #for i in self.stateTable.States["S"].keys():
        #    print(self.stateTable.delStates["*"][i])
        #self.currChar = self.fr.NextChar()
        while self.state != 'F':
            self.currChar = self.fr.NextChar()
            self.state = self.stateTable.States[self.state][self.currChar]
            print(self.currChar)
            print(self.state)

            if self.state == 'S':
                while self.currChar == " ":
                    self.currChar = self.fr.NextChar()
                self.buf = self.buf[:-1]
                print(str(self.lexStartsFrom) + " " + self.buf + "  " + self.PrState)
                self.lexStartsFrom = self.fr.GetPos()
                self.buf = ""
                self.fr.setPrev()
                self.state = self.stateTable.States[self.state][str(self.currChar)]
                #continue
            elif self.state == 'D':
                #prevchar = self.currChar
                self.currChar = self.fr.NextChar()
                nextChar = self.fr.NextChar()
                self.fr.setPrev()
                print(self.fr.GetPos())
                print(str(nextChar))
                print(self.currChar)
                self.state = self.stateTable.delStates[self.currChar][str(nextChar)]
                self.buf += self.currChar
                continue
                #self.fr.setPrev()
            elif self.state == 'ERR':
                print("error")
                break
            elif self.state == 'COMS':
                while self.currChar != "\t":
                    self.currChar = self.fr.NextChar()
                    self.buf += self.currChar
                self.state = "S"
            else:
                self.buf += self.currChar
                self.PrState = self.state
                self.state = self.stateTable.States[self.state][str(self.currChar)]


            #self.state = self.stateTable.States[self.state][self.currChar]

            #self.currChar = self.fr.NextChar()
            #print(self.state)
            #print(self.fr.GetPos())
            
        #fr.NextChar()
        #while self.currChar != '':
        #    print(self.state)
        #    if self.state == 'S':
        #        self.buf =''
        #        self.lexStartsFrom = self.GetPos()
        #        if self.currChar in self.separ:
        #            self.NextChar()
        #            continue
        #        if self.currChar.isalpha():
        #            self.state = 'ID'
        #            self.buf += self.currChar
        #            self.NextChar()
        #            continue
        #        if (self.currChar == "'" or self.currChar == '"'): #разные кавычки сереоз
        #            self.state = 'ST'
        #            self.buf += self.currChar
        #            continue

        #        self.NextChar()

        #        #print(self.currChar)
        #        #self.state = 'N'

        #    elif self.state == 'ID':
        #        if (self.currChar.isalpha() or self.currChar.isdigit() or self.currChar=="_"):
        #            self.buf += self.currChar
        #            self.NextChar()
        #            continue
        #        else:
        #            #if (self.currChar == "." and self.buf == "end"):

        #            if self.buf in self.keyWords:
        #                self.allLemems.append(Lexems.Lexems(self.lexStartsFrom, "зарезервированное слово", self.buf, '-'))
        #            else:
        #                self.allLemems.append(Lexems.Lexems(self.lexStartsFrom, "идентификатор", self.buf, '-'))
        #            self.state = 'S'
        #            continue
        #        continue

        #    elif  self.state == 'ST':
        #        self.NextChar()
        #        self.buf += self.currChar
        #        if (self.currChar == "'" or self.currChar == '"'):
        #            self.allLemems.append(Lexems.Lexems(self.lexStartsFrom, "строка", self.buf, '-'))
        #            self.NextChar()
        #            self.state = 'S'
        #        else:
        #            continue


        #for i in self.allLemems:
        #    print((str)(i.position) + " " + i.type + " " +i.code + " " + i.name)
        #print(StatesTable.StatesTable().States)
        #print(StatesTable.StatesTable().delStates)