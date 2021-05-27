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
        print("parseExpression", oplex.output())     #
        if oplex.type == "Operator":
            if oplex.lex in ['+','-']:
                self.curlex = self.lexAnalizer.nextLex()
                print("parseExpression nextlex", self.curlex.output())   
                right = self.parseExpression()
                return Node.BinOpNode(oplex, left, right)
            return left
        return left
        #elif oplex.type == 'Delimiter' or oplex.type == 'Empty':
            #return left
        #raise Exception("Не следует оператор после идентификатора или числа в parseExpression") 

    
    def parseTerm(self):
        left = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        print("parseTerm", oplex.output())     #
        if oplex.type == "Operator":
            if oplex.lex in ['*','/']:
                self.curlex = self.lexAnalizer.nextLex()
                print("parseTerm", self.curlex.output())   
                right = self.parseTerm()
                return Node.BinOpNode(oplex, left, right)
            return left
        return left
        #elif oplex.type == 'Delimiter' or oplex.type == 'Empty':
        #    return left
        #raise Exception("Не следует оператор после идентификатора или числа в parseTerm") 
    
    def parseFactor(self):
        self.curlex = self.lexAnalizer.getLex()
        print("parseFactor", self.curlex.output())     #
        if self.curlex.type == "Identifier":
            print(self.lexAnalizer.nextLex().output())     # убрать принт, оставить "съедание"
            return Node.IdentNode(self.curlex)
        elif self.curlex.type == "Integer" or curlex.type == "Float":
            print(self.lexAnalizer.nextLex().output())     # убрать принт, оставить "съедание"
            return Node.NumberNode(self.curlex)
        elif self.curlex.lex == "(":
            self.curlex = self.lexAnalizer.nextLex()
            print(self.curlex.output())     #
            curNode = self.parseExpression()
            if self.curlex.lex != ")":
                raise Exception("Тут скобочки нету...")
            else:
                self.curlex = self.lexAnalizer.nextLex()
        raise Exception("Почему-то оказался сздесь, а значит, что-то совершенно пошло не так")


