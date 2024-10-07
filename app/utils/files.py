import os
import shutil

from zipfile import ZipFile

DATASETS_FOLDER = os.path.join('app', 'static', 'datasets')
os.makedirs(DATASETS_FOLDER, exist_ok=True)
        
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

def copy_dataset(dataset_path: str, name:str):
    with ZipFile(dataset_path, 'r') as zipf:
        dir_paths = zipf.list_dir()
        if len(dir_paths.keys()) == 2 and dir_paths[''] == []:
            folder = next((key for key in dir_paths.keys() if key != ''), None)
            if folder is None:
                raise Exception('Dataset not founded.')
            files = [f for f in zipf.namelist() if f.startswith(folder + '/')]
            
            new_dataset_path = dataset_path + '_temp'
            with ZipFile(new_dataset_path, 'w') as new_zipf:
                for file in files:
                    file_name = file.replace(folder + '/', '', 1)
                    if file_name:
                        new_zipf.writestr(file_name, zipf.read(file))
            
            try:      
                copy_dataset(new_dataset_path, name)
            finally:
                os.remove(new_dataset_path)
                return
    
    path = os.path.join(DATASETS_FOLDER, name + '.zip')
    shutil.copy(dataset_path, path)
    
def dataset_exist(dataset_name: str) -> bool:
    return dataset_name in os.listdir(DATASETS_FOLDER)