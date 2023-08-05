
import os
import textwrap
import setuptools


class File:

    def __init__(self, name, purpose):
        self.name = name
        self.purpose = purpose
        self.errors = []

    @property
    def path(self):
        """Project base / root dir (under which lily_assistant is run)."""

        return os.path.join(os.getcwd(), self.name)

    def is_valid(self):
        if not os.path.exists(self.path):
            self.errors.append(
                'Missing: `{self.name}` file. '
                'Its purpose is: {self.purpose}'.format(self=self))

            return False

        return True


class Directory(File):

    def __init__(self, name, purpose):
        self.name = name
        self.purpose = purpose
        self.errors = []

    def is_valid(self):
        if not (os.path.exists(self.path) and os.path.isdir(self.path)):
            self.errors.append(
                'Missing: `{self.name}` directory. '
                'Its purpose is: {self.purpose}'.format(self=self))

            return False

        return True


class StructureChecker:
    """Checks if the project is compliant with the structure guidelines.

    Structure required:
    ├── <project_name>/
    │   └── __init__.py
    ├── tests/
    ├── .git/
    ├── .gitignore
    ├── env.sh
    ├── Makefile
    ├── pytest.ini
    ├── README.md
    ├── requirements.txt
    ├── test-requirements.txt
    └── setup.py

    """

    REQUIRED_STRUCTURE = []

    class BrokenStructure(Exception):
        pass

    def __init__(self):

        self.errors = []
        self.REQUIRED_STRUCTURE = [
            File(
                name='env.sh',
                purpose='storing all environment variables needed by project'),
            File(
                name='pytest.ini',
                purpose='configuration of py.test'),
            File(
                name='README.md',
                purpose=(
                    'general overview of the project, steps to install etc.')),
            File(
                name='requirements.txt',
                purpose='project python package dependencies'),
            File(
                name='test-requirements.txt',
                purpose='project python package tests dependencies'),
            File(
                name='setup.py',
                purpose='builder'),
            File(
                name='Makefile',
                purpose='make file for all commands'),
            File(
                name='.gitignore',
                purpose='git file for ignoring not tracked files'),
            Directory(
                name='tests',
                purpose='tests directory'),
            Directory(
                name='.git',
                purpose='git repo directory'),
            Directory(
                name=StructureChecker.find_project_name(),
                purpose='project code directory'),
        ]

    @classmethod
    def find_project_name(cls):

        try:
            return [
                p
                for p in setuptools.find_packages()
                if p.lower() != 'tests' and '.' not in p][0]

        except IndexError:
            raise cls.BrokenStructure(textwrap.dedent('''

                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                Couldn't find main project directory

                Required structure:

                └── <project_dir>
                    └── __init__.py

            '''))

    def is_valid(self):

        for entity in self.REQUIRED_STRUCTURE:
            if not entity.is_valid():
                self.errors.extend(entity.errors)

        if self.errors:
            return False

        else:
            return True

    def raise_errors(self):
        errors = textwrap.indent(
            text='\n'.join(self.errors),
            prefix=12 * ' ' + '+ ').strip()
        project_name = StructureChecker.find_project_name()

        raise self.BrokenStructure(textwrap.dedent('''

            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            Project Structure Errors Detected

            REQUIRED STRUCTURE:
            ├── {project_name}/
            │   └── __init__.py
            ├── tests/
            ├── .git/
            ├── .gitignore
            ├── env.sh
            ├── Makefile
            ├── pytest.ini
            ├── README.md
            ├── requirements.txt
            ├── test-requirements.txt
            └── setup.py

            ERRORS:
            {errors}
        ''').format(project_name=project_name, errors=errors))
