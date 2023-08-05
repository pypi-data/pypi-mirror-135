
import os
import json
from unittest import TestCase
from unittest.mock import call
import textwrap

import pytest

from lily_assistant.cli.copier import Copier


class CopierTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, tmpdir, mocker):
        self.tmpdir = tmpdir
        self.mocker = mocker

    def setUp(self):
        self.lily_assistant_dir = self.tmpdir.mkdir('lily_assistant')
        self.project_dir = self.tmpdir.mkdir('project')
        self.project_dir.mkdir('.lily').join('config.json').write(json.dumps({
            'version': '0.0.11'
        }))
        os.chdir(str(self.project_dir))

    #
    # COPY
    #
    def test_copy__makes_the_right_calls(self):

        copy_hooks = self.mocker.patch.object(Copier, 'copy_hooks')
        copy_makefile = self.mocker.patch.object(Copier, 'copy_makefile')

        Copier().copy('my_code')

        assert copy_hooks.call_args_list == [call()]
        assert copy_makefile.call_args_list == [call('my_code')]

    #
    # CREATE_EMPTY_CONFIG
    #
    def test_create_empty_config__does_not_exist(self):

        config_json = self.project_dir.join('.lily').join('config.json')

        assert json.loads(config_json.read()) == {
            'version': '0.0.11'
        }

        Copier().create_empty_config('gigly')

        assert json.loads(config_json.read()) == {
            'version': '0.0.11'
        }

    def test_create_empty_config__exists(self):

        config_json = self.project_dir.join('.lily').join('config.json')

        os.remove(str(config_json))

        Copier().create_empty_config('gigly')

        assert json.loads(config_json.read()) == {
            'last_commit_hash': '... THIS WILL BE FILLED AUTOMATICALLY ...',
            'name': '... PUT HERE NAME OF YOUR PROJECT ...',
            'repository': '... PUT HERE URL OF REPOSITORY ...',
            'src_dir': 'gigly',
            'version': '... PUT HERE INITIAL VERSION ...',
            'next_version': None,
            'next_last_commit_hash': None,
        }

    #
    # COPY_HOOKS
    #
    def test_copy_hooks__copies_all_hooks(self):

        gitdir = self.project_dir.mkdir('.git')

        hooks_dir = self.lily_assistant_dir.mkdir('hooks')
        hooks_dir.join('pre-commit').write('pre commit it')
        hooks_dir.join('surprise').write('surprise me')
        self.mocker.patch.object(Copier, 'base_hooks_path', str(hooks_dir))
        copy_hooks_dir = gitdir.mkdir('hooks')

        Copier().copy_hooks()

        assert os.listdir(str(gitdir)) == ['hooks']
        assert set(os.listdir(str(copy_hooks_dir))) == set([
            'pre-commit',
            'surprise',
        ])

    def test_copy_hooks__not_root(self):

        self.project_dir.mkdir('.git')
        no_root_dir = self.project_dir.mkdir('not_root')
        os.chdir(no_root_dir)

        with pytest.raises(Copier.NotProjectRootException) as e:
            Copier().copy_hooks()

        assert e.value.args[0] == (
            'it seems that you\'ve executed not from the root of '
            'the project.')

    def test_copy_hooks__copies_all_hooks__with_override(self):

        gitdir = self.project_dir.mkdir('.git')

        hooks_dir = self.lily_assistant_dir.mkdir('hooks')
        hooks_dir.join('pre-commit').write('NEW pre commit it')
        hooks_dir.join('surprise').write('NEW surprise me')
        self.mocker.patch.object(Copier, 'base_hooks_path', str(hooks_dir))
        copy_hooks_dir = os.path.join(str(gitdir), 'hooks')

        Copier().copy_hooks()

        assert os.listdir(str(gitdir)) == ['hooks']
        assert set(os.listdir(str(copy_hooks_dir))) == set([
            'pre-commit',
            'surprise',
        ])
        assert (
            open(os.path.join(str(copy_hooks_dir), 'pre-commit')).read() ==
            'NEW pre commit it')
        assert (
            open(os.path.join(str(copy_hooks_dir), 'surprise')).read() ==
            'NEW surprise me')

    def test_copy_hooks__copies_all_hooks__when_hooks_do_not_exist(self):

        gitdir = self.project_dir.mkdir('.git')

        hooks_dir = self.lily_assistant_dir.mkdir('hooks')
        hooks_dir.join('pre-commit').write('NEW pre commit it')
        hooks_dir.join('surprise').write('NEW surprise me')
        self.mocker.patch.object(Copier, 'base_hooks_path', str(hooks_dir))
        copy_hooks_dir = gitdir.mkdir('hooks')
        copy_hooks_dir.join('pre-commit').write('OLD pre commit it')

        Copier().copy_hooks()

        assert os.listdir(str(gitdir)) == ['hooks']
        assert set(os.listdir(str(copy_hooks_dir))) == set([
            'pre-commit',
            'surprise',
        ])
        assert (
            open(os.path.join(str(copy_hooks_dir), 'pre-commit')).read() ==
            'NEW pre commit it')
        assert (
            open(os.path.join(str(copy_hooks_dir), 'surprise')).read() ==
            'NEW surprise me')

    #
    # COPY_MAKEFILE
    #
    def test_copy_makefile__copies_makefile(self):

        makefile = self.lily_assistant_dir.join('lily_assistant.makefile')
        makefile.write(textwrap.dedent('''
            ## GENERATED FOR VERSION: {% VERSION %}

            lint:  ## lint the {% SRC_DIR %} & tests
                source env.sh && \
                flake8 --ignore D100,D101 tests && \
                flake8 --ignore D100,D101 {% SRC_DIR %}
        '''))
        self.mocker.patch.object(Copier, 'base_makefile_path', str(makefile))

        Copier().copy_makefile(str('gigly'))

        result_makefile_content = (
            self.project_dir.join('.lily/lily_assistant.makefile').read())
        assert result_makefile_content == textwrap.dedent('''
            ## GENERATED FOR VERSION: 0.0.11

            lint:  ## lint the gigly & tests
                source env.sh && \
                flake8 --ignore D100,D101 tests && \
                flake8 --ignore D100,D101 gigly
        ''')

    def test_copy_makefile__copies_makefile__with_override(self):

        makefile = self.lily_assistant_dir.join('lily_assistant.makefile')
        makefile.write('NEW make it')
        self.mocker.patch.object(Copier, 'base_makefile_path', str(makefile))
        self.project_dir.join(
            '.lily/lily_assistant.makefile').write('OLD make it')

        Copier().copy_makefile(str('gigly'))

        assert (
            self.project_dir.join('.lily/lily_assistant.makefile').read() ==
            'NEW make it')
