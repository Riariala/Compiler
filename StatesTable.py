class StatesTable(object):

    #States['NI']['.'] - не забыть поставить проверку на точку, чтобы не делать тут двой ной массив!!!!!!!!!!
    # в self.States["ID"]["."] нужно внутри цикла поставить проверку на точку, и если это она, то проверить буфер. Если в буфере зарезервированное слово - то это F, иначе это либо объявление массива, либо ошибка.
    # Создавать постоянную проверку на наличие переменных, существуют или нет. Если не существуют, то лексема ошибочна, и выкинуть к чертям ошибку. 
    #Что делать при минусе? Как быть с веществеными числами? 

    def __init__(self):
        #self.States = {"S": {'\n': "D", '\t': "ERR", " ": "S", "A": "ID" , "B": "ID" , "C": "ID" , "D": "ID" , "E": "ID" , "F": "ID" ,"e": "ID" ,"$": "N16" ,"+": "D" ,"*": "D" ,"-": [] ,"/": "D" ,",": "D" ,".": "D" ,":": "D" ,";": "D" ,"(": "NA" ,")": "ERR" ,"[": "NA" ,"]": "ERR" ,"{": "COM" ,"}": "ERR" ,"'": "STR1" ,'"': "STR2" ,"<": "D" ,">": "D" ,"=": "D" ,"_": "ID" },
        #               "F": {'\n': "S", '\t': "ERR", " ": "F", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "ERR" ,"$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".":  "ERR" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "ERR" ,"}": "ERR" ,"'": "ERR" ,'"': "STR2" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "ERR" },
        #               "ID": {'\n': "S", '\t': "ERR", " ": "S", "A": "ID" , "B": "ID" , "C": "ID" , "D": "ID" , "E": "ID" , "F": "ID" ,"e": "ID" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "S",":": "S" ,";": "S" ,"(": "S" ,")": "F" ,"[": "S" ,"]": "F" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ID" },
        #               "NI": {'\n': "S", '\t': "ERR", " ": "S", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "ERR" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "S" ,":": "ERR" ,";": "S" ,"(": "ERR" ,")": "F" ,"[": "ERR" ,"]": "F" ,"{": "COM" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ERR" },
        #               "NF": {'\n': "S", '\t': "ERR", " ": "S", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "NF" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": [] ,"/": "S" ,",": "S" ,".": "ERR" ,":": "ERR" ,";": "S" ,"(": "ERR" ,")": "F" ,"[": "ERR" ,"]": "ERR" ,"{": "COM" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ERR" },
        #               "N16": {'\n': "S", '\t': "ERR", " ": "S", "A": "N16" , "B": "N16" , "C": "N16" , "D": "N16" , "E": "N16" , "F": "N16" ,"e": "ERR" ,"$": "ERR" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "ERR" ,":": "ERR" ,";": "S" ,"(": "ERR" ,")": "F" ,"[": "ERR" ,"]": "ERR" ,"{": "COM" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "ERR" },
        #               "STR1": {'\n': "S", '\t': "ERR", " ": "STR1", "A": "STR1" , "B": "STR1" , "C": "STR1" , "D": "STR1" , "E": "STR1" , "F": "STR1" ,"e": "STR1" ,"$": "STR1" ,"+": "STR1" ,"*": "STR1" ,"-": "STR1" ,"/": "STR1" ,",": "STR1" ,".": "STR1" ,":": "STR1" ,";": "STR1" ,"(": "STR1" ,")": "STR1" ,"[": "STR1" ,"]": "STR1" ,"{": "STR1" ,"}": "STR1" ,"'": "S" ,'"': "STR1" ,"<": "STR1" ,">": "STR1" ,"=": "STR1" ,"_": "STR1" },
        #               "STR2": {'\n': "S", '\t': "ERR", " ": "STR2", "A": "STR2" , "B": "STR2" , "C": "STR2" , "D": "STR2" , "E": "STR2" , "F": "STR2" ,"e": "STR2" ,"$": "STR2" ,"+": "STR2" ,"*": "STR2" ,"-": "STR2" ,"/": "STR2" ,",": "STR2" ,".": "STR2" ,":": "STR2" ,";": "STR2" ,"(": "STR2" ,")": "STR2" ,"[": "STR2" ,"]": "STR2" ,"{": "STR2" ,"}": "STR2" ,"'": "STR2" ,'"': "S" ,"<": "STR2" ,">": "STR2" ,"=": "STR2" ,"_": "STR2" },
        #               "COM": {'\n': "S", '\t': "ERR", " ": "COM", "A": "COM" , "B": "COM" , "C": "COM" , "D": "COM" , "E": "COM" , "F": "COM" ,"e": "COM" ,"$": "COM" ,"+": "COM" ,"*": "COM" ,"-": "COM" ,"/": "COM" ,",": "COM" ,".": "COM" ,":": "COM" ,";": "COM" ,"(": "COM" ,")": "COM" ,"[": "COM" ,"]": "COM" ,"{": "COM" ,"}": "S" ,"'": "COM" ,'"': "COM" ,"<": "COM" ,">": "COM" ,"=": "COM" ,"_": "COM" },
        #               "D": {'\n': "S", '\t': "ERR", " ": "S", "A": "S" , "B": "S" , "C": "S" , "D": "S" , "E": "S" , "F": "S" ,"e": "S" ,"$": "S" ,"+": "S" ,"*": "S" ,"-": "S" ,"/": "S" ,",": "S" ,".": "S" ,":": "S" ,";": "S" ,"(": "S" ,")": "S" ,"[": "S" ,"]": "S" ,"{": "S" ,"}": "S" ,"'": "S" ,'"': "S" ,"<": "S" ,">": "S" ,"=": "S" ,"_": "S" },
        #               "ERR": {'\n': "S", '\t': "ERR", " ": "ERR", "A": "ERR" , "B": "ERR" , "C": "ERR" , "D": "ERR" , "E": "ERR" , "F": "ERR" ,"e": "ERR" ,"$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "ERR" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "ERR" },
        #               "NA": "S", #обрабатывается по особому. Создается новый анализатор
        #               "COMS": {'\n': "S", "\t": "S"}}  #обрабатывается по особому.
        #self.delStates = {"+": {'\n': "ERR", '\t': "ERR",  " ": "S", '$': "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
        #                  "*": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
        #                  "-": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
        #                  "/": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "COMS" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
        #                  ",": {'\n': "ERR", '\t': "ERR"," ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "S" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
        #                  ".": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "D" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
        #                  ":": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
        #                  ";": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "S" ,",": "ERR" ,".": "D" ,":": "ERR" ,";": "ERR" ,"(": "ERR" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
        #                  "<": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
        #                  ">": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "D" ,"_": "S" },
        #                  "=": {'\n': "ERR", '\t': "ERR", " ": "S", "$": "S" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "ERR" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "ERR" ,"'": "S" ,'"': "S" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
        #                  "/n": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "D" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "S" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
        #                  "/t": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "D" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "S" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" },
        #                  " ": {'\n': "S", '\t': "S", " ": "S", "$": "ERR" ,"+": "ERR" ,"*": "ERR" ,"-": "ERR" ,"/": "D" ,",": "ERR" ,".": "ERR" ,":": "ERR" ,";": "ERR" ,"(": "S" ,")": "ERR" ,"[": "ERR" ,"]": "ERR" ,"{": "S" ,"}": "S" ,"'": "ERR" ,'"': "ERR" ,"<": "ERR" ,">": "ERR" ,"=": "ERR" ,"_": "S" }}
        #self.FillStates()


        #S - Start, F - Finish, ID - Identificator, N = Number, NF = Number Float, D - Delimeter, STR - String, COM - comment, ERR - error
        self.States = {'S': {'_':"ID",'\n': "S", '\t': "S", ' ': "S", '"':"STR","'":"STR", ';': "D", '@': "D", '^': "D", '+': "D" ,'*': "D" ,'-': "D" ,"/": "D", "(": "D" ,")": "D" ,"[": "D" ,"]": "D", ",": "D" ,".": "D", ":": "D", "<": "D" ,">": "D" ,"=": "D", "{": "COM" ,"}": "ERR" },
                       'ID': {'_':"ID",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'N': {'_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "NF", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'D': {'_':"F",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "D" ,'*': "D" ,'-': "D" ,"/": "D", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "D", "<": "D" ,">": "D" ,"=": "D"},
                       'NF': {'_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "D" ,'*': "D" ,'-': "D" ,"/": "D", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "D", "<": "D" ,">": "D" ,"=": "D"}}
        self.FillStates()
   

    def FillStates(self):
        for i in range(65,91):
            if str(chr(i)) not in self.States["S"]:
                self.States["S"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["ID"]:
                self.States["ID"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["N"]:
                self.States["N"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["NF"]:
                self.States["NF"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["D"]:
                self.States["D"][str(chr(i))] = str("F")
        for i in range(97,123):
            if str(chr(i)) not in self.States["S"]:
                self.States["S"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["ID"]:
                self.States["ID"][str(chr(i))] = str("ID")
            if str(chr(i)) not in self.States["N"]:
                self.States["N"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["NF"]:
                self.States["NF"][str(chr(i))] = str("ERR")
            if str(chr(i)) not in self.States["D"]:
                self.States["D"][str(chr(i))] = str("F")
        for i in range(0,10):
            if str(i) not in self.States["S"]:
                self.States["S"][str(i)] = str("N")
            if str(i) not in self.States["ID"]:
                self.States["ID"][str(i)] = str("ID")
            if str(i) not in self.States["N"]:
                self.States["N"][str(i)] = str("N")
            if str(i) not in self.States["NF"]:
                self.States["NF"][str(i)] = str("NF")
            if str(i) not in self.States["D"]:
                self.States["D"][str(i)] = str("F")
        self.States["NF"]['E'] = str("NF")
        self.States["NF"]['e'] = str("NF")

    def getNewState(self, _state: str, _char: str):
        return self.States[_state][_char]


            