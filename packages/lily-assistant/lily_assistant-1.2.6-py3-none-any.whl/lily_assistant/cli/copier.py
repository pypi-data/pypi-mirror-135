
import os
import re
import shutil

import click

from lily_assistant.config import Config


class Copier:

    class NotProjectRootException(Exception):
        pass

    def __init__(self):
        self.root_dir = os.getcwd()

    def copy(self, src_dir):

        self.create_empty_config(src_dir)

        self.copy_hooks()

        self.copy_makefile(src_dir)

    def create_empty_config(self, src_dir):

        if not Config.exists():
            Config.create_empty(src_dir)

    def copy_hooks(self):

        git_dir = os.path.join(self.root_dir, '.git')
        copy_hooks_dir = os.path.join(git_dir, 'hooks')
        if os.path.exists(git_dir):
            if os.path.exists(copy_hooks_dir):
                shutil.rmtree(copy_hooks_dir)

        else:
            raise Copier.NotProjectRootException(
                'it seems that you\'ve executed not from the root of the '
                'project.')

        shutil.copytree(self.base_hooks_path, copy_hooks_dir)

        click.secho(
            'copied git hooks to {copy_hooks_dir}'.format(
                copy_hooks_dir=copy_hooks_dir),
            fg='blue')

    def copy_makefile(self, src_dir):

        config = Config()

        with open(self.base_makefile_path, 'r') as makefile:
            content = makefile.read()
            content = re.sub(r'{%\s*SRC_DIR\s*%}', src_dir, content)
            content = re.sub(r'{%\s*VERSION\s*%}', config.version, content)

        makefile_path = os.path.join(
            self.root_dir, '.lily', 'lily_assistant.makefile')

        with open(makefile_path, 'w') as f:
            f.write(content)

        click.secho(
            'copied lily_assistant makefile to {makefile_path}'.format(
                makefile_path=makefile_path),
            fg='blue')

    @property
    def base_makefile_path(self):

        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'base.makefile')

    @property
    def base_hooks_path(self):

        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'hooks')
