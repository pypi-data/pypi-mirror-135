
import os
from unittest import TestCase
from unittest.mock import call

import pytest

from lily_assistant.repo.repo import Repo
from lily_assistant.config import Config


class RepoTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixture(self, mocker, tmpdir):
        self.mocker = mocker
        self.tmpdir = tmpdir

        self.base_dir = self.tmpdir.mkdir('base')
        self.mocker.patch.object(
            Config, 'get_project_path').return_value = str(self.base_dir)

    #
    # GIT
    #

    #
    # PUSH
    #
    def test_push(self):
        git = self.mocker.patch.object(Repo, 'git')
        git.return_value = 'feature/189-hello_world'
        r = Repo()

        r.push()

        assert git.call_args_list == [
            call('rev-parse --abbrev-ref HEAD'),
            call('push origin feature/189-hello_world'),
        ]

    #
    # PULL
    #
    def test_pull(self):
        git = self.mocker.patch.object(Repo, 'git')
        git.return_value = 'feature/190-hello_world'
        r = Repo()

        r.pull()

        assert git.call_args_list == [
            call('rev-parse --abbrev-ref HEAD'),
            call('pull origin feature/190-hello_world'),
        ]

    #
    # CURRENT_BRANCH
    #
    def test_current_branch(self):
        git = self.mocker.patch.object(Repo, 'git')
        git.return_value = 'feature/cs-178-hello-world\n'
        r = Repo()

        assert r.current_branch == 'feature/cs-178-hello-world'
        assert git.call_args_list == [call('rev-parse --abbrev-ref HEAD')]

    #
    # CURRENT_COMMIT_HASH
    #
    def test_current_commit_hash(self):
        git = self.mocker.patch.object(Repo, 'git')
        git.return_value = '671ca44b704cb5d2cf6df0c74b37fabc1\n'
        r = Repo()

        assert r.current_commit_hash == '671ca44b704cb5d2cf6df0c74b37fabc1'
        assert git.call_args_list == [call('rev-parse HEAD')]

    #
    # STASH
    #
    def test_stash(self):
        git = self.mocker.patch.object(Repo, 'git')
        r = Repo()

        r.stash()

        assert git.call_args_list == [call('stash')]

    #
    # ADD ALL
    #
    def test_add_all(self):
        git = self.mocker.patch.object(Repo, 'git')
        r = Repo()

        r.add_all()

        assert git.call_args_list == [call('add .'), call('add -u .')]

    #
    # ADD
    #
    def test_add(self):
        git = self.mocker.patch.object(Repo, 'git')
        r = Repo()

        r.add('/this/file')

        assert git.call_args_list == [call('add /this/file')]

    #
    # COMMIT
    #
    def test_commit(self):
        git = self.mocker.patch.object(Repo, 'git')
        r = Repo()

        r.commit('hello world')

        assert git.call_args_list == [
            call('commit --no-verify -m "hello world"'),
        ]

    #
    # ALL_CHANGES_COMMITED
    #
    def test_all_changes_commited__lily_changes(self):
        git = self.mocker.patch.object(Repo, 'git')
        git.side_effect = [
            # -- local changes
            (
                'M lily_assistant/cli/cli.py\n '
                'M tests/test_repo/test_version.py'
            ),

            # -- staged changes
            (
                'M  lily_assistant/cli/base.makefile'
            ),

            # -- staged changes, local changes
            (
                'M  lily_assistant/cli/base.makefile\n '
                'M lily_assistant/cli/cli.py\n '
                'M tests/test_repo/test_version.py'
            ),

            # -- staged changes & lily artefacts
            (
                'M  .lily/cli/base.makefile\n '
                'M  lily_assistant/cli/base.makefile'
            ),

            # -- lily conf changes (artefacts)
            (
                'M  .lily/cli/base.makefile'
            ),

            # -- no changes
            '\n\t',
        ]
        r = Repo()

        assert r.all_changes_commited() is False
        assert r.all_changes_commited() is False
        assert r.all_changes_commited() is False
        assert r.all_changes_commited() is False
        assert r.all_changes_commited() is True
        assert r.all_changes_commited() is True

        assert git.call_args_list == [
            call('status --porcelain'),
            call('status --porcelain'),
            call('status --porcelain'),
            call('status --porcelain'),
            call('status --porcelain'),
            call('status --porcelain'),
        ]

    def test_git(self):
        execute = self.mocker.patch.object(Repo, 'execute')
        r = Repo()

        r.git('whatever')

        assert execute.call_args_list == [call('git whatever')]

    #
    # GENERIC - EXECUTE
    #
    def test_execute(self):

        captured = Repo().execute('echo "hello world"')

        assert captured == 'hello world\n'

    def test_execute__raises_error(self):

        with pytest.raises(OSError) as e:
            Repo().execute('python -c "import sys; sys.exit(125)"')

        assert e.value.args[0] == (
            'Command: python -c "import sys; sys.exit(125)" '
            'return exit code: 125')

    #
    # GENERIC - SPLIT COMMAND
    #
    def test_split_command(self):

        assert Repo().split_command(
            'hi there') == ['hi', 'there']
        assert Repo().split_command(
            'hi   there') == ['hi', 'there']
        assert Repo().split_command(
            "hi   'there hello'") == ['hi', 'there hello']
        assert Repo().split_command(
            'hi   "there hello"') == ['hi', 'there hello']

        assert Repo().split_command('git commit -m "hello world"') == [
            'git', 'commit', '-m', 'hello world']

    #
    # DIR / FILES
    #
    def test_clear_dir(self):

        hi_dir = self.base_dir.mkdir('hi')
        hi_dir.join('hello.txt').write('hi')
        hi_dir.join('bye.md').write('bye')

        r = Repo()

        assert sorted(os.listdir(str(hi_dir))) == ['bye.md', 'hello.txt']

        r.clear_dir('hi')

        assert os.listdir(str(hi_dir)) == []

    def test_create_dir(self):

        Repo().create_dir('hello')

        assert os.path.exists(
            os.path.join(str(self.base_dir), 'hello')) is True

    def test_create_dir__twice(self):

        r = Repo()

        r.create_dir('hello')

        # -- this will return not error
        r.create_dir('hello')
