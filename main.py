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
#

### обновления для парсера: 
# Оно родилось и пока что мало что умеет (ничего не умеет)
# Может работать с длинными выражениями, но неправильно: неверный порядок выполнения
# 
# 
#

if __name__ == '__main__':

    # запуск и тестирование парсера:

    testname = "parse_tests\\1.txt"
    parserper = Parse.Parser(testname)
    itog = parserper.parseExpression()
    itog.Print(0)



    #--------------------------------------------------------------------------------------------------#
    
    # запуск и тестирование лексера:

    #for i in range(1,23): #номера файлов, увеличивать при новых тестах
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