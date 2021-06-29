from collections import OrderedDict

import GetLex
import Symbols
import Symbols

class Parser():

    def __init__(self, testname):
        self.lexAnalizer = GetLex.GetLex(testname)
        self.stackTable = []
        self.curlex = ''

    def Require(self, name):
        if self.lexAnalizer.getLex().lex not in name:
            waited = "' или '".join(name)
            raise  Exception(f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось "{waited}"')
        self.lexAnalizer.nextLex()

    def RequireType(self, typename):
        if self.lexAnalizer.getLex().type not in typename:
            waited = "' или '".join(typename)
            raise  Exception(f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось "{waited}"')

    def checkNodeType(self, Nodetypes, nodetocheck):
        if type(nodetocheck) in Nodetypes:
            raise Exception(f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось выражение')

    def parseProgramm(self):
        try:
            stmts = []
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex == 'program':
                progW = Symbols.KeyWordNode(self.curlex)
                self.curlex = self.lexAnalizer.nextLex()
                self.RequireType(["Identifier"])
                stmts.append(Symbols.ProgramNameNode(progW, self.curlex))
                self.Require([";"])
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex == 'var':
                self.stackTable.append(OrderedDict())
                varstmts = []
                progW = Symbols.KeyWordNode(self.curlex)
                self.lexAnalizer.nextLex()
                while self.curlex.lex != 'begin':
                    for i in self.parseVar():
                        varstmts.append(i)
                    self.Require([";"])
                    self.curlex = self.lexAnalizer.getLex()
                stmts.append(Symbols.ProgVarBlockNode(progW, varstmts))
            if self.curlex.lex == 'begin':
                stmts.append(self.parseStmt())
                self.Require(["."])
            return (Symbols.ProgrammNode(stmts))
        except Exception as e:
            return(Symbols.ErrorNode(e))

   
    def parseVar(self):
        self.curlex = self.lexAnalizer.getLex()
        varnames = []
        if self.curlex.type == 'Delimiter':
            return(Symbols.NullNode())
        self.RequireType(["Identifier"])

        if self.curlex.lex not in self.stackTable[-1]:
            self.stackTable[-1][self.curlex.lex] = ''
        else:
            raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Переменная {str(self.curlex.lex)} объявлена повторно')

        #varibl = self.parseFactor()
        oplex = self.lexAnalizer.nextLex()
        varnames.append(self.curlex)
        while oplex.lex == ",":
            self.curlex = self.lexAnalizer.nextLex()
            self.RequireType(["Identifier"])

            if self.curlex.lex not in self.stackTable[-1]:
                self.stackTable[-1][self.curlex.lex] = ''
            else:
                raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Переменная {str(self.curlex.lex)} объявлена повторно')

            varibl = self.parseFactor()
            varnames.append(self.curlex)
            oplex = self.lexAnalizer.getLex()
        oprtn = Symbols.VarAssignNode(self.lexAnalizer.getLex())
        self.Require([":", ":="])
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex ==";":
            raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {str(self.curlex.lex)}, ожидалось выражение')
        if self.curlex.type =="Identifier" and oprtn.name == ':':
            vartype = self.curlex.lex

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

        return varnodeslist
        return Symbols.ProgVarNode(varnames, vartype, exprnode, oprtn)

    def parseStmt(self):
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
        self.Require(['writeln'])
        oplex = self.lexAnalizer.getLex()
        self.Require(['('])
        tooutput = []
        while oplex.lex ==',' or oplex.lex =='(':
            tooutput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        self.Require([')'])
        return Symbols.WritelnNode(callW, tooutput)


    def parseReadln(self):
        callW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['readln'])
        oplex = self.lexAnalizer.getLex()
        self.Require(['('])
        toinput = []
        while oplex.lex ==',' or oplex.lex =='(':
            toinput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        self.Require([')'])
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
                raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Нельзя преобразовать тип {str(right.lexref.typeref.name)} к {str(left.lexref.typeref.name)}')
            return Symbols.AssignNode(oper, right, left)
        else:
            self.Require([":=","+=","-=","*=","/="])
            

    def parseBlock(self):
        open = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['begin'])
        self.curlex = self.lexAnalizer.getLex()
        stmnts = []
        while self.curlex.lex != "end":
            stmnts.append(self.parseStmt())
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex != ";":
                break;
            self.lexAnalizer.nextLex()
        close = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['end'])
        return Symbols.BlockNode(stmnts, open, close)
    
    def parseWhile(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['while'])
        expression = self.parseExpression()
        doW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['do'])
        body = self.parseStmt()
        return Symbols.WhileNode(call, expression, body, doW)

    def parseRepeatUntil(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['repeat'])
        body = self.parseStmt()
        untilW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['until'])
        expression = self.parseExpression()
        return Symbols.repeatUntilNode(call, expression, body, untilW)

    def parseFor(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['for'])
        condit1 = self.parseStmt()
        toW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['to', 'downto'])
        condit2 = self.parseExpression()
        doW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['do'])
        body = self.parseStmt()
        return Symbols.ForNode(call, condit1, toW, condit2, doW, body)

    def parseIf(self):
        call = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['if'])
        expression = self.parseExpression()
        thenW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['then'])
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
        left = self.parseTerm()
        oplex = self.lexAnalizer.getLex()
        leftpoints =[left]
        while (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['+','-', 'or']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            if oplex.lex == "or":
                newtyperef = "boolean"
            elif oplex.lex == '-':
                if right.lexref.typeref.name=="string" or left.lexref.typeref.name=="string":
                    raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Оператор "{oplex.lex}" не применим к типу "String"')
            newtyperef = right.lexref.typeref
            if left.lexref.typeref.name == right.lexref.typeref.name:
                symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
            else:
                raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Нельзя преобразовать тип {str(right.lexref.typeref.name)} к {str(left.lexref.typeref.name)}')
            leftpoints = [Symbols.BinOpNode(symexpr)]
            oplex = self.lexAnalizer.getLex()

        if (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['=','<>', '<','>', '>=', '<=', 'in']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseExpression()
            newtyperef = Symbols.SymType("boolean")
            if left.lexref.typeref.name == right.lexref.typeref.name:
                symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
            else:
                raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Нельзя сравнить переменные типа {str(right.lexref.typeref.name)} и {str(left.lexref.typeref.name)}')
            leftpoints = [Symbols.BinOpNode(symexpr)]
            oplex = self.lexAnalizer.getLex()
            return leftpoints[0]
        return leftpoints[0]
    
    def parseTerm(self):
        left = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        leftpoints = [left]
        while oplex.type == "Operator" or oplex.type == "Key Word":
            if oplex.lex in ['*','/', 'div','mod', 'as', 'is', 'and']:
                self.curlex = self.lexAnalizer.nextLex() 
                right = self.parseFactor()
                if oplex.lex == "and":
                    newtyperef = Symbols.SymType("boolean")
                elif oplex.lex in ["/", 'div','mod']:
                    if right.lexref.typeref.name=="string" or left.lexref.typeref.name=="string":
                        raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Оператор "{oplex.lex}" не применим к типу "String"')
                    if oplex.lex == '/':
                        newtyperef = Symbols.SymType("float")
                else:
                    newtyperef = right.lexref.typeref
                if left.lexref.typeref.name == right.lexref.typeref.name:
                    symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
                else:
                    raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Нельзя преобразовать тип {str(right.lexref.typeref.name)} к {str(left.lexref.typeref.name)}')
                leftpoints = [Symbols.BinOpNode(symexpr)]
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
            self.checkNodeType([Symbols.NullNode], right)
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
            return Symbols.NumberNode(varSym)
        elif self.curlex.type == "Float":  
            varSym = Symbols.SymFlaot(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.NumberNode(varSym)
        elif self.curlex.type == "String":
            varSym = Symbols.SymStr(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.StringConstNode(varSym)


        ######
        elif self.curlex.lex == "(":
            self.lexAnalizer.nextLex() 
            self.curlex = self.lexAnalizer.getLex()
            curNode = self.parseExpression()
            self.checkNodeType([Symbols.NullNode], curNode)
            self.curlex = self.lexAnalizer.getLex()
            self.Require([")"])
            return curNode
        return Symbols.NullNode()
    ############
