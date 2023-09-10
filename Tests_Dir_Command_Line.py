import subprocess
import unittest
import os
import argparse


def run_dir_command(command, directory):
    cmd = f'{command} \"{directory}\"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout


def open_files(com, name):
    filename = os.path.join(name, f'{com}.txt')
    with open(filename, 'r') as file:
        content = file.read()
    return content


class TestDirCommand(unittest.TestCase):

    directory = None
    path = None

    def test_dir(self):
        self.command = 'dir'
        output = run_dir_command(self.command, TestDirCommand.directory)
        output_lines = output.split('\n')
        output_lines = [line for line in output_lines if 'bytes free' not in line]
        processed_output = '\n'.join(output_lines)
        file_content = open_files(self.command, TestDirCommand.path)
        file_content_lines = file_content.split('\n')
        file_content_lines = [line for line in file_content_lines if 'bytes free' not in line]
        processed_file_content = '\n'.join(file_content_lines)
        self.assertEqual(processed_output, processed_file_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the dir command from the command line')
    parser.add_argument('--directory', required=True, help='Directory which is going to be tested')
    parser.add_argument('--path',required=True, help='Directory where is the file to be compared')

    args, remaining = parser.parse_known_args()

    TestDirCommand.directory = args.directory
    TestDirCommand.path = args.path

    unittest.main(argv=[__file__] + remaining)

