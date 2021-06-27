import GetLex
import Node

class Parser():

    def __init__(self, testname):
        #self.testfile = testname
        self.lexAnalizer = GetLex.GetLex(testname)
        self.curlex = ''

    def Require(self, name):
        if self.lexAnalizer.getLex().lex not in name:
            print("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) +
                 ". Встречено '"+self.lexAnalizer.getLex().lex+"', ожидалось '" + " или ".join(name)+ "'" )
            raise Exception("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) + 
                            ". Встречено '"+self.lexAnalizer.getLex().lex+"', ожидалось '" + "' или '".join(name)+ "'" )
        self.lexAnalizer.nextLex()

    def parseStmt(self):
        self.curlex = self.lexAnalizer.getLex()
        #print(self.curlex.lex)
        if self.curlex.lex == "begin":
            stmt = self.parseBlock()
        elif self.curlex.lex == "if":
            stmt = self.parseIf()
        elif self.curlex.lex == "while":
            stmt = self.parseWhile()
        elif self.curlex.type == "Identifier":
            stmt = self.parseAssigmOrFunc()
        elif self.curlex.lex == "readln" or self.curlex.lex == "writeln":
            stmt = self.parseAssigmOrFunc()
        elif self.curlex.lex == "end" or self.curlex.lex == ";" :
            return Node.NullNode()
        return Node.StmtNode(stmt)

    def parseAssigmOrFunc(self):
        left = self.parseFactor()
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex == ";":
            return left
        elif self.curlex.lex == ":=":
            oper = self.curlex
            self.lexAnalizer.nextLex()
            right = self.parseExpression()
            return Node.AssignNode(oper, right, left)

    def parseBlock(self):
        open = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['begin'])
        self.curlex = self.lexAnalizer.getLex()
        stmnts = []
        while self.curlex.lex != "end":
            stmnts.append(self.parseStmt())
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex != ";":
                break;
            self.lexAnalizer.nextLex()
        close = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['end'])
        #self.Require([";","."])
        return Node.BlockNode(stmnts, open, close)
    
    def parseWhile(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['while'])
        expression = self.parseExpression()
        doW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['do'])
        body = self.parseStmt()
        return Node.WhileNode(call, expression, body, doW)

    def parseIf(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['if'])
        expression = self.parseExpression()
        thenW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['then'])
        body = self.parseStmt()
        if self.lexAnalizer.getLex() == 'else':
            elseW = Node.KeyWordNode(self.lexAnalizer.getLex())
            self.lexAnalizer.nextLex()
            elsebody = self.parseStmt()
        else:
            elseW = Node.NullNode()
            elsebody = Node.NullNode()
        return Node.IfNode(call, expression, body, thenW, elsebody, elseW)

    def parseExpression(self):
        left = self.parseTerm()
        oplex = self.lexAnalizer.getLex()
        leftpoints = left
        while (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['+','-', 'or','xor']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            leftpoints = Node.BinOpNode(oplex, [leftpoints], right)
            oplex = self.lexAnalizer.getLex()
            #return leftpoints
        if (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['=','<>', '<','>', '>=', '<=', 'in']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseExpression()
            return Node.BoolOpNode(oplex, [leftpoints], [right])
        return leftpoints

    def parseTerm(self):
        left = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        leftpoints = [left]
        if oplex.type == "Delimiter" and oplex.lex == ".":
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            leftpoints = [Node.RecordNode(oplex, leftpoints, right)]
        while oplex.type == "Operator" or oplex.type == "Key Word":
            if oplex.lex.lower() in ['*','/', 'div','mod', 'as', 'is', 'and']:
                self.curlex = self.lexAnalizer.nextLex() 
                right = self.parseFactor()
                leftpoints = [Node.BinOpNode(oplex, leftpoints, right)]
                oplex = self.lexAnalizer.getLex()
            else:
                return leftpoints[0]
        return leftpoints[0]

    def parseFactor(self):
        self.curlex = self.lexAnalizer.getLex()
        oplex = self.lexAnalizer.getLex()
        if oplex.lex.lower() in ['not','+', '-','^', '@']:
            operation = oplex
            self.lexAnalizer.nextLex()
            right = self.parseFactor()
            return Node.UnarOpNode(operation, right)
        self.lexAnalizer.nextLex() 
        if self.curlex.type == "Identifier" or self.curlex.lex == "readln" or self.curlex.lex == "writeln":
            oplex = self.lexAnalizer.getLex()   
            if oplex.type == "Delimiter" and oplex.lex == "[":
                main = self.curlex
                open = oplex
                self.lexAnalizer.nextLex() 
                mid = self.parseExpression()
                self.curlex = self.lexAnalizer.getLex()
                self.Require(["]"])
                return Node.toMassNode(main, [mid], open, self.curlex)
            if oplex.type == "Delimiter" and oplex.lex == "(":
                main = self.curlex
                open = oplex
                self.curlex = self.lexAnalizer.nextLex() 
                mid = []
                while self.curlex.lex != ")":
                    mid.append(self.parseExpression())
                    self.curlex = self.lexAnalizer.getLex()
                    self.Require([")", ","])
                return Node.callNode(main, mid, open, self.curlex)
            return Node.IdentNode(self.curlex)
        elif self.curlex.type == "Integer" or self.curlex.type == "Float":  
            return Node.NumberNode(self.curlex)
        elif self.curlex.type == "String":
            return Node.StringConstNode(self.curlex)
        elif self.curlex.lex == "(":
            self.curlex = self.lexAnalizer.getLex()
            curNode = self.parseExpression()
            self.curlex = self.lexAnalizer.getLex()
            self.Require([")"])
            return curNode
        print("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) + ". Синтаксическая ошибка." )
        raise Exception("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) + ". Синтаксическая ошибка." )