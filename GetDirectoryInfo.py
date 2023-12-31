import os
import time
import win32api
import win32com
import win32com.client
import argparse
import json
from pymongo import MongoClient


class DirectoryScanner:
    """Class to scan a specified directory for files."""

    def __init__(self, directory):
        """Initialize DirectoryScanner with a target directory."""
        self.directory = directory

    def getfiles(self):
        """Function to retrieve all files' information within the directory."""
        file_list = []
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_info = FileInformation(self.directory, filepath)
                file_list.append(file_info.getdata())
        return file_list


class FileInformation:
    """Class to extract and structure relevant information of a given file."""

    def __init__(self, base_directory, filepath):
        """Initialize FileInformation with base directory and target filepath."""
        self.base_directory = base_directory
        self.filepath = filepath
        self.filename = os.path.basename(filepath)

    def getdata(self):
        """Function to gather detailed properties of the file."""
        shell = win32com.client.Dispatch('Shell.Application')
        namespace = shell.Namespace(os.path.dirname(self.filepath))
        item = namespace.ParseName(os.path.basename(self.filepath))
        partial_filepath = self.filepath.replace(self.base_directory, '', 1).lstrip('\\')
        try:
            author = win32api.GetFileVersionInfo(self.filepath, '\\StringFileInfo\\040601b0\\Author')
            tags = win32api.GetFileVersionInfo(self.filepath, '\\StringFileInfo\\040601b0\\Tags')
            title = win32api.GetFileVersionInfo(self.filepath, '\\StringFileInfo\\040601b0\\Title')
        except Exception:
            author, tags, title = None, None, None
        properties = {
            'Name': self.filename.split('.')[0],
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
            'Copyright': namespace.GetDetailsOf(item, 25),
            'Filepath': partial_filepath
        }
        return properties


def main():
    """Main function to initiate directory scanning and data saving."""
    parser = argparse.ArgumentParser(description='Scan a directory and retrieve the file information.')
    parser.add_argument('--directory', type=str, help='Path to the directory to be scanned.')
    parser.add_argument('--output', type=str, help='Path to the output JSON file')
    parser.add_argument('--db_name', type=str, help='Name of the MongoDB database')
    parser.add_argument('--collection_name', type=str, help='Name of the MongoDB collection')
    parser.add_argument('--connection_string', type=str, default='mongodb://localhost:27017/',
                        help='connection string MongDB')

    args = parser.parse_args()

    directoryScanner = DirectoryScanner(args.directory)
    files_info = directoryScanner.getfiles()

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(files_info, f, ensure_ascii=False, indent=4)

    client = MongoClient(args.connection_string)

    db = client[args.db_name]
    collection = db[args.collection_name]

    collection.insert_many(files_info)


if __name__ == '__main__':
    main()
