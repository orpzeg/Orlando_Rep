import os
import time
import win32api
import win32com
import win32com.client
import argparse
import json

class DirectoryScanner:
    def __init__(self, directory):
        self.directory = directory

    def getFiles(self):
        file_list = []
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_info = FileInformation(filepath)
                file_list.append(file_info.getData())
        return file_list

class FileInformation:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)

    def getData(self):
        shell = win32com.client.Dispatch('Shell.Application')
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
            'File type': os.path.splitext(self.filename)[1],
            'Author': author,
            'Tags': tags,
            'Title': title,
            'File description': namespace.GetDetailsOf(item, 34),
            'Product name': namespace.GetDetailsOf(item, 297),
            'Product version': namespace.GetDetailsOf(item, 298),
            'Copyright': namespace.GetDetailsOf(item, 25)
        }
        return properties

def main():
    parser = argparse.ArgumentParser(description='Scan a directory and retrieve the file information.')
    parser.add_argument('--directory', type=str, help='Path to the directory to be scanned.')
    parser.add_argument('--output', type=str, help='Path to the output JSON file')

    args = parser.parse_args()

    directoryScanner = DirectoryScanner(args.directory)
    files_info = directoryScanner.getFiles()

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(files_info, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
