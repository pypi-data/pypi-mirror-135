
import os
from unittest import TestCase
from unittest.mock import call, Mock
import textwrap

from click.testing import CliRunner
import pytest

from lily_assistant.checkers.commit_message import CommitMessageChecker
from lily_assistant.checkers.repo import GitRepo
from lily_assistant.cli.cli import cli
from lily_assistant.cli.copier import Copier
from lily_assistant.config import Config
from lily_assistant.repo.repo import Repo
from lily_assistant.repo.version import VersionRenderer


class ConfigMock:

    def __init__(
            self,
            version,
            last_commit_hash,
            next_version=None,
            next_last_commit_hash=None):
        self._version = version
        self._last_commit_hash = last_commit_hash
        self._next_version = next_version
        self._next_last_commit_hash = next_last_commit_hash

    @classmethod
    def get_config_path(cls):
        return '/some/path/config.json'

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def next_version(self):
        return self._next_version

    @next_version.setter
    def next_version(self, value):
        self._next_version = value

    @property
    def last_commit_hash(self):
        return self._last_commit_hash

    @last_commit_hash.setter
    def last_commit_hash(self, value):
        self._last_commit_hash = value

    @property
    def next_last_commit_hash(self):
        return self._next_last_commit_hash

    @next_last_commit_hash.setter
    def next_last_commit_hash(self, value):
        self._next_last_commit_hash = value


class CliTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, mocker, tmpdir):
        self.mocker = mocker
        self.tmpdir = tmpdir

        self.base_dir = tmpdir.mkdir('base')
        self.mocker.patch.object(
            Config, 'get_project_path').return_value = str(self.base_dir)

    def setUp(self):
        self.runner = CliRunner()

    #
    # INIT
    #
    def test_init(self):

        copy = self.mocker.patch.object(Copier, 'copy')

        result = self.runner.invoke(cli, ['init', 'src_dir'])
        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            [INFO]

            Please insert the following line at the top of your Makefile:

            include .lily/lily_assistant.makefile
        ''').strip()
        assert copy.call_args_list == [call('src_dir')]

    #
    # HAS_CORRECT_STRUCTURE
    #
    def test_has_correct_structure__valid(self):

        raise_errors = Mock()
        self.mocker.patch(
            'lily_assistant.cli.cli.StructureChecker'
        ).return_value = Mock(
            is_valid=Mock(return_value=True),
            raise_errors=raise_errors)

        result = self.runner.invoke(cli, ['has-correct-structure'])

        assert result.exit_code == 0
        assert result.output == ''
        assert raise_errors.call_count == 0

    def test_has_correct_structure__invalid(self):

        raise_errors = Mock()
        self.mocker.patch(
            'lily_assistant.cli.cli.StructureChecker'
        ).return_value = Mock(
            is_valid=Mock(return_value=False),
            raise_errors=raise_errors)

        result = self.runner.invoke(cli, ['has-correct-structure'])

        assert result.exit_code == 0
        assert result.output == ''
        assert raise_errors.call_args_list == [call()]

    #
    # IS_NOT_MASTER
    #
    def test_is_not_master__true(self):

        self.mocker.patch.object(GitRepo, 'active_branch', 'development')

        result = self.runner.invoke(cli, ['is-not-master'])

        assert result.exit_code == 0
        assert result.output == ''

    def test_is_not_master__false(self):

        self.mocker.patch.object(GitRepo, 'active_branch', 'master')

        result = self.runner.invoke(cli, ['is-not-master'])

        assert result.exit_code == 1
        assert result.output.strip() == textwrap.dedent('''
            [ERROR]

            you shouldn't perform this action on the master branch
        ''').strip()

    #
    # IS_COMMIT_MESSAGE_VALID
    #
    def test_is_commit_message_valid__valid(self):

        self.mocker.patch.object(
            CommitMessageChecker, 'is_valid').return_value = True
        commit_msg = self.tmpdir.join('message.txt')
        commit_msg.write('hello world')

        result = self.runner.invoke(
            cli, ['is-commit-message-valid', str(commit_msg)])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            [INFO]

            COMMIT MESSAGE: hello world
        ''').strip()

    def test_is_commit_message_valid__invalid(self):

        self.mocker.patch.object(
            CommitMessageChecker, 'is_valid').return_value = False
        commit_msg = self.tmpdir.join('message.txt')
        commit_msg.write('hello world')

        result = self.runner.invoke(
            cli, ['is-commit-message-valid', str(commit_msg)])

        assert result.exit_code == 1
        assert result.output.strip() == textwrap.dedent('''
            [ERROR]

            your commit message is not following the commit message convention.
        ''').strip()

    #
    # IS_VIRTUALENV
    #
    def test_is_virtualenv__false(self):

        os.environ['VIRTUAL_ENV'] = ''

        result = self.runner.invoke(cli, ['is-virtualenv'])

        assert result.exit_code == 1
        assert result.output.strip() == textwrap.dedent('''
            [ERROR]

            You must run your tests & code against VIRTUAL ENVIRONMENT
        ''').strip()

    def test_is_virtualenv__true(self):

        os.environ['VIRTUAL_ENV'] = 'something'

        result = self.runner.invoke(cli, ['is-virtualenv'])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    #
    # UPGRADE VERSION
    #
    def test_upgrade_version__makes_the_right_calls(self):

        self.mocker.patch.object(Repo, 'current_commit_hash', '222222')
        self.mocker.patch.object(
            Repo,
            'all_changes_commited'
        ).return_value = True
        render_next_version = self.mocker.patch.object(
            VersionRenderer, 'render_next_version')
        render_next_version.return_value = '1.2.13'

        config = ConfigMock(
            version='1.2.12',
            last_commit_hash='111111')
        self.mocker.patch(
            'lily_assistant.cli.cli.Config',
        ).return_value = config

        result = self.runner.invoke(
            cli,
            ['upgrade-version', VersionRenderer.VERSION_UPGRADE.MAJOR.value])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            [INFO]

            - Next config version upgraded to: 1.2.13
        ''').strip()

        assert config.version == '1.2.12'
        assert config.last_commit_hash == '111111'
        assert config.next_version == '1.2.13'
        assert config.next_last_commit_hash == '222222'

        assert render_next_version.call_args_list == [call('1.2.12', 'MAJOR')]

    def test_upgrade_version__not_commited_chages(self):

        self.mocker.patch.object(Repo, 'current_commit_hash', '222222')
        self.mocker.patch.object(
            Repo,
            'all_changes_commited'
        ).return_value = False
        render_next_version = self.mocker.patch.object(
            VersionRenderer, 'render_next_version')
        render_next_version.return_value = '1.2.13'

        config = ConfigMock(
            version='1.2.12',
            next_version=None,
            last_commit_hash='111111',
            next_last_commit_hash=None)
        self.mocker.patch(
            'lily_assistant.cli.cli.Config',
        ).return_value = config

        result = self.runner.invoke(
            cli,
            ['upgrade-version', VersionRenderer.VERSION_UPGRADE.MAJOR.value])

        assert result.exit_code == 1
        assert result.output.strip() == (
            'Error: Not all changes were commited! One cannot upgrade '
            'version with some changes still being not commited')

        # -- config version and commit_hash didn't change
        assert config.version == '1.2.12'
        assert config.next_version is None
        assert config.last_commit_hash == '111111'
        assert config.next_last_commit_hash is None

        assert render_next_version.call_count == 0

    # def test_upgrade_version__invalid_upgrade_type(self):

    #     result = self.runner.invoke(
    #         cli, ['upgrade-version', 'NOT_MAJOR'])

    #     assert result.exit_code == 2
    #     assert (
    #         'invalid choice: NOT_MAJOR. '
    #         '(choose from MAJOR, MINOR, PATCH)') in result.output

    #
    # PUSH_UPGRADED_VERSION
    #
    def test_push_upgraded_version__makes_the_right_calls(self):

        repo_add_all = self.mocker.patch.object(Repo, 'add_all')
        repo_commit = self.mocker.patch.object(Repo, 'commit')
        repo_push = self.mocker.patch.object(Repo, 'push')

        config = ConfigMock(
            version='1.2.12',
            next_version='1.2.13',
            last_commit_hash='111111',
            next_last_commit_hash='222222')
        self.mocker.patch(
            'lily_assistant.cli.cli.Config',
        ).return_value = config

        result = self.runner.invoke(cli, ['push-upgraded-version'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            [INFO]

            - Version upgraded to: 1.2.13
        ''').strip()

        assert config.version == '1.2.13'
        assert config.next_version is None
        assert config.last_commit_hash == '222222'
        assert config.next_last_commit_hash is None

        assert repo_add_all.call_args_list == [call()]
        assert repo_commit.call_args_list == [call('VERSION: 1.2.13')]
        assert repo_push.call_args_list == [call()]
