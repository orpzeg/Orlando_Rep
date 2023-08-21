import os
import time
import win32api
import win32com
import win32com.client

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
        shell = win32com.client.Dispatch("Shell.Application")
        namespace = shell.Namespace(os.path.dirname(self.filepath))
        item = namespace.ParseName(os.path.basename(self.filepath))
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
            'Title': title,
            'File description': namespace.GetDetailsOf(item, 34),
            'Product name': namespace.GetDetailsOf(item, 297),
            'Product version': namespace.GetDetailsOf(item, 298),
            'Copyright': namespace.GetDetailsOf(item, 25)
        }
        return properties

directoryScanner = DirectoryScanner('C:\\Program Files\\JetBrains\\PyCharm Community Edition 2023.1.4\\bin')
for file in directoryScanner.getFiles():
    print(file)

for fileInfo in directoryScanner.getFiles():
    print(fileInfo['Name'])
