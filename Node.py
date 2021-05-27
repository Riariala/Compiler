from abc import ABC, abstractmethod

class Node():
    @abstractmethod
    def Print(self):
        pass

class NumberNode(Node):

    def __init__(self, lex):
        self.lex = lex
        self.value = lex.mean

    def Print(self, space):
        print(" "*space,self.value)
    
class IdentNode(Node):

    def __init__(self, lex):
        self.name = lex.lex
        self.lex = lex

    def Print(self, space):
        print(" "*space,self.name)
        
class BinOpNode(Node):

    def __init__(self, oplex, left, right):
        self.oplex = oplex
        self.operetion = oplex.lex
        self.left = left
        self.right = right

    def Print(self, space):
        print(" " * space, self.operetion)
        self.left.Print(space+1)
        self.right.Print(space+1)