import GetLex
# -*- coding: utf-8 -*-

#Еще надо (напоминалка):
#
#
#

#обновления: 
# нормальная кодировка, русские буквы не превращаются в непонятные символы
# сделаны автоматические тесты
# сделан вывод значения для чисел (преобразование в привычный вид)
# шестнадцатиричное число ($), восьмиричное (&) и двоичное (%)
# новое состояние "P" (отслеживает точку, чтобы было невозомжно объявить вместо 0.2 -> .2, вызвать Class.method все еще возможно)
#

if __name__ == '__main__':
    for i in range(1,23): #номера файлов, увеличивать при новых тестах
        testname = "tests\\"+str(i)+".txt"
        answname = "tests\\code_answ\\"+str(i)+".txt"
        chackname = "tests\\"+str(i)+"(answer).txt"
        print(testname)
        fw = open(answname, 'w', encoding="utf-8")
        lexAnalizer = GetLex.GetLex(testname)
        lexem = lexAnalizer.getLex()
        while lexem:
            fw.write(lexem.output())
            if lexem.error:
                break
            lexem = lexAnalizer.getLex()
            if lexem:
                fw.write( '\n')
        fw.close()
        #Вывод итога теста:
        with open(answname, "r", encoding="utf-8") as thisf, open(chackname, "r", encoding="utf-8") as correct:
            while True:
                ar = thisf.readline()
                cr = correct.readline() 
                if ar != cr:
                    print(False)
                    print("ошбика на символе "+str(cr))
                    print(cr + ar)
                    break
                if ar == "":
                    print(True)
                    break

            