
import os
from unittest import TestCase

import pytest

from lily_assistant.checkers.structure import (
    StructureChecker,
    File,
    Directory,
)
from tests import remove_white_chars


class FileTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, tmpdir, mocker):
        self.tmpdir = tmpdir
        self.mocker = mocker

    #
    # IS_VALID
    #
    def test_is_valid__exists(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.join('some.txt').write('something')
        os.chdir(str(base_dir))

        f = File('some.txt', 'whatever')

        assert f.is_valid() is True
        assert f.errors == []

    def test_is_valid__does_not_exist(self):

        base_dir = self.tmpdir.mkdir('base')
        os.chdir(str(base_dir))

        f = File('some.txt', 'whatever')

        assert f.is_valid() is False
        assert f.errors == [
            'Missing: `some.txt` file. Its purpose is: whatever',
        ]


class DirectoryTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, tmpdir, mocker):
        self.tmpdir = tmpdir
        self.mocker = mocker

    #
    # IS_VALID
    #
    def test_is_valid__exists(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.mkdir('tests')
        os.chdir(str(base_dir))

        d = Directory('tests', 'whatever')

        assert d.is_valid() is True
        assert d.errors == []

    def test_is_valid__does_not_exist(self):

        base_dir = self.tmpdir.mkdir('base')
        os.chdir(str(base_dir))

        d = Directory('tests', 'whatever')

        assert d.is_valid() is False
        assert d.errors == [
            'Missing: `tests` directory. Its purpose is: whatever',
        ]

    def test_is_valid__not_directory(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.join('tests').write('something')
        os.chdir(str(base_dir))

        d = Directory('tests', 'whatever')

        assert d.is_valid() is False
        assert d.errors == [
            'Missing: `tests` directory. Its purpose is: whatever',
        ]


class StructureCheckerTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, tmpdir, mocker):
        self.tmpdir = tmpdir
        self.mocker = mocker

    #
    # FIND_PROJECT_NAME
    #
    def test_find_project_name__all_ok(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.mkdir('code').join('__init__.py').write('#')
        os.chdir(str(base_dir))

        assert StructureChecker.find_project_name() == 'code'

    def test_find_project_name__missing_project_directory(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.mkdir('code')
        os.chdir(str(base_dir))

        with pytest.raises(StructureChecker.BrokenStructure) as e:
            StructureChecker.find_project_name()

        text = e.value.args[0]
        expected = remove_white_chars('''

            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            Couldn't find main project directory

            Required structure:

            └── <project_dir>
                └── __init__.py
        ''')

        assert remove_white_chars(text) == expected

    #
    # IS_VALID
    #
    def test_is_valid__all_ok(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.mkdir('tests')
        base_dir.join('requirements.txt').write('require')
        base_dir.join('Makefile').write('make')
        base_dir.mkdir('code').join('__init__.py').write('#')
        os.chdir(str(base_dir))

        checker = StructureChecker()
        self.mocker.patch.object(
            checker,
            'REQUIRED_STRUCTURE',
            [
                File('requirements.txt', 'to require'),
                File('Makefile', 'to make'),
                Directory('tests', 'to test'),
                Directory('code', 'to code'),
            ])

        assert checker.is_valid() is True
        assert checker.errors == []

    def test_is_valid__missing_file(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.mkdir('tests')
        base_dir.join('Makefile').write('make')
        base_dir.mkdir('code').join('__init__.py').write('#')
        os.chdir(str(base_dir))

        checker = StructureChecker()
        self.mocker.patch.object(
            checker,
            'REQUIRED_STRUCTURE',
            [
                File('requirements.txt', 'to require'),
                File('Makefile', 'to make'),
                Directory('tests', 'to test'),
                Directory('code', 'to code'),
                Directory('images', 'to image'),
            ])

        assert checker.is_valid() is False
        assert checker.errors == [
            'Missing: `requirements.txt` file. Its purpose is: to require',
            'Missing: `images` directory. Its purpose is: to image',
        ]

    #
    # RAISE_ERRORS
    #
    def test_raise_errors(self):

        base_dir = self.tmpdir.mkdir('base')
        base_dir.mkdir('tests')
        base_dir.join('Makefile').write('make')
        base_dir.mkdir('code').join('__init__.py').write('# ...')
        os.chdir(str(base_dir))

        checker = StructureChecker()
        self.mocker.patch.object(
            checker,
            'REQUIRED_STRUCTURE',
            [
                File('requirements.txt', 'to require'),
                File('Makefile', 'to make'),
                Directory('tests', 'to test'),
                Directory('code', 'to code'),
                Directory('images', 'to image'),
            ])
        checker.is_valid()

        with pytest.raises(checker.BrokenStructure) as e:
            checker.raise_errors()

        text = e.value.args[0]
        expected = remove_white_chars('''

            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            Project Structure Errors Detected

            REQUIRED STRUCTURE:
            ├── code/
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
            + Missing: `requirements.txt` file. Its purpose is: to require
            + Missing: `images` directory. Its purpose is: to image
        ''')

        assert remove_white_chars(text) == expected
