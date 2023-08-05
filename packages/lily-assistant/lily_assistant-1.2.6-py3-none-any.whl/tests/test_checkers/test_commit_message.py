
from unittest import TestCase

from lily_assistant.checkers.commit_message import CommitMessageChecker


class CommitMessageCheckerTestCase(TestCase):

    def test_is_valid(self):

        assert CommitMessageChecker('message').is_valid() is True
