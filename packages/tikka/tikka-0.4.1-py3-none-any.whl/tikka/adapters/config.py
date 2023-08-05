# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os
import shutil
from pathlib import Path
from typing import Any

from tikka.domains.entities.constants import CONFIG_FILENAME
from tikka.domains.interfaces.config import ConfigInterface

ASSETS_PATH = Path(__file__).parent.joinpath("assets")
DEFAULT_CONFIG_PATH = ASSETS_PATH.joinpath(CONFIG_FILENAME)


class FileConfig(ConfigInterface):
    data: dict = {}
    filepath = None

    def __init__(self, path: Path):
        """
        Create config file in user config path

        :param path: Path instance of config file path
        :return:
        """
        self.filepath = Path().joinpath(path, CONFIG_FILENAME).expanduser()

        if not path.expanduser().exists():
            os.makedirs(path.expanduser())

        if not self.filepath.exists():
            # copy default config in user config path
            shutil.copyfile(DEFAULT_CONFIG_PATH.expanduser(), self.filepath)

        # load config file in data
        self.load()

    def load(self):
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConfigInterface.load.__doc__
        )
        with self.filepath.open("r", encoding="utf-8") as file_handler:
            self.data = json.load(file_handler)

    def save(self):
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConfigInterface.save.__doc__
        )
        with self.filepath.open("w", encoding="utf-8") as file_handler:
            json.dump(self.data, file_handler)

    def set(self, name: str, value: Any):
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConfigInterface.set.__doc__
        )
        self.data[name] = value
        self.save()

    def get(self, name: str):
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            ConfigInterface.get.__doc__
        )
        return self.data[name]
