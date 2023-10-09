import subprocess
import os
import unittest


class CommandRunner:
    """Handles running of shell commands."""

    @staticmethod
    def run(command, filter_text=None):
        """
        Runs a command and optionally filters the output.

        :param command: The command to run.
        :param filter_text: If specified, lines containing this text will be filtered out.
        :return: Command output as a string.
        """
        result = subprocess.run(command, capture_output=True, text=True, shell=True).stdout.strip()
        if filter_text:
            result = '\n'.join(line for line in result.split('\n') if filter_text not in line)
        return result


class DirectoryManager:
    """Handles directory and file operations."""

    @staticmethod
    def _sanitize_command(command):
        """Sanitize command to be used as a file name."""
        return command.replace("/", "").replace("-", "").replace(" ", "_")

    @staticmethod
    def create_directory(path, dir_name):
        """Create a directory, if it doesn't exist, and return its path."""
        directory = os.path.join(path, dir_name)
        os.makedirs(directory, exist_ok=True)
        return directory

    @staticmethod
    def generate_demo_files(directory, file_name):
        """Generate files with increasing sizes in the specified directory."""
        size = 1024
        while size <= 1_048_576:
            filename = os.path.join(directory, f'{file_name}{size}.txt')
            CommandRunner.run(f'fsutil file createnew "{filename}" {size}')
            size *= 2

    @staticmethod
    def create_command_output_file(directory, command, target_directory):
        """Generate a file containing the output of a command."""
        sanitized_command = DirectoryManager._sanitize_command(command)
        filename = os.path.join(directory, f'{sanitized_command}.txt')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(CommandRunner.run(f'{command} {target_directory}', 'bytes free'))

    @staticmethod
    def read_file(directory, command):
        """Read the content of a file and return it."""
        sanitized_command = DirectoryManager._sanitize_command(command)
        filename = os.path.join(directory, f'{sanitized_command}.txt')
        with open(filename, 'r') as file:
            return file.read()


class TestDir(unittest.TestCase):
    """Test class to verify the correctness of commands."""

    def setUp(self):
        """Setup temporary directories and generate demo files."""
        temp_dir = CommandRunner.run('echo %temp%')
        self.demo_dir = DirectoryManager.create_directory(temp_dir, 'Orlando')
        DirectoryManager.generate_demo_files(self.demo_dir, 'rlnd')
        self.cmd_dir = DirectoryManager.create_directory(temp_dir, 'dirfile')

    def _test_command(self, command):
        """Utility method to test a command."""
        DirectoryManager.create_command_output_file(self.cmd_dir, command, self.demo_dir)
        file_content = DirectoryManager.read_file(self.cmd_dir, command)
        command_output = CommandRunner.run(f'{command} {self.demo_dir}', 'bytes free')
        self.assertEqual(file_content, command_output)

    def test_dir(self):
        self._test_command('dir')

    def test_dirB(self):
        self._test_command('dir /B')

    def test_dirD(self):
        self._test_command('dir /D')

    def test_dirON(self):
        self._test_command('dir /ON')

    def test_dirOS(self):
        self._test_command('dir /OS')

    def test_dirTC(self):
        self._test_command('dir /TC')

    def test_dirTA(self):
        self._test_command('dir /TA')

    def test_dirW(self):
        self._test_command('dir /W')

    def test_dir4(self):
        self._test_command('dir /4')

    def test_dirA_Not_A(self):
        self._test_command('dir /A-A')

    def tearDown(self):
        """Cleanup temporary directories."""
        CommandRunner.run(f'rmdir /S /Q {self.demo_dir}')
        CommandRunner.run(f'rmdir /S /Q {self.cmd_dir}')


if __name__ == '__main__':
    unittest.main()
