class FileSystem:

    def __init__(self):
        self.root_folder = Folder('/')
        self.current_folder = self.root_folder
        self.current_path = '/'

    def cd(self, path):
        pass

class File:

    def __init__(self, name):
        self.name = name
        self.contents = ''

class Folder:

    def __init__(self, name):
        self.name = name
        self.prev = None
        self.folders = dict()
        self.files = set()
    
    def ls(self):
        for folder in self.folders:
            print(folder)

    def mkdir(self, folder_name):
        new_folder = Folder(folder_name)
        self.folders[folder_name] = new_folder

    def __str__(self):
        return self.name

file_system = FileSystem()

def proccess_input():
    print(f'{file_system.current_path}/$', end='')
    line = input()
    splitted_line = list(line.split())
    match splitted_line[0]:
        case 'mkdir':
            if len(splitted_line) == 2:
                folder_name = splitted_line[1]
                file_system.current_folder.mkdir(folder_name)
            else:
                path, folder_name = map(str, splitted_line[1:])
                splitted_path = list(path.split('/'))
                temp_folder = file_system.current_folder
                for folder_name in splitted_path:
                    if not temp_folder.folders.get(folder_name):
                        print("Path doesn't exist")
                        return None
                    temp_folder = temp_folder.folders[folder_name]
                temp_folder.mkdir(folder_name)
        case 'ls':
            file_system.current_folder.ls()
        case 'cd':
            path = splitted_line[1]
            splitted_path = list(path.split('/'))
            initial_path = file_system.current_path
            temp_folder = file_system.current_folder
            for folder_name in splitted_path:
                if folder_name == '..':
                        pass
                if not temp_folder.folders.get(folder_name):
                        print("Path doesn't exist")
                        file_system.current_path = initial_path
                        return None
                file_system.current_path += folder_name
                temp_folder = temp_folder.folders[folder_name]
            file_system.current_folder = temp_folder
                


            

while True:
    proccess_input()