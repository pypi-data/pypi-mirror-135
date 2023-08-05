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
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.pubkey import PublicKey
from tikka.domains.interfaces.repository.preferences import (
    WALLET_SAVE_DEFAULT_DIRECTORY,
)
from tikka.libs.secret import generate_alphabetic
from tikka.slots.pyqt.resources.gui.windows.wallet_save_rc import Ui_WalletSaveDialog

if TYPE_CHECKING:
    import _


class WalletSaveWindow(QDialog, Ui_WalletSaveDialog):
    """
    WalletSaveWindow class
    """

    def __init__(
        self,
        application: Application,
        account: Account,
        parent: Optional[QWidget] = None,
    ):
        """
        Init save wallet window

        :param application: Application instance
        :param account: Account instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self.account = account
        self._ = self.application.translator.gettext

        self.public_key_value_label.setText(
            str(PublicKey.from_pubkey(self.account.pubkey))
        )
        self.file_format = "EWIF"

        # generate access code
        self.acces_code_line_edit.setText(generate_alphabetic())

        # events
        self.change_button.clicked.connect(self._on_change_button_clicked)
        self.browse_files_button.clicked.connect(self._on_browse_files_button_clicked)

    def _on_change_button_clicked(self):
        """
        Triggered when user click on change button

        :return:
        """
        self.acces_code_line_edit.setText(generate_alphabetic())

    def _on_browse_files_button_clicked(self):
        """
        Triggered when user click on browse files button

        :return:
        """
        # clear error label
        self.error_label.setText("")

        # open file dialog
        filepath = self.open_file_dialog()
        if filepath is not None:
            # update default dir preference
            self.application.preferences_repository.set(
                WALLET_SAVE_DEFAULT_DIRECTORY,
                str(Path(filepath).expanduser().absolute().parent),
            )

            # save wallet
            result = self.application.accounts.save_wallet(
                self.account,
                filepath,
                self.acces_code_line_edit.text(),
                self.application.config.get("currency"),
            )
            if not result:
                self.error_label.setText(self.tr("Failed to save wallet!"))
                return

            self.close()

    def open_file_dialog(self) -> Optional[str]:
        """
        Open file dialog and return the selected filepath or None

        :return:
        """
        default_dir = self.application.preferences_repository.get(
            WALLET_SAVE_DEFAULT_DIRECTORY
        )
        if default_dir is not None:
            default_dir = str(Path(default_dir).expanduser().absolute())
        else:
            default_dir = ""

        pubkey = PublicKey.from_pubkey(self.account.pubkey)
        # extension = self.wallet_format_value.GetString(
        #     self.wallet_format_value.GetSelection()
        # ).lower()
        extension = self.file_format.lower()
        if extension == "ewif":
            extension = "dunikey"
        filename = "{name}_{pubkey}-{checksum}_{currency}.{extension}".format(  # pylint: disable=consider-using-f-string
            name="wallet",
            pubkey=pubkey.shorten,
            checksum=pubkey.checksum,
            currency=self.application.config.get("currency"),
            extension=extension,
        )

        result = QFileDialog.getSaveFileName(
            self,
            self.tr("Save wallet file"),
            str(Path(default_dir).joinpath(filename)),
            "EWIF Files (*.dunikey)",
        )
        if result[0] == "":
            return None

        return result[0]


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    account_ = Account("732SSfuwjB7jkt9th1zerGhphs6nknaCBCTozxUcPWPU")
    WalletSaveWindow(application_, account_).exec_()
