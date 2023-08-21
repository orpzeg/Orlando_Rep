import os
import time
import win32api

class DirectoryScanner:
    def __init__(self, directory):
        self.directory = directory

    def getFiles(self):
        file_list = []
        for filename in os.listdir(self.directory):
            filepath = os.path.join(self.directory, filename)
            file_info = FileInformation(filepath)
            file_list.append(file_info.getData())
        return file_list

class FileInformation:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)

    def getData(self):
        try:
            author = win32api.GetFileVersionInfo(self.filepath, '\\StringFileInfo\\040601b0\\Author')
            tags = win32api.GetFileVersionInfo(self.filepath, '\\StringFileInfo\\040601b0\\Tags')
            title = win32api.GetFileVersionInfo(self.filepath, '\\StringFileInfo\\040601b0\\Title')
        except:
            author, tags, title = None, None, None
        properties = {
            'Name': self.filename,
            'Size': os.path.getsize(self.filepath),
            'Date modified': time.ctime(os.path.getmtime(self.filepath)),
            'Date created': time.ctime(os.path.getctime(self.filepath)),
            'File type': 'Directory' if os.path.isdir(self.filepath) else os.path.splitext(self.filename)[1],
            'Author': author,
            'Tags': tags,
            'Title': title
        }
        return properties

directoryScanner = DirectoryScanner('D:\\Proyectos Python')
for file in directoryScanner.getFiles():
    print(file)

for fileInfo in directoryScanner.getFiles():
    print(fileInfo['Size'])

