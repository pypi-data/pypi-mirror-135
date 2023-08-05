
from subprocess import Popen, PIPE


class GitRepo:

    @property
    def active_branch(self):

        command = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        with Popen(command, stdout=PIPE) as proc:
            active_branch = str(proc.stdout.read(), encoding='utf-8')

            return active_branch.strip().lower()
