from abc import ABC, abstractmethod

class Node():
    @abstractmethod
    def Print(self):
        pass

class NodeRanger(Node):
    def __init__(self, node):
        self.node = node

    def Print(self, space):
        self.node.Print(space)

class NumberNode(Node):

    def __init__(self, lex):
        self.lex = lex
        self.value = lex.mean

    def Print(self, fw, space):
        fw.write(" "*space + str(self.value))
    
class IdentNode(Node):

    def __init__(self, lex):
        self.name = lex.lex
        self.lex = lex

    def Print(self,fw,  space):
        fw.write(" "*space + self.name)
        
class BinOpNode(Node):

    def __init__(self, oplex, left, right):
        self.oplex = oplex
        self.operetion = oplex.lex
        self.left = left
        self.right = right

    def Print(self, fw,  space):
        fw.write(" " * space + self.operetion)
        for i in self.left:
            fw.write('\n')
            i.Print(fw, space+1)
        fw.write('\n')
        self.right.Print(fw, space+1)