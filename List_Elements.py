import os
import time

def list_directory_files(directory):
    file_list = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        properties = {
            'Name': filename,
            'Size':os.path.getsize(filepath),
            'Date modified': time.ctime(os.path.getmtime(filepath)),
            'Date created': time.ctime(os.path.getctime(filepath)),
            'File type': 'Directory' if os.path.isdir(filepath) else os.path.splitext(filename)[1]
        }
        file_list.append(properties)
    return file_list

directory_path = 'D:\\Proyectos Python'
files_details = list_directory_files(directory_path)
for file_detail in files_details:
    print(file_detail)