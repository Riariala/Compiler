import GetLex

if __name__ == '__main__':
    for i in range(1,11):
        testname = "tests\\"+str(i)+".txt"
        answname = "tests\\code_answ\\"+str(i)+".txt"
        print(testname)
        fw = open(answname, 'w')
        lexAnalizer = GetLex.GetLex(testname)
        lexem = lexAnalizer.getLex()
        while lexem:
            print(lexem.output())
            fw.write(lexem.output() + '\n')
            if lexem.error:
                break
            lexem = lexAnalizer.getLex()