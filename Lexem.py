class Lexem(object):

    def __init__(self, _lex, _type, _line, _charn, _er):
        self.lex = _lex
        self.type = _type
        self.line = _line
        self.charn = _charn
        self.error = _er

    def output(self):
        if not self.error:
            return f'{self.line}' +'\t' + f'{self.charn}'+'\t' + f'{self.type}'+'\t' + f'{self.lex}'
        else: 
            return f'{self.line}' +'\t' + f'{self.charn}'+'\t' + 'ошибка в лексеме '+ f'{self.lex}'