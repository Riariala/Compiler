import GetLex
import Node

class Parser():

    def __init__(self, testname):
        self.lexAnalizer = GetLex.GetLex(testname)
        self.curlex = ''
        self.catcherror = False

    def Require(self, name):
        if self.lexAnalizer.getLex().lex not in name:
            waited = "' или '".join(name)
            self.catcherror = True
            return f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.lexAnalizer.getLex().lex} ожидалось "{waited}"'
        self.lexAnalizer.nextLex()
        return

    def RequireType(self, typename):
        if self.lexAnalizer.getLex().type not in typename:
            waited = "' или '".join(typename)
            self.catcherror = True
            return f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.lexAnalizer.getLex().lex} ожидалось "{waited}"'
        return

    def checkNodeType(self, Nodetypes, nodetocheck):
        if type(nodetocheck) in Nodetypes:
            self.catcherror = True
            return f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.lexAnalizer.getLex().lex} ожидалось выражение'
        return

    def parseProgramm(self):
        stmts = []
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex == 'program':
            progW = Node.KeyWordNode(self.curlex)
            self.curlex = self.lexAnalizer.nextLex()
            err = self.RequireType(["Identifier"])
            if err:
                return Node.ErrorNode(err)
            stmts.append(Node.ProgramNameNode(progW, self.curlex))
            err = self.Require([";"])
            if err:
                return Node.ErrorNode(err)
        self.curlex = self.lexAnalizer.getLex()
        while self.curlex.lex in ["function","procedure"]:
            if self.curlex.lex =="function":
                parsed = self.parseFunction()
            elif self.curlex.lex == "procedure":
                parsed = self.parsePocedure()
            stmts.append(parsed)
            self.curlex = self.lexAnalizer.nextLex()
        if self.curlex.lex == 'var':
            varstmts = []
            progW = Node.KeyWordNode(self.curlex)
            self.lexAnalizer.nextLex()
            while self.curlex.lex != 'begin':
                varstmts.append(self.parseVar())
                err = self.Require([";"])
                if err:
                    return Node.ErrorNode(err)
                self.curlex = self.lexAnalizer.getLex()
            stmts.append(Node.ProgVarBlockNode(progW, varstmts))
        if self.curlex.lex == 'begin':
            stmts.append(self.parseStmt())
            err = self.Require(["."])
            if err:
                return Node.ErrorNode(err)
        return (Node.ProgrammNode(stmts))

    def parseFunction(self):
        funcCallW  = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(["function"])
        if err:
            return Node.ErrorNode(err)
        funcname = self.lexAnalizer.getLex()
        err = self.RequireType(["Identifier"])
        if err:
            return Node.ErrorNode(err)
        rbrac = self.lexAnalizer.nextLex()
        self.curlex = self.lexAnalizer.getLex()
        err = self.Require(["("])
        if err:
            return Node.ErrorNode(err)
        args = []
        while self.curlex.lex == ";" or self.curlex.lex == "(":
            if self.curlex.lex == 'var':
                varcallW = Node.KeyWordNode(self.curlex)
                args.append(Node.FuncProcRefArg(varcallW, self.parseVar()))
            else:
                args.append(Node.FuncProcValArg(self.parseVar()))
            self.curlex = self.lexAnalizer.getLex()
        lbrac = self.lexAnalizer.getLex()
        err = self.Require([")"])
        if err:
            return Node.ErrorNode(err)
        dotdot = self.lexAnalizer.getLex()
        err = self.Require([":"])
        if err:
            return Node.ErrorNode(err)
        err = self.RequireType(["Identifier"])
        if err:
            return Node.ErrorNode(err)
        resulttype = self.lexAnalizer.getLex()
        self.lexAnalizer.nextLex()
        err = self.Require([";"])
        if err:
            return Node.ErrorNode(err)
        body = self.parseStmt()
        return Node.FuncNode(funcCallW, funcname, rbrac, lbrac,dotdot,resulttype, body, args)
    
    def parsePocedure(self):
        funcCallW  = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(["procedure"])
        if err:
            return Node.ErrorNode(err)
        funcname = self.lexAnalizer.getLex()
        err = self.RequireType(["Identifier"])
        if err:
            return Node.ErrorNode(err)
        rbrac = self.lexAnalizer.nextLex()
        self.curlex = self.lexAnalizer.getLex()
        err = self.Require(["("])
        if err:
            return Node.ErrorNode(err)
        args = []
        while self.curlex.lex == ";" or self.curlex.lex == "(":
            if self.curlex.lex == 'var':
                varcallW = Node.KeyWordNode(self.curlex)
                args.append(Node.FuncProcRefArg(varcallW, self.parseVar()))
            else:
                args.append(Node.FuncProcValArg(self.parseVar()))
            self.curlex = self.lexAnalizer.getLex()
        lbrac = self.lexAnalizer.getLex()
        err = self.Require([")"])
        err = self.Require([";"])
        if err:
            return Node.ErrorNode(err)
        body = self.parseStmt()
        return Node.ProcedureNode(funcCallW, funcname, rbrac, lbrac, body, args)

    
    def parseVar(self):
        self.curlex = self.lexAnalizer.getLex()
        varnames = []
        if self.curlex.type == 'Delimiter':
            return(Node.NullNode())
        err = self.RequireType(["Identifier"])
        if err:
                return Node.ErrorNode(err)
        varibl = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        varnames.append(varibl)
        while oplex.lex == ",":
            self.curlex = self.lexAnalizer.nextLex()
            err = self.RequireType(["Identifier"])
            if err:
                return Node.ErrorNode(err)
            varibl = self.parseFactor()
            varnames.append(varibl)
            oplex = self.lexAnalizer.getLex()
        oprtn = Node.VarAssignNode(self.lexAnalizer.getLex())
        err = self.Require([":", ":="])
        if err:
                return Node.ErrorNode(err)
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex ==";":
            self.catcherror = true
            return Node.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
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
                err = self.Require([']'])
                if err:
                    return Node.ErrorNode(err)
            ofW = self.lexAnalizer.getLex()
            err = self.Require(['of'])
            if err:
                return Node.ErrorNode(err)
            typel = self.perseInitType()
            return Node.ArrTypeNode(typeLex, typel, Node.KeyWordNode(ofW), diap, rbrc, lbrc)
        else:
            return Node.SingleTypeNode(typeLex)

    def parseDiap(self):
        fromexpr = self.parseExpression()
        delim = self.lexAnalizer.getLex()
        if delim.lex in [',', ']']:
            return fromexpr
        err = self.Require(['..',','])
        if err:
                return Node.ErrorNode(err)
        toexpr = self.parseExpression()
        if type(fromexpr) == Node.NullNode:
            return Node.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
        if type(toexpr) == Node.NullNode:
            return Node.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
        return Node.DiapnNode(delim, fromexpr, toexpr)

    def parseStmt(self):
        if self.catcherror:
            return Node.NullNode() 
        self.curlex = self.lexAnalizer.getLex()
        stmt = ''
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
        elif self.curlex.lex == "break":
            self.lexAnalizer.nextLex()
            stmt = Node.KeyWordNode(self.curlex)
        elif self.curlex.lex == "continue":
            self.lexAnalizer.nextLex()
            stmt = Node.KeyWordNode(self.curlex)
        elif self.curlex.type == "Identifier":
            stmt = self.parseAssigmOrFunc()
        elif self.curlex.lex == "readln": 
            stmt = self.parseReadln()
        elif self.curlex.lex == "writeln":
            stmt = self.parseWriteln()
        elif self.curlex.lex == "end" or self.curlex.lex == ";" :
            return Node.NullNode()
        if stmt:
            return Node.StmtNode(stmt)
        else:
            return Node.NullNode()

    def parseWriteln(self):
        callW = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['writeln'])
        if err:
            return Node.ErrorNode(err)
        oplex = self.lexAnalizer.getLex()
        err = self.Require(['('])
        if err:
            return Node.ErrorNode(err)
        tooutput = []
        while oplex.lex ==',' or oplex.lex =='(':
            tooutput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        err = self.Require([')'])
        if err:
            return Node.ErrorNode(err)
        return Node.WritelnNode(callW, tooutput)


    def parseReadln(self):
        callW = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['readln'])
        if err:
            return Node.ErrorNode(err)
        oplex = self.lexAnalizer.getLex()
        err = self.Require(['('])
        if err:
            return Node.ErrorNode(err)
        toinput = []
        while oplex.lex ==',' or oplex.lex =='(':
            toinput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        err = self.Require([')'])
        if err:
            return Node.ErrorNode(err)
        return Node.ReadlnNode(callW, toinput)
        
    def parseAssigmOrFunc(self):
        left = self.parseFactor()
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex in [";", "end"]:
            return left
        elif self.curlex.lex in  [":=","+=","-=","*=","/="]:
            oper = self.curlex
            self.lexAnalizer.nextLex()
            right = self.parseExpression()
            return Node.AssignNode(oper, right, left)
        else:
            err = self.Require([":=","+=","-=","*=","/="])
            if err:
                return Node.ErrorNode(err)
            

    def parseBlock(self):
        open = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['begin'])
        if err:
                return Node.ErrorNode(err)
        self.curlex = self.lexAnalizer.getLex()
        stmnts = []
        while self.curlex.lex != "end":
            stmnts.append(self.parseStmt())
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex != ";" or self.catcherror:
                break;
            self.lexAnalizer.nextLex()
        close = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['end'])
        if err:
            return Node.ErrorNode(err)
        return Node.BlockNode(stmnts, open, close)
    
    def parseWhile(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['while'])
        if err:
                return Node.ErrorNode(err)
        expression = self.parseExpression()
        doW = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['do'])
        if err:
                return Node.ErrorNode(err)
        body = self.parseStmt()
        return Node.WhileNode(call, expression, body, doW)

    def parseRepeatUntil(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['repeat'])
        if err:
                return Node.ErrorNode(err)
        body = self.parseStmt()
        untilW = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['until'])
        if err:
                return Node.ErrorNode(err)
        expression = self.parseExpression()
        return Node.repeatUntilNode(call, expression, body, untilW)

    def parseFor(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['for'])
        if err:
                return Node.ErrorNode(err)
        condit1 = self.parseStmt()
        toW = Node.KeyWordNode(self.lexAnalizer.getLex())
        err =self.Require(['to', 'downto'])
        if err:
                return Node.ErrorNode(err)
        condit2 = self.parseExpression()
        doW = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['do'])
        if err:
                return Node.ErrorNode(err)
        body = self.parseStmt()
        return Node.ForNode(call, condit1, toW, condit2, doW, body)

    def parseIf(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['if'])
        if err:
                return Node.ErrorNode(err)
        expression = self.parseExpression()
        thenW = Node.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['then'])
        if err:
                return Node.ErrorNode(err)
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
        if self.catcherror:
            return Node.NullNode()
        left = self.parseTerm()
        oplex = self.lexAnalizer.getLex()
        leftpoints = left
        while (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['+','-', 'or','xor']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            err = self.checkNodeType([Node.NullNode], right)
            if err:
                return Node.ErrorNode(err)
            leftpoints = Node.BinOpNode(oplex, [leftpoints], right)
            oplex = self.lexAnalizer.getLex()
        if (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['=','<>', '<','>', '>=', '<=', 'in']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseExpression()
            err = self.checkNodeType([Node.NullNode], right)
            if err:
                return Node.ErrorNode(err)
            return Node.BoolOpNode(oplex, [leftpoints], [right])
        return leftpoints

    def parseTerm(self):
        if self.catcherror:
            return Node.NullNode()
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
                err = self.checkNodeType([Node.NullNode], right)
                if err:
                    return Node.ErrorNode(err)
                leftpoints = [Node.BinOpNode(oplex, leftpoints, right)]
                oplex = self.lexAnalizer.getLex()
            else:
                return leftpoints[0]
        return leftpoints[0]

    def parseFactor(self):
        if self.catcherror:
            return Node.NullNode()
        self.curlex = self.lexAnalizer.getLex()
        oplex = self.lexAnalizer.getLex()
        if oplex.lex.lower() in ['not','+', '-','^', '@']:
            operation = oplex
            self.lexAnalizer.nextLex()
            right = self.parseFactor()
            err = self.checkNodeType([Node.NullNode], right)
            if err:
                return Node.ErrorNode(err)
            return Node.UnarOpNode(operation, right)
        if self.curlex.type == "Identifier" or self.curlex.lex == "readln" or self.curlex.lex == "writeln":
            self.lexAnalizer.nextLex() 
            oplex = self.lexAnalizer.getLex()   
            if oplex.type == "Delimiter" and oplex.lex == "[":
                main = self.curlex
                open = oplex
                self.lexAnalizer.nextLex() 
                mid = self.parseExpression()
                self.curlex = self.lexAnalizer.getLex()
                err = self.Require(["]"])
                if err:
                    return Node.ErrorNode(err)
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
                        err = self.Require([")", ","])
                        if err:
                            return Node.ErrorNode(err)
                return Node.callNode(main, mid, open, self.curlex)
            return Node.IdentNode(self.curlex)
        elif self.curlex.type == "Integer" or self.curlex.type == "Float":  
            self.lexAnalizer.nextLex() 
            return Node.NumberNode(self.curlex)
        elif self.curlex.type == "String":
            self.lexAnalizer.nextLex() 
            return Node.StringConstNode(self.curlex)
        elif self.curlex.lex == "(":
            self.lexAnalizer.nextLex() 
            self.curlex = self.lexAnalizer.getLex()
            curNode = self.parseExpression()
            err = self.checkNodeType([Node.NullNode], curNode)
            if err:
                return Node.ErrorNode(err)
            self.curlex = self.lexAnalizer.getLex()
            err = self.Require([")"])
            if err:
                    return Node.ErrorNode(err)
            return curNode
        return Node.NullNode()