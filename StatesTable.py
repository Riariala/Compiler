class StatesTable(object):

    #States['NI']['.'] - не забыть поставить проверку на точку, чтобы не делать тут двой ной массив!!!!!!!!!!
    # в self.States["ID"]["."] нужно внутри цикла поставить проверку на точку, и если это она, то проверить буфер. Если в буфере зарезервированное слово - то это F, иначе это либо объявление массива, либо ошибка.
    # Создавать постоянную проверку на наличие переменных, существуют или нет. Если не существуют, то лексема ошибочна, и выкинуть к чертям ошибку. 
    #Что делать при минусе? Как быть с веществеными числами? 

    def __init__(self):
        self.States = {"S": {'\n': "D", '\t': "ERR", " ": "S", "A": "ID" , "B": "ID" , "C": "ID" , "D": "ID" , "E": "ID" , "F": "ID" ,"e": "ID" ,"$": "N16" ,"+": "D" ,"*": "D" ,"-": [] ,"/": "D" ,",": "D" ,".": "D" ,":": "D" ,";": "D" ,"(": "NA" ,")": "ERR" ,"[": "NA" ,"]": "ERR" ,"{": "COM" ,"}": "ERR" ,"'": "STR1" ,'"': "STR2" ,"<": "D" ,">": "D" ,"=": "D" ,"_": "ID" },
                       "F": {'\n': "S", '\t': "ERR", " ": "F", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "ERR" ,"$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".":  "ERR" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "ERR" ,"}": "ERR" ,"'": "ERR" ,'"': "STR2" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "ERR" },
                       "ID": {'\n': "S", '\t': "ERR", " ": "S", "A": "ID" , "B": "ID" , "C": "ID" , "D": "ID" , "E": "ID" , "F": "ID" ,"e": "ID" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "S",":": "S" ,";": "S" ,"(": "S" ,")": "F" ,"[": "S" ,"]": "F" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ID" },
                       "NI": {'\n': "S", '\t': "ERR", " ": "S", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "ERR" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "S" ,":": "ERR" ,";": "S" ,"(": "ERR" ,")": "F" ,"[": "ERR" ,"]": "F" ,"{": "COM" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ERR" },
                       "NF": {'\n': "S", '\t': "ERR", " ": "S", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "NF" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": [] ,"/": "S" ,",": "S" ,".": "ERR" ,":": "ERR" ,";": "S" ,"(": "ERR" ,")": "F" ,"[": "ERR" ,"]": "ERR" ,"{": "COM" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ERR" },
                       "N16": {'\n': "S", '\t': "ERR", " ": "S", "A": "N16" , "B": "N16" , "C": "N16" , "D": "N16" , "E": "N16" , "F": "N16" ,"e": "ERR" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "ERR" ,":": "ERR" ,";": "S" ,"(": "ERR" ,")": "F" ,"[": "ERR" ,"]": "ERR" ,"{": "COM" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ERR" },
                       "STR1": {'\n': "S", '\t': "ERR", " ": "STR1", "A": "STR1" , "B": "STR1" , "C": "STR1" , "D": "STR1" , "E": "STR1" , "F": "STR1" ,"e": "STR1" ,"$": "STR1" ,"+": "STR1" ,"*": "STR1" ,"-": "STR1" ,"/": "STR1" ,",": "STR1" ,".": "STR1" ,":": "STR1" ,";": "STR1" ,"(": "STR1" ,")": "STR1" ,"[": "STR1" ,"]": "STR1" ,"{": "STR1" ,"}": "STR1" ,"'": "S" ,'"': "STR1" ,"<": "STR1" ,">": "STR1" ,"=": "STR1" ,"_": "STR1" },
                       "STR2": {'\n': "S", '\t': "ERR", " ": "STR2", "A": "STR2" , "B": "STR2" , "C": "STR2" , "D": "STR2" , "E": "STR2" , "F": "STR2" ,"e": "STR2" ,"$": "STR2" ,"+": "STR2" ,"*": "STR2" ,"-": "STR2" ,"/": "STR2" ,",": "STR2" ,".": "STR2" ,":": "STR2" ,";": "STR2" ,"(": "STR2" ,")": "STR2" ,"[": "STR2" ,"]": "STR2" ,"{": "STR2" ,"}": "STR2" ,"'": "STR2" ,'"': "S" ,"<": "STR2" ,">": "STR2" ,"=": "STR2" ,"_": "STR2" },
                       "COM": {'\n': "S", '\t': "ERR", " ": "COM", "A": "COM" , "B": "COM" , "C": "COM" , "D": "COM" , "E": "COM" , "F": "COM" ,"e": "COM" ,"$": "COM" ,"+": "COM" ,"*": "COM" ,"-": "COM" ,"/": "COM" ,",": "COM" ,".": "COM" ,":": "COM" ,";": "COM" ,"(": "COM" ,")": "COM" ,"[": "COM" ,"]": "COM" ,"{": "COM" ,"}": "S" ,"'": "COM" ,'"': "COM" ,"<": "COM" ,">": "COM" ,"=": "COM" ,"_": "COM" },
                       "D": {'\n': "S", '\t': "ERR", " ": "S", "A": "S" , "B": "S" , "C": "S" , "D": "S" , "E": "S" , "F": "S" ,"e": "S" ,"$": "S" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "S" ,":": "S" ,";": "S" ,"(": "S" ,")": "S" ,"[": "S" ,"]": "S" ,"{": "S" ,"}": "S" ,"'": "S" ,'"': "S" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "S" },
                       "ERR": {'\n': "S", '\t': "ERR", " ": "ERR", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "ERR" ,"$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "ERR" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "ERR" },
                       "NA": "S", #обрабатывается по особому. Создается новый анализатор
                       "COMS": {'\n': "S", "\t": "S"}}  #обрабатывается по особому.
        self.delStates = {"+": {'\n': "ERR", '\t': "ERR",  " ": "S", '$': "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
                          "*": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
                          "-": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
                          "/": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "COMS" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
                          ",": {'\n': "ERR", '\t': "ERR"," ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "S" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
                          ".": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "D" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
                          ":": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
                          ";": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "S" ,",": "ERR" ,".": "D" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
                          "<": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
                          ">": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
                          "=": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
                          "/n": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "D" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "S" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
                          "/t": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "D" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "S" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
                          " ": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "D" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "S" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" }}
        self.FillStates()
   
    def FillStates(self):
        for i in range(65,91):
            if str(chr(i)) not in self.States["S"]:
                self.States["S"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["F"]:
                self.States["F"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["ID"]:
                self.States["ID"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["NI"]:
                self.States["NI"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["NF"]:
                self.States["NF"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["N16"]:
                self.States["N16"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["STR1"]:
                self.States["STR1"][str(chr(i))] = str("STR1")
            if str(chr(i)) not in self.States["STR2"]:
                self.States["STR2"][str(chr(i))] = str("STR2")
            if str(chr(i)) not in self.States["COM"]:
                self.States["COM"][str(chr(i))] = str("COM")
            if str(chr(i)) not in self.States["D"]:
                self.States["D"][str(chr(i))] = str("S")
            if str(chr(i)) not in self.States["ERR"]:
                self.States["ERR"][str(chr(i))] = str("ERR")
            self.delStates["+"][str(chr(i))] = str("S")
            self.delStates["*"][str(chr(i))] = str("S")
            self.delStates["-"][str(chr(i))] = str("S")
            self.delStates["/"][str(chr(i))] = str("S")
            self.delStates[","][str(chr(i))] = str("S")
            self.delStates["."][str(chr(i))] = str("S")
            self.delStates[":"][str(chr(i))] = str("S")
            self.delStates[";"][str(chr(i))] = str("S")
            self.delStates["<"][str(chr(i))] = str("S")
            self.delStates[">"][str(chr(i))] = str("S")
            self.delStates["="][str(chr(i))] = str("S")
            self.delStates["/n"][str(chr(i))] = str("S")
            self.delStates["/t"][str(chr(i))] = str("S")
            self.delStates[" "][str(chr(i))] = str("S")
        for i in range(97,123):
            if str(chr(i)) not in self.States["S"]:
                self.States["S"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["F"]:
                self.States["F"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["ID"]:
                self.States["ID"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["NI"]:
                self.States["NI"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["NF"]:
                self.States["NF"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["N16"]:
                self.States["N16"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["STR1"]:
                self.States["STR1"][str(chr(i))] = str("STR1")
            if str(chr(i)) not in self.States["STR2"]:
                self.States["STR2"][str(chr(i))] = str("STR2")
            if str(chr(i)) not in self.States["COM"]:
                self.States["COM"][str(chr(i))] = str("COM")
            if str(chr(i)) not in self.States["D"]:
                self.States["D"][str(chr(i))] = str("S")
            if str(chr(i)) not in self.States["ERR"]:
                self.States["ERR"][str(chr(i))] = str("ERR")
            self.delStates["+"][str(chr(i))] = str("S")
            self.delStates["*"][str(chr(i))] = str("S")
            self.delStates["-"][str(chr(i))] = str("S")
            self.delStates["/"][str(chr(i))] = str("S")
            self.delStates[","][str(chr(i))] = str("S")
            self.delStates["."][str(chr(i))] = str("S")
            self.delStates[":"][str(chr(i))] = str("S")
            self.delStates[";"][str(chr(i))] = str("S")
            self.delStates["<"][str(chr(i))] = str("S")
            self.delStates[">"][str(chr(i))] = str("S")
            self.delStates["="][str(chr(i))] = str("S")
            self.delStates["/n"][str(chr(i))] = str("S")
            self.delStates["/t"][str(chr(i))] = str("S")
            self.delStates[" "][str(chr(i))] = str("S")
        for i in range(0,10):
            self.States["S"][str(i)] = str("NI")
            self.States["F"][str(i)] = str("ERR")
            self.States["ID"][str(i)] = str("ID")
            self.States["NI"][str(i)] = str("NI")
            self.States["NF"][str(i)] = str("NF")
            self.States["N16"][str(i)] = str("N16")
            self.States["STR1"][str(i)] = str("STR1")
            self.States["STR2"][str(i)] = str("STR2")
            self.States["COM"][str(i)] = str("COM")
            self.States["D"][str(i)] = str("S")
            self.States["ERR"][str(i)] = str("ERR")
            self.delStates["+"][str(i)] = str("S")
            self.delStates["*"][str(i)] = str("S")
            self.delStates["-"][str(i)] = str("NF")
            self.delStates["/"][str(i)] = str("S")
            self.delStates[","][str(i)] = str("S")
            self.delStates["."][str(i)] = str("NF")
            self.delStates[":"][str(i)] = str("S")
            self.delStates[";"][str(i)] = str("ERR")
            self.delStates["<"][str(i)] = str("S")
            self.delStates[">"][str(i)] = str("S")
            self.delStates["="][str(i)] = str("S")
            self.delStates["/n"][str(i)] = str("ERR")
            self.delStates["/t"][str(i)] = str("ERR")
            self.delStates[" "][str(i)] = str("ERR")

            