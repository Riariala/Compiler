import GetLex

if __name__ == '__main__':
    #Lexes.Lexes().Analistic()
    lexAnalizer = GetLex.Lexems()
    lex = ""
    while lex != "EOF":
        lex = lexAnalizer.getLex()
        print(lex)
        