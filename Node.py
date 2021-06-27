from abc import ABC, abstractmethod

import Lexem

class Node():
    @abstractmethod
    def Print(self):
        pass

class Expression(Node):
    def Print(self):
        pass

class StmtNode(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def Print(self, fw, space):
        self.stmt.Print(fw, space)

class BlockNode(Node):
    def __init__(self, stmts, open, close):
        self.stmts = stmts
        self.openW = open
        self.closeW = close

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        self.openW.Print( fw, space)
        for i in self.stmts:
            i.Print(fw, space+1)
        self.closeW.Print( fw, space)

class WhileNode(Node):
    def __init__(self, lex, cond, body,doW:Node):
        self.call = lex
        self.condition = cond
        self.body = body
        self.doW = doW

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        self.call.Print( fw, space)
        self.condition.Print(fw, space+1)
        self.doW.Print( fw, space)
        self.body.Print(fw, space+1)

class IfNode(Node):
    def __init__(self, lex:Lexem.Lexem, cond, body,thenW, elsebody, elseW:Node):
        self.call = lex
        self.condition = cond
        self.body = body
        self.thenW = thenW
        self.elseW = elseW
        self.elsebody = elsebody

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        self.call.Print( fw, space)
        self.condition.Print(fw, space+1)
        self.thenW.Print( fw, space)
        self.body.Print(fw, space+1)
        self.elseW.Print( fw, space)
        self.elsebody.Print(fw, space+1)

class KeyWordNode(Node):
     def __init__(self, lex):
         self.lex = lex
         self.name = lex.lex

     def Print(self, fw, space):
         if space != 0:
            writeline = "│"*(space-1) + "├"
         else:
            writeline = ""
         fw.write(writeline + str(self.name)+'\n')


class NodeRanger(Node): #????
    def __init__(self, node):
        self.node = node

    def Print(self, space):
        self.node.Print(space)

class NumberNode(Expression):

    def __init__(self, lex):
        self.lex = lex
        self.value = lex.mean

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + str(self.value)+'\n')

class StringConstNode(Expression):

    def __init__(self, lex):
        self.lex = lex
        self.value = lex.mean

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + str(self.value)+'\n')
    
class IdentNode(Expression):

    def __init__(self, lex):
        self.name = lex.lex
        self.lex = lex

    def Print(self,fw,  space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + self.name+'\n')
        
class BinOpNode(Expression):

    def __init__(self, oplex, left, right):
        self.oplex = oplex
        self.operetion = oplex.lex
        self.left = left
        self.right = right

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + self.operetion+'\n')
        for i in self.left:
            i.Print(fw, space+1)
        self.right.Print(fw, space+1)

class UnarOpNode(Expression):
    def __init__(self, lex, right):
        self.name = lex.lex
        self.lex = lex
        self.right = right

    def Print(self,fw,  space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + str(self.name)+'\n')
        self.right.Print(fw,  space+1)

class RecordNode(Expression):
    def __init__(self, lex, left, right):
        self.operetion = lex.lex
        self.lex = lex
        self.left = left
        self.right = right

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + self.operetion+'\n')
        for i in self.left:
            i.Print(fw, space+1)
        self.right.Print(fw, space+1)

class toMassNode(Expression):
    def __init__(self, lex, middle, opensk, closesk):
        self.mainname = lex.lex
        self.opensk = opensk
        self.closesk = closesk
        self.lex = lex
        self.middle = middle

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + self.mainname+'\n')
        if space != 0:
            writeline = "│"*(space) + "├"
        else:
            writeline = ""
        fw.write(writeline + self.opensk.lex + '\n')
        for i in self.middle:
            i.Print(fw, space+2)
        fw.write(writeline + self.closesk.lex+'\n')

class callNode(Expression):
    def __init__(self, lex, middle, opensk, closesk):
        self.mainname = lex.lex
        self.opensk = opensk
        self.closesk = closesk
        self.lex = lex
        self.middle = middle

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline+ self.mainname + '\n')
        writeline = "│"*(space) + "├"
        fw.write(writeline + self.opensk.lex +'\n')
        for i in self.middle:
            i.Print(fw, space+2)
        fw.write(writeline + self.closesk.lex + '\n')

class NullNode(Node):
    def __init__(self):
        self.name = ""

    def Print(self, fw, space):
        pass


class AssignNode(Node):
    def __init__(self, lex, right, left):
        self.operation = lex.lex
        self.lex = lex
        self.right = right
        self.left = left

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + self.operation + '\n')
        for i in [self.left]:
            i.Print(fw, space+1)
        for i in [self.right]:
            i.Print(fw, space+1)

class BoolOpNode(Node):
    def __init__(self, lex, left, right):
        self.operation = lex.lex
        self.lex = lex
        self.left = left
        self.right = right

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├"
        else:
            writeline = ""
        fw.write(writeline + self.operation + '\n')
        for i in self.left:
            i.Print(fw, space+1)
        for i in self.right:
            i.Print(fw, space+1)