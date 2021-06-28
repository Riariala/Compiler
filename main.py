import GetLex
import Parse
import os, os.path
# -*- coding: utf-8 -*-


if __name__ == '__main__':

    # запуск и тестирование синтаксического анализатора:
    lenth = len([name for name in os.listdir('parser_tests') if os.path.isfile("parser_tests\\"+name)])//2 +1
    #print(lenth)
    for i in range(1,lenth):
        testname = "parser_tests\\"+str(i)+".txt"
        answname = "parser_tests\\code_answ\\"+str(i)+".txt"
        chackname = "parser_tests\\"+str(i)+"(answer).txt"
        print(testname)
        fw = open(answname, 'w', encoding="utf-8")
        parserper = Parse.Parser(testname)
        itog = parserper.parseProgramm()
        itog.Print(fw, 0)
        fw.close()
        #Вывод итога теста:
        with open(answname, "r", encoding="utf-8") as thisf, open(chackname, "r", encoding="utf-8") as correct:
            while True:
                ar = thisf.readline()
                cr = correct.readline()
                if ar != cr:
                    print(False)
                    print("ошбика в выражении "+ str(cr))
                    print(cr + ar)
                    break
                if ar == "":
                    print(True)
                    break

    ##--------------------------------------------------------------------------------------------------#

    ## запуск и тестирование парсера выражений:
    #lenth = len([name for name in os.listdir('parse_tests') if os.path.isfile("parse_tests\\"+name)])//2 +1
    ##print(lenth)
    #for i in range(1,lenth):
    #    testname = "parse_tests\\"+str(i)+".txt"
    #    answname = "parse_tests\\code_answ\\"+str(i)+".txt"
    #    chackname = "parse_tests\\"+str(i)+"(answer).txt"
    #    print(testname)
    #    fw = open(answname, 'w', encoding="utf-8")
    #    parserper = Parse.Parser(testname)
    #    itog = parserper.parseExpression()
    #    itog.Print(fw, 0)
    #    fw.close()
    #    #Вывод итога теста:
    #    with open(answname, "r", encoding="utf-8") as thisf, open(chackname, "r", encoding="utf-8") as correct:
    #        while True:
    #            ar = thisf.readline()
    #            cr = correct.readline() 
    #            if ar != cr:
    #                print(False)
    #                print("ошбика в выражении "+ str(cr))
    #                print(cr + ar)
    #                break
    #            if ar == "":
    #                print(True)
    #                break


    ##--------------------------------------------------------------------------------------------------#
    
    # #запуск и тестирование лексера:
    #lenth = len([name for name in os.listdir('lexer_tests') if os.path.isfile("lexer_tests\\"+name)])//2 +1
    #for i in range(1,lenth): #номера файлов, увеличивать при новых тестах
    #    testname = "lexer_tests\\"+str(i)+".txt"
    #    answname = "lexer_tests\\code_answ\\"+str(i)+".txt"
    #    chackname = "lexer_tests\\"+str(i)+"(answer).txt"
    #    print(testname)
    #    lexAnalizer = GetLex.GetLex(testname)
    #    fw = open(answname, 'w', encoding="utf-8")
    #    lexem = lexAnalizer.getLex()
    #    while lexem.lex:
    #        fw.write(lexem.output())
    #        if lexem.error:
    #            break
    #        lexem = lexAnalizer.nextLex()
    #        if lexem.lex:
    #            fw.write( '\n')
    #    fw.close()
    #    #Вывод итога теста:
    #    with open(answname, "r", encoding="utf-8") as thisf, open(chackname, "r", encoding="utf-8") as correct:
    #        while True:
    #            ar = thisf.readline()
    #            cr = correct.readline() 
    #            if ar != cr:
    #                print(False)
    #                print("ошбика на символе "+str(cr))
    #                print(cr + ar)
    #                break
    #            if ar == "":
    #                print(True)
    #                break