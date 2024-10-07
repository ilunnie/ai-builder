from zipfile import ZipFile
        
def list_dir(file: ZipFile) -> dict:
    path = {'': []}
    files = file.namelist()
    for file_path in files:
        parts = file_path.split('/')
        size = len(parts)
        relative_path = path
        
        for index in range(size):
            key = parts[index]
            
            if index < size - 1:
                if key not in relative_path:
                    relative_path[key] = {'': []}
                relative_path = relative_path[key]
            else:
                if key != '':
                    if index == 0:
                        path[''].append(key)
                    else:
                        relative_path[''].append(key)
    return path
            
ZipFile.list_dir = list_dir