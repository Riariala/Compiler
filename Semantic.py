from collections import OrderedDict

import GetLex
import Symbols
import Symbols

class Parser():

    def __init__(self, testname):
        self.lexAnalizer = GetLex.GetLex(testname)
        self.stackTable = []
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
            progW = Symbols.KeyWordNode(self.curlex)
            self.curlex = self.lexAnalizer.nextLex()
            err = self.RequireType(["Identifier"])
            if err:
                return Symbols.ErrorNode(err)
            stmts.append(Symbols.ProgramNameNode(progW, self.curlex))
            err = self.Require([";"])
            if err:
                return Symbols.ErrorNode(err)
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex == 'var':
            self.stackTable.append(OrderedDict())
            varstmts = []
            progW = Symbols.KeyWordNode(self.curlex)
            self.lexAnalizer.nextLex()
            while self.curlex.lex != 'begin':
                for i in self.parseVar():
                    varstmts.append(i)
                err = self.Require([";"])
                if err:
                    return Symbols.ErrorNode(err)
                self.curlex = self.lexAnalizer.getLex()
            stmts.append(Symbols.ProgVarBlockNode(progW, varstmts))
        if self.curlex.lex == 'begin':
            stmts.append(self.parseStmt())
            err = self.Require(["."])
            if err:
                return Symbols.ErrorNode(err)
        return (Symbols.ProgrammNode(stmts))

   
    def parseVar(self):
        self.curlex = self.lexAnalizer.getLex()
        varnames = []
        if self.curlex.type == 'Delimiter':
            return(Symbols.NullNode())
        err = self.RequireType(["Identifier"])
        if err:
            return Symbols.ErrorNode(err)

        if self.curlex.lex not in self.stackTable[-1]:
            self.stackTable[-1][self.curlex.lex] = ''
        else:
            self.catcherror = true
            return Symbols.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Переменная {self.curlex.lex} объявлена повторно')

        #varibl = self.parseFactor()
        oplex = self.lexAnalizer.nextLex()
        varnames.append(self.curlex)
        while oplex.lex == ",":
            self.curlex = self.lexAnalizer.nextLex()
            err = self.RequireType(["Identifier"])
            if err:
                return Symbols.ErrorNode(err)

            if self.curlex.lex not in self.stackTable[-1]:
                self.stackTable[-1][self.curlex.lex] = ''
            else:
                self.catcherror = true
                return Symbols.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Переменная {self.curlex.lex} объявлена повторно')

            varibl = self.parseFactor()
            varnames.append(self.curlex)
            oplex = self.lexAnalizer.getLex()
        #for i in varnames:
        #    self.stackTable[-1][i.lex] = Symbols.Symtype(i, type_name)
        oprtn = Symbols.VarAssignNode(self.lexAnalizer.getLex())
        err = self.Require([":", ":="])
        if err:
                return Symbols.ErrorNode(err)
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex ==";":
            self.catcherror = true
            return Symbols.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
        if self.curlex.type =="Identifier" and oprtn.name == ':':
            #_type = self.perseInitType()
            vartype = self.curlex.lex
            #varsymbtype = Symbols.SymType()

            oprtn = Symbols.NullNode()
            self.curlex = self.lexAnalizer.nextLex()
            exprnode = Symbols.NullNode()
        elif self.curlex.type =="Identifier" and oprtn.name == ':=':
            exprnode = self.parseExpression()
            vartype = exprnode.symbref.type_name
        varnodeslist = []
        for i in varnames:
            self.stackTable[-1][i.lex] = Symbols.SymType(vartype)
            varnodeslist.append(Symbols.ProgVarNode(i, self.stackTable[-1][i.lex], exprnode, oprtn))

        #if oprtn.name == ':=':
        #    exprnode = self.parseExpression()
        #    return Symbols.ProgVarNode(varnames, _type, exprnode, oprtn)
        #oplex = self.lexAnalizer.getLex()
        #if oplex.lex == "=" or oplex.lex == ":=":
        #    oprtn = Symbols.VarAssignNode(oplex)
        #    self.lexAnalizer.nextLex()
        #    exprnode = self.parseExpression()
        #else:
        #    oprtn = Symbols.NullNode()
        #    exprnode = Symbols.NullNode()
        return varnodeslist
        return Symbols.ProgVarNode(varnames, vartype, exprnode, oprtn)

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
                    return Symbols.ErrorNode(err)
            ofW = self.lexAnalizer.getLex()
            err = self.Require(['of'])
            if err:
                return Symbols.ErrorNode(err)
            typel = self.perseInitType()
            return Symbols.ArrTypeNode(typeLex, typel, Symbols.KeyWordNode(ofW), diap, rbrc, lbrc)
        else:
            return Symbols.SingleTypeNode(typeLex)

    def parseDiap(self):
        fromexpr = self.parseExpression()
        delim = self.lexAnalizer.getLex()
        if delim.lex in [',', ']']:
            return fromexpr
        err = self.Require(['..',','])
        if err:
                return Symbols.ErrorNode(err)
        toexpr = self.parseExpression()
        if type(fromexpr) == Symbols.NullNode:
            return Symbols.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
        if type(toexpr) == Symbols.NullNode:
            return Symbols.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
        return Symbols.DiapnNode(delim, fromexpr, toexpr)

    def parseStmt(self):
        if self.catcherror:
            return Symbols.NullNode() 
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
            varW = Symbols.KeyWordNode(self.curlex)
            stmt = Symbols.ProgVarBlockNode(varW, [self.parseVar()])
        elif self.curlex.lex == "for":
            stmt = self.parseFor()
        elif self.curlex.lex == "break":
            self.lexAnalizer.nextLex()
            stmt = Symbols.KeyWordNode(self.curlex)
        elif self.curlex.lex == "continue":
            self.lexAnalizer.nextLex()
            stmt = Symbols.KeyWordNode(self.curlex)
        elif self.curlex.type == "Identifier":
            stmt = self.parseAssigmOrFunc()
        elif self.curlex.lex == "readln": 
            stmt = self.parseReadln()
        elif self.curlex.lex == "writeln":
            stmt = self.parseWriteln()
        elif self.curlex.lex == "end" or self.curlex.lex == ";" :
            return Symbols.NullNode()
        if stmt:
            return Symbols.StmtNode(stmt)
        else:
            return Symbols.NullNode()

    def parseWriteln(self):
        callW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['writeln'])
        if err:
            return Symbols.ErrorNode(err)
        oplex = self.lexAnalizer.getLex()
        err = self.Require(['('])
        if err:
            return Symbols.ErrorNode(err)
        tooutput = []
        while oplex.lex ==',' or oplex.lex =='(':
            tooutput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        err = self.Require([')'])
        if err:
            return Symbols.ErrorNode(err)
        return Symbols.WritelnNode(callW, tooutput)


    def parseReadln(self):
        callW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['readln'])
        if err:
            return Symbols.ErrorNode(err)
        oplex = self.lexAnalizer.getLex()
        err = self.Require(['('])
        if err:
            return Symbols.ErrorNode(err)
        toinput = []
        while oplex.lex ==',' or oplex.lex =='(':
            toinput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        err = self.Require([')'])
        if err:
            return Symbols.ErrorNode(err)
        return Symbols.ReadlnNode(callW, toinput)
        
    def parseAssigmOrFunc(self):
        left = self.parseFactor() #Node
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex in [";", "end"]:
            return left
        elif self.curlex.lex in  [":=","+=","-=","*=","/="]:
            oper = self.curlex
            self.lexAnalizer.nextLex()
            right = self.parseExpression()
            if left.lexref.typeref.name != right.lexref.typeref.name:
                return Symbols.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Нельзя преобразовать тип {right.lexref.typeref.name} к {left.lexref.typeref.name}')
            return Symbols.AssignNode(oper, right, left)
        else:
            err = self.Require([":=","+=","-=","*=","/="])
            if err:
                return Symbols.ErrorNode(err)
            

    def parseBlock(self):
        open = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['begin'])
        if err:
                return Symbols.ErrorNode(err)
        self.curlex = self.lexAnalizer.getLex()
        stmnts = []
        while self.curlex.lex != "end":
            stmnts.append(self.parseStmt())
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex != ";" or self.catcherror:
                break;
            self.lexAnalizer.nextLex()
        close = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['end'])
        if err:
            return Symbols.ErrorNode(err)
        return Symbols.BlockNode(stmnts, open, close)
    
    def parseWhile(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['while'])
        if err:
                return Symbols.ErrorNode(err)
        expression = self.parseExpression()
        doW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['do'])
        if err:
                return Symbols.ErrorNode(err)
        body = self.parseStmt()
        return Symbols.WhileNode(call, expression, body, doW)

    def parseRepeatUntil(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['repeat'])
        if err:
                return Symbols.ErrorNode(err)
        body = self.parseStmt()
        untilW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['until'])
        if err:
                return Symbols.ErrorNode(err)
        expression = self.parseExpression()
        return Symbols.repeatUntilNode(call, expression, body, untilW)

    def parseFor(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['for'])
        if err:
                return Symbols.ErrorNode(err)
        condit1 = self.parseStmt()
        toW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err =self.Require(['to', 'downto'])
        if err:
                return Symbols.ErrorNode(err)
        condit2 = self.parseExpression()
        doW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['do'])
        if err:
                return Symbols.ErrorNode(err)
        body = self.parseStmt()
        return Symbols.ForNode(call, condit1, toW, condit2, doW, body)

    def parseIf(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['if'])
        if err:
                return Symbols.ErrorNode(err)
        expression = self.parseExpression()
        thenW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        err = self.Require(['then'])
        if err:
                return Symbols.ErrorNode(err)
        body = self.parseStmt()
        if self.lexAnalizer.getLex() == 'else':
            elseW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
            self.lexAnalizer.nextLex()
            elsebody = self.parseStmt()
        else:
            elseW = Symbols.NullNode()
            elsebody = Symbols.NullNode()
        return Symbols.IfNode(call, expression, body, thenW, elsebody, elseW)

    def parseExpression(self):
        if self.catcherror:
            return Symbols.NullNode()
        left = self.parseTerm()
        oplex = self.lexAnalizer.getLex()
        leftpoints = left
        while (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['+','-', 'or','xor']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            err = self.checkNodeType([Symbols.NullNode], right)
            if err:
                return Symbols.ErrorNode(err)
            leftpoints = Symbols.BinOpNode(oplex, [leftpoints], right)
            oplex = self.lexAnalizer.getLex()
        if (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['=','<>', '<','>', '>=', '<=', 'in']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseExpression()
            err = self.checkNodeType([Symbols.NullNode], right)
            if err:
                return Symbols.ErrorNode(err)
            return Symbols.BoolOpNode(oplex, [leftpoints], [right])
        return leftpoints

    def parseTerm(self):
        if self.catcherror:
            return Symbols.NullNode()
        left = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        leftpoints = [left]
        if oplex.type == "Delimiter" and oplex.lex == ".":
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            leftpoints = [Symbols.RecordNode(oplex, leftpoints, right)]
        while oplex.type == "Operator" or oplex.type == "Key Word":
            if oplex.lex.lower() in ['*','/', 'div','mod', 'as', 'is', 'and']:
                self.curlex = self.lexAnalizer.nextLex() 
                right = self.parseFactor()
                err = self.checkNodeType([Symbols.NullNode], right)
                if err:
                    return Symbols.ErrorNode(err)
                leftpoints = [Symbols.BinOpNode(oplex, leftpoints, right)]
                oplex = self.lexAnalizer.getLex()
            else:
                return leftpoints[0]
        return leftpoints[0]

    def parseFactor(self):
        if self.catcherror:
            return Symbols.NullNode()
        self.curlex = self.lexAnalizer.getLex()
        oplex = self.lexAnalizer.getLex()

        if oplex.lex.lower() in ['not','+', '-','^', '@']:
            operation = oplex
            self.lexAnalizer.nextLex()
            right = self.parseFactor()

            err = self.checkNodeType([Symbols.NullNode], right)
            if err:
                return Symbols.ErrorNode(err)
            symexpr = Symbols.SymExpr(operation, Symbols.NullNode(), right, right.lexref.typeref)
            return Symbols.UnarOpNode(symexpr)


        if self.curlex.type == "Identifier":
            ident = self.curlex
            if ident.lex in self.stackTable[-1]:
                self.lexAnalizer.nextLex() 
                oplex = self.lexAnalizer.getLex()   
                symb_var = Symbols.SymVar(ident, self.stackTable[-1][ident.lex])
                return Symbols.IdentNode(symb_var)
            else:
                return Symbols.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Переменная {self.curlex.lex} не была объявлена')
        elif self.curlex.type == "Integer":
            varSym = Symbols.SymInt(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.NumberNode( varSym)
        elif self.curlex.type == "Float":  
            varSym = Symbols.SymFlaot(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.NumberNode(varSym)
        elif self.curlex.type == "String":
            varSym = Symbols.SymStr(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.StringConstNode(varSym)


        elif self.curlex.lex == "(":
            self.lexAnalizer.nextLex() 
            self.curlex = self.lexAnalizer.getLex()
            curNode = self.parseExpression()
            err = self.checkNodeType([Symbols.NullNode], curNode)
            if err:
                return Symbols.ErrorNode(err)
            self.curlex = self.lexAnalizer.getLex()
            err = self.Require([")"])
            if err:
                    return Symbols.ErrorNode(err)
            return curNode
        return Symbols.NullNode()
