import os
import time
import win32api

def list_directory_files(directory):
    file_list = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            author = win32api.GetFileVersionInfo(filepath, '\\StringFileInfo\\040601b0\\Author')
            tags = win32api.GetFileVersionInfo(filepath, '\\StringFileInfo\\040601b0\\Tags')
            title = win32api.GetFileVersionInfo(filepath, '\\StringFileInfo\\040601b0\\Title')
        except:
            author, tags, title = None, None, None
        properties = {
            'Name': filename,
            'Size':os.path.getsize(filepath),
            'Date modified': time.ctime(os.path.getmtime(filepath)),
            'Date created': time.ctime(os.path.getctime(filepath)),
            'File type': 'Directory' if os.path.isdir(filepath) else os.path.splitext(filename)[1],
            'Author': author,
            'Tags': tags,
            'Title': title
        }
        file_list.append(properties)
    return file_list

directory_path = 'Input your Directory'
files_details = list_directory_files(directory_path)
for file_detail in files_details:
    print(file_detail)
