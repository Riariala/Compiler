import GetLex
import Parse
import Semantic
import os, os.path
import sys
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    testtype = '4'
    starttest = 1
    try:
        testtype = sys.argv[1]
        starttest = int(sys.argv[2])
    except:
        pass
    if testtype == '1':
        directory = 'lexer_tests'
    elif testtype == '2':
        directory = 'parse_tests'
    elif testtype == '3':
        directory = 'parser_tests'
    elif testtype == '4':
        directory = 'semantic_tests'
    else: raise Exception("Введите 1 для лексического анализатора, 2 для простых выражений, 3 для синтаксического анализатора, 4 для семантического.")

    # запуск и тестирование синтаксического анализатора:
    lenth = len([name for name in os.listdir(directory) if os.path.isfile(directory+"\\"+name)])//2 +1
    if starttest>=lenth or starttest<=0: starttest =1
    for i in range(starttest,lenth):
        testname = directory+"\\"+str(i)+".txt"
        answname = directory+"\\code_answ\\"+str(i)+".txt"
        chackname = directory+"\\"+str(i)+"(answer).txt"
        print(testname)
        fw = open(answname, 'w', encoding="utf-8")
        if testtype == '1':
            lexAnalizer = GetLex.GetLex(testname)
            try:
                lexem = lexAnalizer.getLex()
                while lexem.lex:
                    fw.write(lexem.output() +'\n')
                    lexem = lexAnalizer.nextLex()
            except Exception as e:
                fw.write(str(e))
        elif testtype == '2':
            parserper = Parse.Parser(testname)
            try:
                itog = parserper.parseExpression()
                itog.Print(fw, 0)
            except Exception as e:
                fw.write(str(e))
        elif testtype == '3':
            parserper = Parse.Parser(testname)
            itog = parserper.parseProgramm()
            itog.Print(fw, 0)
        elif testtype == '4':
            parserper = Semantic.Parser(testname)
            itog = parserper.parseProgramm()
            itog.Print(fw, 0)
        fw.close()

        #Вывод итога теста:
        with open(answname, "r", encoding="utf-8") as thisf, open(chackname, "r", encoding="utf-8") as correct:
            while True:
                ar = thisf.readline()
                cr = correct.readline()
                if ar.split() != cr.split():
                    print(False)
                    print("ошбика в выражении "+ str(cr))
                    print(cr + ar)
                    break
                if ar == "":
                    print(True)
                    break

