
class File:
    def __init__(self, name):
        self.name = name
        self.contents = ''

class Folder:

    def __init__(self, name):
        self.name = name
        self.folders = list()
    
    def __str__(self):
        return self.name

    def ls(self):
        for folder in self.folders:
            print(folder)