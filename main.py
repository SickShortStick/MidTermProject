class File:

    def __init__(self, name):
        self.name = name
        self.parent = None
        self.contents = []

    def __str__(self):
        result = ''
        for line in self.contents:
            result += line + '\n'
        return result

class Folder:

    def __init__(self, name):
        self.name = name
        self.parent = None
        self.folders = dict()
        self.files = dict()
    

    def __str__(self):
        return self.name

class FileSystem:

    def __init__(self):
        self.root_folder = Folder('root')
        self.current_folder = self.root_folder
        self.current_path = 'root/'

    def ls(self, destination_folder=None):
        if destination_folder == None:
            destination_folder = file_system.current_folder
        for folder in destination_folder.folders:
            print(f'{folder} Folder')
        for file_name, file in destination_folder.files.items():
            print(f'{file_name} File')

    def cd(self, destination_folder, destination_path):
        file_system.current_folder = destination_folder
        file_system.current_path = destination_path


    def mkdir(self, folder_name, parent_folder = None):
        parent_folder = file_system.current_folder if parent_folder == None else parent_folder
        new_folder = Folder(folder_name)
        new_folder.parent = parent_folder
        parent_folder.folders[folder_name] = new_folder

    def touch(self, file_name: str, destination_folder):
        new_file = File(file_name)
        new_file.parent = destination_folder
        destination_folder.files[file_name] = new_file
    
    def rm(self, target_folder: Folder):
        parent_folder : Folder = target_folder.parent
        parent_folder.folders.pop(target_folder.name)
    
    def cat(self, target_file: File):
        print(target_file)

    def nwfiletxt(self, target_file: File):
        print(f'enter lines for {target_file.name}(/end/ means done)')
        line = input()
        target_file.contents.clear()
        while line != '/end/':
            target_file.contents.append(line)
            line = input()

    def appendtxt(self, target_file: File):
        print(f'enter lines for {target_file.name}(/end/ means done)')
        line = input()
        while line != '/end/':
            target_file.contents.append(line)
            line = input()
        
    def mv(self, target_entity, destinaiton_folder: Folder):
        if type(target_entity) == Folder:
            target_entity.parent.folders.pop(target_entity.name)
            destinaiton_folder.folders[target_entity.name] = target_entity
        else:
            target_entity.parent.files.pop(target_entity.name)
            destinaiton_folder.files[target_entity.name] = target_entity
        target_entity.parent = destinaiton_folder

    def rename(self, target_entity, new_name):
        initial_name = target_entity.name
        target_entity.name = new_name
        if type(target_entity) == Folder:
            target_entity.parent.folders.pop(initial_name)
            target_entity.parent.folders[new_name] = target_entity
        else:
            target_entity.parent.files.pop(initial_name)
            target_entity.parent.files[new_name] = target_entity

    def deline(self, target_file: File,line):
        if 0 <= (line - 1) < len(target_file.contents):
            target_file.contents.pop(line - 1)
        else:
            print(f"Line {line} doesnt't exist")

    def cp(self, target_entity, destination_folder):
        if type(target_entity) == Folder:
            coppied_folder = make_copy_of_folders(target_entity)
            destination_folder.folders[coppied_folder.name] = coppied_folder
        else:
            copy_file = File(target_entity.name)
            copy_file.contents = target_entity.contents.copy()
            copy_file.parent = destination_folder
            destination_folder.files[copy_file.name] = copy_file


file_system = FileSystem()

