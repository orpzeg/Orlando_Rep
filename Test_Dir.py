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
    filename = f'{command.replace("/", "")}.txt'
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

    def test_dirB(self):
        cmddir_file_generator(self.cmddir, 'dir /B', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir B')
        command_runner = run_commmand(f'dir /B {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dirD(self):
        cmddir_file_generator(self.cmddir, 'dir /D', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir D')
        command_runner = run_commmand(f'dir /D {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dirON(self):
        cmddir_file_generator(self.cmddir, 'dir /ON', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir ON')
        command_runner = run_commmand(f'dir /ON {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dirOS(self):
        cmddir_file_generator(self.cmddir, 'dir /OS', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir OS')
        command_runner = run_commmand(f'dir /OS {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dirTC(self):
        cmddir_file_generator(self.cmddir, 'dir /TC', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir TC')
        command_runner = run_commmand(f'dir /TC {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dirTA(self):
        cmddir_file_generator(self.cmddir, 'dir /TA', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir TA')
        command_runner = run_commmand(f'dir /TA {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dirW(self):
        cmddir_file_generator(self.cmddir, 'dir /W', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir W')
        command_runner = run_commmand(f'dir /W {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dir4(self):
        cmddir_file_generator(self.cmddir, 'dir /4', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir 4')
        command_runner = run_commmand(f'dir /4 {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def test_dirA_NOT_A(self):
        cmddir_file_generator(self.cmddir, 'dir /A-A', self.demo_dir)  # Create the command files
        file_content = open_files(self.cmddir, 'dir A-A')
        command_runner = run_commmand(f'dir /A-A {self.demo_dir}', 'Test')
        self.assertEqual(file_content, command_runner)

    def tearDown(self) -> None:
        run_commmand(f'rmdir /S /Q {self.demo_dir}')
        run_commmand(f'rmdir /S /Q {self.cmddir}')

if __name__ == '__main__':
    unittest.main()
