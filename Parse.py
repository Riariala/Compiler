import GetLex
import Node

class Parser():

    def __init__(self, testname):
        #self.testfile = testname
        self.lexAnalizer = GetLex.GetLex(testname)
        self.curlex = ''

    def parseExpression(self):
        left = self.parseTerm()
        oplex = self.lexAnalizer.getLex()
        leftpoints = [left]
        while oplex.type == "Operator":
            if oplex.lex in ['+','-']:
                self.curlex = self.lexAnalizer.nextLex()
                right = self.parseTerm()
                leftpoints = [Node.BinOpNode(oplex, leftpoints, right)]
                oplex = self.lexAnalizer.getLex()
                #return Node.BinOpNode(oplex, left, right)
            else:
                return leftpoints[0]
        return leftpoints[0]
        #elif oplex.type == 'Delimiter' or oplex.type == 'Empty':
            #return left
        #raise Exception("Не следует оператор после идентификатора или числа в parseExpression") 

    
    def parseTerm(self):
        left = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        leftpoints = [left]
        while oplex.type == "Operator":
            if oplex.lex in ['*','/']:
                self.curlex = self.lexAnalizer.nextLex() 
                right = self.parseFactor()
                leftpoints = [Node.BinOpNode(oplex, leftpoints, right)]
                oplex = self.lexAnalizer.getLex()
            else:
                return leftpoints[0]
        return leftpoints[0]
        #elif oplex.type == 'Delimiter' or oplex.type == 'Empty':
        #    return leftpoints[0]
        #raise Exception("Не следует оператор после идентификатора или числа в parseTerm") 
    
    def parseFactor(self):
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.type == "Identifier":
            self.lexAnalizer.nextLex().output()    
            return Node.IdentNode(self.curlex)
        elif self.curlex.type == "Integer" or self.curlex.type == "Float":
            self.lexAnalizer.nextLex().output()    
            return Node.NumberNode(self.curlex)
        elif self.curlex.lex == "(":
            self.curlex = self.lexAnalizer.nextLex()
            curNode = self.parseExpression()
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex != ")":
                raise Exception("Тут скобочки нету...")
            else:
                self.curlex = self.lexAnalizer.nextLex()
                return curNode
        #if self.curlex.type == "Empty":
        #    return 
        raise Exception("Почему-то оказался здесь, а значит, что-то совершенно пошло не так")


