import GetLex
import Node

class Parser():

    def __init__(self, testname):
        self.lexAnalizer = GetLex.GetLex(testname)
        self.curlex = ''

    def Require(self, name):
        if self.lexAnalizer.getLex().lex not in name:
            print("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) +
                 ". Встречено '"+self.lexAnalizer.getLex().lex+"', ожидалось '" + " или ".join(name)+ "'" )
            raise Exception("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) + 
                            ". Встречено '"+self.lexAnalizer.getLex().lex+"', ожидалось '" + "' или '".join(name)+ "'" )
        self.lexAnalizer.nextLex()

    def RequireType(self, typename):
        if self.lexAnalizer.getLex().type not in typename:
            print("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) +
                 ". Встречено '"+self.lexAnalizer.getLex().lex+"', ожидалось '" + " или ".join(typename)+ "'" )
            raise Exception("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) + 
                            ". Встречено '"+self.lexAnalizer.getLex().lex+"', ожидалось '" + "' или '".join(typename)+ "'" )

    def parseProgramm(self):
        stmts = []
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex == 'program':
            progW = Node.KeyWordNode(self.curlex)
            self.curlex = self.lexAnalizer.nextLex()
            self.RequireType(["Identifier"])
            stmts.append(Node.ProgramNameNode(progW, self.curlex))
            self.Require([";"])
        if self.curlex.lex == 'var':
            varstmts = []
            progW = Node.KeyWordNode(self.curlex)
            self.lexAnalizer.nextLex()
            while self.curlex.lex != 'begin':
                varstmts.append(self.parseVar())
                self.Require([";"])
                self.curlex = self.lexAnalizer.getLex()
            stmts.append(Node.ProgVarBlockNode(progW, varstmts))
        if self.curlex.lex == 'begin':
            stmts.append(self.parseStmt())
            self.Require(["."])
        return (Node.ProgrammNode(stmts))

    def parseVar(self):
        self.curlex = self.lexAnalizer.getLex()
        varnames = []
        self.RequireType(["Identifier"])
        varibl = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        varnames.append(varibl)
        while oplex.lex == ",":
            self.curlex = self.lexAnalizer.nextLex()
            self.RequireType(["Identifier"])
            varibl = self.parseFactor()
            varnames.append(varibl)
            oplex = self.lexAnalizer.getLex()
        oprtn = Node.VarAssignNode(self.lexAnalizer.getLex())
        self.Require([":", ":="])
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex ==";":
            raise Exception("Строка " + str(self.lexAnalizer.currLine) +", символ " + str(self.lexAnalizer.lexStartsFrom) + 
                            ". Встречено '"+self.curlex.lex+"', ожидалось выражение" )
        if (self.curlex.type =="Identifier" or self.curlex.lex == "array") and oprtn.name == ':':
            _type = self.perseInitType()
            oprtn = Node.NullNode()
            self.curlex = self.lexAnalizer.nextLex()
        else:
            _type = Node.NullNode()
        if oprtn.name == ':=':
            exprnode = self.parseExpression()
            return Node.ProgVarNode(varnames, _type, exprnode, oprtn)
        oplex = self.lexAnalizer.getLex()
        if oplex.lex == "=" or oplex.lex == ":=":
            oprtn = Node.VarAssignNode(oplex)
            self.lexAnalizer.nextLex()
            exprnode = self.parseExpression()
        else:
            oprtn = Node.NullNode()
            exprnode = Node.NullNode()
        return Node.ProgVarNode(varnames, _type, exprnode, oprtn)

    def perseInitType(self):
        typeLex = self.lexAnalizer.getLex()
        if typeLex.lex == "array":
            oplex = self.lexAnalizer.nextLex()
            if oplex.lex == '[':
                rbrc = oplex
                diap = []
                while oplex.lex in [",", "["]:
                    self.lexAnalizer.nextLex()
                    diap.append(self.parseDiap())
                    oplex = self.lexAnalizer.getLex()
                lbrc = self.lexAnalizer.getLex()
                self.Require([']'])
            ofW = self.lexAnalizer.getLex()
            self.Require(['of'])
            typel = self.perseInitType()
            return Node.ArrTypeNode(typeLex, typel, Node.KeyWordNode(ofW), diap, rbrc, lbrc)
        else:
            return Node.SingleTypeNode(typeLex)

    def parseDiap(self):
        fromexpr = self.parseExpression()
        delim = self.lexAnalizer.getLex()
        self.Require(['..',','])
        toexpr = self.parseExpression()
        return Node.DiapnNode(delim, fromexpr, toexpr)

    def parseStmt(self):
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex == "begin":
            stmt = self.parseBlock()
        elif self.curlex.lex == "if":
            stmt = self.parseIf()
        elif self.curlex.lex == "while":
            stmt = self.parseWhile()
        elif self.curlex.lex == "repeat":
            stmt = self.parseRepeatUntil()
        elif self.curlex.lex == "var":
            self.lexAnalizer.nextLex()
            varW = Node.KeyWordNode(self.curlex)
            stmt = Node.ProgVarBlockNode(varW, [self.parseVar()])
        elif self.curlex.lex == "for":
            stmt = self.parseFor()
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
        elif self.curlex.lex in  [":=","+=","-=","*=","/="]:
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
        return Node.BlockNode(stmnts, open, close)
    
    def parseWhile(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['while'])
        expression = self.parseExpression()
        doW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['do'])
        body = self.parseStmt()
        return Node.WhileNode(call, expression, body, doW)

    def parseRepeatUntil(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['repeat'])
        body = self.parseStmt()
        untilW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['until'])
        expression = self.parseExpression()
        return Node.repeatUntilNode(call, expression, body, untilW)

    def parseFor(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['for'])
        condit1 = self.parseStmt()
        toW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['to'])
        condit2 = self.parseExpression()
        doW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['do'])
        body = self.parseStmt()
        return Node.ForNode(call, condit1, toW, condit2, doW, body)

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
                if self.lexAnalizer.getLex().lex == ')':
                    self.curlex = self.lexAnalizer.nextLex() 
                else:
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
        return Node.NullNode()