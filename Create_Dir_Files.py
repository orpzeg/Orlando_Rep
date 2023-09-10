import re
import argparse
import subprocess
import os


def getFlags(command):
    cmd = f'{command} /?'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    flags = re.findall(r"/\w", result.stdout)
    filtered_flags = [flag for flag in set(flags) if flag[1].isupper()]
    return filtered_flags


def createFiles(command, directory, output):
    list_of_flags = getFlags(command)
    for flag in list_of_flags:
        cmd = f'{command} {directory} {flag}'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        filename = f'{flag[1:]}.txt'
        output_path = os.path.join(output, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.stdout)


def create(commands, directory, output):
    filenames = []
    for com in commands:
        cmd = f'{com} {directory}'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        filename = f'{com.replace("/","")}.txt'
        output_path = os.path.join(output, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        filenames.append(filename)
    return filenames


def main():
    parser = argparse.ArgumentParser(description='Create files with a specific command')
    parser.add_argument('--command', nargs='+', help='Command from which you wish to create the files')
    parser.add_argument('--directory', type=str, help='Directory from which you wish to create the files')
    parser.add_argument('--output', type=str, help='Output directory for the obtained files')

    args = parser.parse_args()

    fileaddresses = create(args.command, f"\"{args.directory}\"", args.output)
    for fileaddress in fileaddresses:
        print(f"File created successfully: {fileaddress}")

if __name__ == '__main__':
    main()