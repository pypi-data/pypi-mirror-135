
from enum import Enum, unique


class VersionRenderer:

    @unique
    class VERSION_UPGRADE(Enum):  # noqa

        MAJOR = 'MAJOR'

        MINOR = 'MINOR'

        PATCH = 'PATCH'

    def render_next_version(
            self, current_version, upgrade_type=VERSION_UPGRADE.PATCH.value):

        major, minor, patch = current_version.split('.')
        major, minor, patch = int(major), int(minor), int(patch)

        if upgrade_type == self.VERSION_UPGRADE.MAJOR.value:
            major += 1
            minor = 0
            patch = 0

        elif upgrade_type == self.VERSION_UPGRADE.MINOR.value:
            minor += 1
            patch = 0

        elif upgrade_type == self.VERSION_UPGRADE.PATCH.value:
            patch += 1

        return '{0}.{1}.{2}'.format(major, minor, patch)
