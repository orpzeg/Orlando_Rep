import subprocess
import os
import unittest


def run_commmand(command, test=None):
    result = subprocess.run(command, capture_output=True, text=True, shell=True).stdout.strip()
    if test == 'Test':
        res = result.split('\n')
        res = [line for line in res if 'bytes free' not in line]
        result = '\n'.join(res)
    return result

def directory_generator(path, dir_name):
    directory = os.path.join(path, dir_name)
    os.makedirs(directory, exist_ok=True)
    return directory

def demo_file_generator(directory, file_name):
    size = 1024
    while size <= 1_048_576:
        filename = os.path.join(directory, f'{file_name}{size}.txt')
        run_commmand(f'fsutil file createnew "{filename}" {size}')
        size *= 2

def cmddir_file_generator(directory, command, target_directory):
    filename = f'{command}.txt'
    output_path = os.path.join(directory, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(run_commmand(f'{command} {target_directory}', 'Test'))

def open_files(directory, command):
    filename = os.path.join(directory, f'{command}.txt')
    with open(filename, 'r') as file:
        content = file.read()
    return content


class TestDir(unittest.TestCase):
    def setUp(self) -> None:
        dir = run_commmand('echo %temp%')
        self.demo_dir = directory_generator(dir, 'Orlando')  # Create the demo directory
        demo_file_generator(self.demo_dir, 'rlnd')  # Create the demo files
        self.cmddir = directory_generator(dir, 'dirfile')  # Create the command directory

    def test_dir(self):
        cmddir_file_generator(self.cmddir, 'dir', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir')
        command_runner = run_commmand(f'dir {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

