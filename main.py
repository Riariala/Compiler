import GetLex
import Parse
# -*- coding: utf-8 -*-

### Еще надо (напоминалка):
# переписать вывод ошибок везде
#   

### обновления для лексера: 
# исправлена кодировка: русские буквы не превращаются в непонятные символы
# сделаны автоматические тесты
# сделан вывод значения для чисел (преобразование в десятичную систему и вывод без экспоненты)
# шестнадцатиричное число ($), восьмиричное (&) и двоичное (%)
# новое состояние "P" (отслеживает точку, чтобы было невозомжно объявить вместо 0.2 -> .2, вызвать Class.method все еще возможно)
# исправлена ошибка со скобками: если в состоянии D встречался знак "*", он считал это комментарием (больше не считает)

### обновления для парсера: 
# Оно родилось и пока что мало что умеет
# Может работать с длинными выражениями, верный порядок выполнения
# Работает со скобками
# 
#

if __name__ == '__main__':

    # запуск и тестирование парсера:
    for i in range(1,7):
        testname = "parse_tests\\"+str(i)+".txt"
        answname = "parse_tests\\code_answ\\"+str(i)+".txt"
        chackname = "parse_tests\\"+str(i)+"(answer).txt"
        print(testname)
        fw = open(answname, 'w', encoding="utf-8")
        parserper = Parse.Parser(testname)
        itog = parserper.parseExpression()
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


    #--------------------------------------------------------------------------------------------------#
    
    # запуск и тестирование лексера:

    #for i in range(1,25): #номера файлов, увеличивать при новых тестах
    #    testname = "lexer_tests\\"+str(i)+".txt"
    #    answname = "lexer_tests\\code_answ\\"+str(i)+".txt"
    #    chackname = "lexer_tests\\"+str(i)+"(answer).txt"
    #    print(testname)
    #    fw = open(answname, 'w', encoding="utf-8")
    #    lexAnalizer = GetLex.GetLex(testname)
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