def proccess_input():
    error = False
    print(f'{file_system.current_path}/$', end='')
    line = input()
    splitted_line = list(line.split())
    match splitted_line[0]:
        case 'mkdir':
            if len(splitted_line) == 2:
                folder_name = splitted_line[1]
                file_system.mkdir(folder_name)
            else:
                path, folder_name = map(str, splitted_line[1:])
                splitted_path = list(path.split('/'))
                temp_folder = traverse_linked_list(splitted_path[1:])[0]
                file_system.mkdir(folder_name, temp_folder)
                # temp_folder = file_system.current_folder
                # for folder_name in splitted_path:
                #     if not temp_folder.folders.get(folder_name):
                #         print("Path doesn't exist")
                #         return None
                #     temp_folder = temp_folder.folders[folder_name]
                # temp_folder.mkdir(folder_name)
        case 'ls':
            if len(splitted_line) == 1:
                file_system.ls(file_system.current_folder)
            else:
                destination_folder, destination_path = get_destination_folder_and_path(splitted_line)                
                file_system.ls(destination_folder)
        case 'cd':
            destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
            file_system.cd(destination_folder, destination_path)
        case 'touch':
            file_name = splitted_line[-1]
            splitted_line_slash = list(splitted_line[1].split('/'))
            if len(splitted_line_slash) == 1:
                file_system.touch(file_name, file_system.current_folder)
            else:
                destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
                file_system.touch(file_name, destination_folder)
        case 'rm':
            destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
            file_system.rm(destination_folder)
        case 'nwfiletxt':
            splitted_line_slash = list(splitted_line[1].split('/'))
            file_name = splitted_line_slash[-1]
            if len(splitted_line_slash) == 1:
                destination_folder, destination_path = file_system.current_folder, file_system.current_path
            else:
                length_of_file_name = len(splitted_line_slash[-1])
                splitted_line = ['', splitted_line[1][:len(splitted_line[1]) - length_of_file_name - 1]]
                destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
            if destination_folder.files.get(file_name) == None:
                print("file doesn't exist")
                return None
            file_system.nwfiletxt(destination_folder.files.get(file_name))
        case 'cat':
            splitted_line_slash = list(splitted_line[1].split('/'))
            file_name = splitted_line_slash[-1]
            if len(splitted_line_slash) == 1:
                destination_folder, destination_path = file_system.current_folder, file_system.current_path
            else:
                length_of_file_name = len(splitted_line_slash[-1])
                splitted_line = ['', splitted_line[1][:len(splitted_line[1]) - length_of_file_name - 1]]
                destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
            if destination_folder.files.get(file_name) == None:
                print("file doesn't exist")
                return None
            file_system.cat(destination_folder.files.get(file_name))
        case 'appendtxt':
            splitted_line_slash = list(splitted_line[1].split('/'))
            file_name = splitted_line_slash[-1]
            if len(splitted_line_slash) == 1:
                destination_folder, destination_path = file_system.current_folder, file_system.current_path
            else:
                length_of_file_name = len(splitted_line_slash[-1])
                splitted_line = ['', splitted_line[1][:len(splitted_line[1]) - length_of_file_name - 1]]
                destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
            if destination_folder.files.get(file_name) == None:
                print("file doesn't exist")
                return None
            file_system.appendtxt(destination_folder.files.get(file_name))
        case 'mv':
            source_path = splitted_line[1]
            destination_path = splitted_line[2]
            splitted_line_slash = list(splitted_line[1].split('/'))
            destination_folder, destination_path = get_destination_folder_and_path(destination_path)
            if len(splitted_line_slash) == 1:
                starting_folder, starting_path = file_system.current_folder, file_system.current_path
            else:
                splitted_line = ['', splitted_line[1][:len(splitted_line[1]) - len(splitted_line_slash[-1]) - 1]]
                starting_folder, starting_path = get_destination_folder_and_path(splitted_line)
            file_system.mv(starting_folder.files.get(splitted_line_slash[-1]) if '.txt' in source_path else starting_folder.folders.get(splitted_line_slash[-1]), destination_folder)
        case 'cp':
            source_path = splitted_line[1]
            destination_path = splitted_line[2]
            splitted_line_slash = list(splitted_line[1].split('/'))
            destination_folder, destination_path = get_destination_folder_and_path(destination_path)
            if len(splitted_line_slash) == 1:
                starting_folder, starting_path = file_system.current_folder, file_system.current_path
            else:
                splitted_line = ['', splitted_line[1][:len(splitted_line[1]) - len(splitted_line_slash[-1]) - 1]]
                starting_folder, starting_path = get_destination_folder_and_path(splitted_line)
                file_system.cp(starting_folder.files.get(splitted_line_slash[-1]) if '.txt' in source_path else starting_folder.folders.get(splitted_line_slash[-1]), destination_folder)
        case 'rename':
            splitted_line_slash = list(splitted_line[1].split('/'))
            original_target_name = splitted_line_slash[-1]
            new_name = splitted_line[-1]
            source_path = splitted_line[1]
            if len(splitted_line_slash) == 1:
                destination_folder, destination_path = file_system.current_folder, file_system.current_path
            else:
                length_of_new_name = len(original_target_name)
                splitted_line = ['', splitted_line[1][:len(splitted_line[1]) - length_of_new_name - 1]]
                destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
            if destination_folder.files.get(original_target_name) == None:
                print("file doesn't exist")
                return None
            if destination_folder.folders.get(original_target_name) == None:
                print("folder doesn't exist")
                return None
            file_system.rename(destination_folder.files.get(original_target_name) if '.txt' in original_target_name else destination_folder.folders.get(original_target_name), new_name)
        case 'deline':
            splitted_line_slash = list(splitted_line[1].split('/'))
            line_index = int(splitted_line[-1])
            file_name = splitted_line_slash[-1]
            if len(splitted_line_slash) == 1:
                destination_folder, destination_path = file_system.current_folder, file_system.current_path
            else:
                length_of_file_name = len(splitted_line_slash[-1])
                splitted_line = ['', splitted_line[1][:len(splitted_line[1]) - length_of_file_name - 1]]
                destination_folder, destination_path = get_destination_folder_and_path(splitted_line)
            if destination_folder.files.get(file_name) == None:
                print("file doesn't exist")
                return None
            file_system.deline(destination_folder.files.get(file_name), line_index)


def make_copy_of_folders(parent: Folder):

    new_parent_node = Folder(parent.name)
    for file in parent.files.values():
        new_file = File(file.name)
        new_file.contents = file.contents.copy()
        new_file.parent = new_parent_node
        new_parent_node.files[new_file.name] = new_file

    for folder in parent.folders.values():
        new_child_node = make_copy_of_folders(folder)
        new_child_node.parent = new_parent_node
        new_parent_node.folders[new_child_node.name] = new_child_node

    return new_parent_node

def traverse_linked_list(folders_path_list):
    temp_folder = file_system.current_folder
    initial_path = file_system.current_path
    temp_path = file_system.current_path
    for folder in folders_path_list:
        if folder == '..':
            temp_path = temp_path.removesuffix(f'{temp_folder.name}/')
            if temp_folder.parent == None:
                print("path doesn't exist")
                return None
            temp_folder = temp_folder.parent
        elif temp_folder.folders.get(folder):
            temp_folder = temp_folder.folders.get(folder)
            temp_path += folder + '/'
        else:
            print("path doesn't exist")
            return None
    return [temp_folder, temp_path]

        
def get_destination_folder_and_path(splitted_line):
    path = splitted_line[1]
    splitted_path = list(path.split('/'))
    if '/' in path:
        destination_folder, destination_path = traverse_linked_list(splitted_path[1:])
    else:
        destination_folder, destination_path = traverse_linked_list([path])
    return [destination_folder, destination_path]

while True:
    proccess_input()