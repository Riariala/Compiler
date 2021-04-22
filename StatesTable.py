class StatesTable(object):

    def __init__(self):
        #S - Start, F - Finish, ID - Identifier, N = Number, NF = Number Float, D - Delimiter, STR - String, COM - comment, ERR - error
        self.States = {'S': {b'_':"ID",'\n': "S", '\t': "S", ' ': "S", '"':"STR","'":"STR", ';': "D", '@': "D", '^': "D", '+': "D" ,'*': "D" ,'-': "D" ,"/": "D", "(": "D" ,")": "D" ,"[": "D" ,"]": "D", ",": "D" ,".": "D", ":": "D", "<": "D" ,">": "D" ,"=": "D", "{": "COM" ,"}": "ERR" },
                       'ID': {'_':"ID",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'N': {'_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "NF", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'D': {'_':"F",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "D" ,'*': "D" ,'-': "D" ,"/": "D", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "D", "<": "D" ,">": "D" ,"=": "D"},
                       'NF': {'_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "NF" ,'*': "D" ,'-': "NF" ,"/": "D", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "ERR", ":": "D", "<": "D" ,">": "D" ,"=": "D"}}
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
        self.States["N"]['E'] = str("NF")
        self.States["N"]['e'] = str("NF")


    def getNewState(self, _state: str, _char: str):
        if _state in self.States.keys():
            if _char in self.States[_state].keys():
                return self.States[_state][_char]
        return "ERR"


            