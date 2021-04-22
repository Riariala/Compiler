
class FileReader(object):

    def __init__(self, fileName: str):
        self.file = open(fileName, 'r')

    def NextChar(self):
        return str(self.file.read(1))

    def setPrev(self):
        self.file.seek(self.GetPos()-1)

    def GetPos(self):
        return self.file.tell()