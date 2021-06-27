# -*- coding: utf-8 -*-

import StatesTable
import Lexem

class GetLex(object):
    def __init__(self, testname):
        self.keyWords = ['readln', 'writeln','and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function', 'goto', 'if', 'in', 'label', 'mod', 'nil', 'not', 'of', 'or', 'packed', 'procedure', 'program', 'record', 'repeat', 'set', 'then', 'to', 'type', 'until', 'var', 'while', 'with']
        self.Delimiter = ['.', ';', ',', '(', ')',  '[', ']', ':', '{','}','$', '..']
        self.operators = ['+', '-', '*', '/', '=', '>', '<','<>',':=','>=','<=','+=','-=','/=','*=', '^', "@" ]
        self.separ = [' ','\n', '\t', '\0', '\r']
        self.state = "S" 
        self.fr = open(testname, 'r', encoding="utf-8")
        self.currChar = ' '
        self.buf = ''
        self.lexStartsFrom = 0
        self.lexStartsFromLine = 0
        self.currIndexChar = 0
        self.currLine = 1
        self.stateTable = StatesTable.StatesTable()
        self.type = ''

    def nextLex(self):
        toReturm = ''
        while True:
            if self.state == "S":
                self.buf = ''
                self.lexStartsFrom = self.currIndexChar
                self.lexStartsFromLine = self.currLine
            if self.state == 'BACK':
                self.state = 'D'
                numbuf = self.buf[:len(self.buf)-2]
                numstartPos = self.lexStartsFrom
                self.buf = self.buf[len(self.buf)-2:] 
                self.lexStartsFrom = self.currIndexChar - 2     #потому что ушло на 2 вперед, надо вернуться
                return Lexem.Lexem(numbuf, 'Integer', self.lexStartsFromLine, numstartPos, False)
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
            self.type = 'String'
        if prevState == "ID": 
            if self.buf in self.keyWords:
                self.type = 'Key Word'
            else: self.type = 'Identifier'
        if prevState == "N" or prevState == "16" or prevState == "8" or prevState == "2":
            self.type = 'Integer'
        if prevState == "NFP" or prevState == "NFPORD" or prevState == "NFPE"or prevState == "NFPEO":
            self.type = 'Float'
        if prevState == "D" or prevState == "P" or prevState == "BR" or prevState == "SL":
            if self.buf in self.operators:
                self.type = 'Operator'
            elif self.buf in self.Delimiter: self.type = 'Delimiter'
        self.state = "S"
        if self.buf != '':
            return Lexem.Lexem(self.buf, self.type, self.lexStartsFromLine, self.lexStartsFrom, False)
        else: return Lexem.Lexem("", "Empty", self.lexStartsFromLine, self.lexStartsFrom, False)

    def getLex(self):   #без смещения
        if self.buf:
            return Lexem.Lexem(self.buf, self.type, self.lexStartsFromLine, self.lexStartsFrom, False)
        else:
            lex = self.nextLex()
            return lex