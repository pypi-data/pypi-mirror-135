
from unittest import TestCase
from unittest.mock import MagicMock, Mock, call

import pytest

from lily_assistant.checkers.repo import GitRepo


class GitRepoTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, mocker):
        self.mocker = mocker

    def test_active_branch(self):

        Popen = self.mocker.patch('lily_assistant.checkers.repo.Popen')  # noqa
        proc = Mock(stdout=Mock(read=Mock(return_value=b'some_branch')))
        Popen.return_value = MagicMock(__enter__=Mock(return_value=proc))

        assert GitRepo().active_branch == 'some_branch'
        assert Popen.call_args_list == [
            call(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=-1),
        ]

    def test_active_branch__strips_and_lower(self):

        Popen = self.mocker.patch('lily_assistant.checkers.repo.Popen')  # noqa
        proc = Mock(stdout=Mock(read=Mock(return_value=b' \t SOME_branch')))
        Popen.return_value = MagicMock(__enter__=Mock(return_value=proc))

        assert GitRepo().active_branch == 'some_branch'
        assert Popen.call_args_list == [
            call(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=-1),
        ]
