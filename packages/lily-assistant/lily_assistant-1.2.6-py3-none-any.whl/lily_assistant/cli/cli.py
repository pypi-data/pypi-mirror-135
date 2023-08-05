
import os
import click

from .copier import Copier
from ..checkers.commit_message import CommitMessageChecker
from ..checkers.repo import GitRepo
from ..checkers.structure import StructureChecker
from .logger import Logger
from lily_assistant.repo.repo import Repo
from lily_assistant.repo.version import VersionRenderer
from lily_assistant.config import Config


logger = Logger()


"""
Quick hack to force lily_assistant to see correct encoding locales.

Please keep in mind that those encoding will live only in the process
spawned by lily_assistant and will not contaminate your global namespace.

"""
if not os.environ.get('LC_ALL'):  # pragma: no cover
    os.environ['LC_ALL'] = 'en_US.utf-8'


if not os.environ.get('LANG'):  # pragma: no cover
    os.environ['LANG'] = 'en_US.utf-8'


@click.group()
def cli():
    """Expose multiple commands allowing one to work with lily_assistant."""
    pass


@click.command()
@click.argument('src_dir')
def init(src_dir):
    """Init `Lily-Assistant`.

    During this operation the following will take place:
    - git hooks will be copied to `./.git/hooks`
    - `.lily/lily_assistant.makefile` will be copied to the root project
      directory.

    WARNING it is assumed that this command will be invoked in the root
    of the project.

    :param src_dir: name of your source directory

    """
    Copier().copy(src_dir)

    logger.info('''

        Please insert the following line at the top of your Makefile:

        include .lily/lily_assistant.makefile
    ''')


@click.command()
def has_correct_structure():
    """Check if the repo has the required file / directory structure."""

    checker = StructureChecker()
    if not checker.is_valid():
        checker.raise_errors()


@click.command()
def is_not_master():
    """Check if one is not on master branch.

    Check if one is not attempting to perform certain operations directly
    against `master` branch.

    """

    is_not_master = GitRepo().active_branch != 'master'
    if not is_not_master:
        logger.error('''
            you shouldn't perform this action on the master branch
        ''')

    assert is_not_master


@click.command()
@click.argument('commit_msg_path')
def is_commit_message_valid(commit_msg_path):
    """Check if commit message follows standards."""

    with open(commit_msg_path) as f:
        message = f.read()

    is_valid = CommitMessageChecker(message).is_valid()

    if is_valid:
        logger.info('COMMIT MESSAGE: {message}'.format(message=message))

    else:
        logger.error('''
            your commit message is not following the commit message convention.
        ''')

    assert is_valid


@click.command()
def is_virtualenv():
    """Check if tests / code is executed against virtual environment."""

    is_virtualenv = len(os.environ.get('VIRTUAL_ENV', '').strip()) > 0
    if not is_virtualenv:
        logger.error('''
            You must run your tests & code against VIRTUAL ENVIRONMENT
        ''')

    assert is_virtualenv


@click.command()
@click.argument('upgrade_type', type=click.Choice([
    v.value for v in VersionRenderer.VERSION_UPGRADE
]))
def upgrade_version(upgrade_type):
    """Upgrade version of the repo artefacts.

    - update config.yaml file with version and last_commit_hash

    """

    config = Config()
    repo = Repo()
    version = VersionRenderer()

    if not repo.all_changes_commited():
        raise click.ClickException(
            'Not all changes were commited! One cannot upgrade version with '
            'some changes still being not commited')

    # -- next_version
    config.next_version = version.render_next_version(
        config.version, upgrade_type)

    # -- next_last_commit_hash
    config.next_last_commit_hash = repo.current_commit_hash

    logger.info(f'''
        - Next config version upgraded to: {config.next_version}
    ''')


@click.command()
def push_upgraded_version():
    """Push Upgraded version and all of its artefacts.

    - add commit with artefacts

    - tag branch with the version of repo

    - push changes to the remote

    """

    config = Config()
    repo = Repo()

    # -- version
    config.version = config.next_version
    config.next_version = None

    # -- last_commit_hash
    config.last_commit_hash = config.next_last_commit_hash
    config.next_last_commit_hash = None

    # -- add all artefacts coming from the post upgrade step
    repo.add_all()
    repo.commit('VERSION: {}'.format(config.version))
    repo.push()

    logger.info(f'''
        - Version upgraded to: {config.version}
    ''')


cli.add_command(init)


cli.add_command(has_correct_structure)


cli.add_command(is_not_master)


cli.add_command(is_commit_message_valid)


cli.add_command(is_virtualenv)


cli.add_command(upgrade_version)


cli.add_command(push_upgraded_version)
