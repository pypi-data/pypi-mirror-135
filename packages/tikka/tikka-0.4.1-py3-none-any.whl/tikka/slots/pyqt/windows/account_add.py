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
from gettext import gettext
from typing import TYPE_CHECKING, Optional

from PyQt5.QtWidgets import QApplication, QDialog, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.pubkey import (
    PubkeyChecksumNotValid,
    PubkeyNotValid,
    PublicKey,
)
from tikka.slots.pyqt.resources.gui.windows.account_add_rc import Ui_AccountAddDialog

if TYPE_CHECKING:
    import _

tr = gettext


class AccountAddWindow(QDialog, Ui_AccountAddDialog):
    """
    AccountAddWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init add account window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application

        # events
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.public_key_line_edit.textChanged.connect(
            self.on_public_key_line_edit_changed
        )
        self.buttonBox.rejected.connect(self.close)

    @staticmethod
    def _get_public_key(text: str) -> PublicKey:
        """
        Convert text to PublicKey instance

        :param text: Base58 or Base58:checksum public key
        :return:
        """
        if ":" in text:
            base58, checksum = text.split(":", 2)
            pubkey = PublicKey(base58, checksum)
        else:
            pubkey = PublicKey.from_pubkey(text)

        return pubkey

    def _normalize_public_key_field(self) -> Optional[PublicKey]:
        """
        Validate and convert public key field to PublicKey instance

        :return:
        """
        entry = self.public_key_line_edit.text()
        try:
            pubkey = self._get_public_key(entry)
        except PubkeyChecksumNotValid:
            self.error_label.setText(tr("Checksum is not valid!"))
            return None
        except PubkeyNotValid:
            self.error_label.setText(tr("Public key is not valid!"))
            return None

        # create account instance
        account = Account(pubkey.base58)
        for existing_account in self.application.accounts.list:
            if account == existing_account:
                self.error_label.setText(tr("Account already exists!"))
                return None

        return pubkey

    def on_public_key_line_edit_changed(self) -> None:
        """
        Triggered when the public key field is changed

        :return:
        """
        pubkey = self._normalize_public_key_field()
        if pubkey is not None:
            self.error_label.setText("")
            self.buttonBox.setEnabled(True)
        else:
            self.buttonBox.setEnabled(False)

    def on_accepted_button(self) -> None:
        """
        Triggered when user click on ok button

        :return:
        """
        pubkey = self._normalize_public_key_field()
        if pubkey is not None:
            # create account instance
            account = Account(pubkey.base58)

            # add instance in application
            self.application.accounts.add_account(account)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    AccountAddWindow(application_).exec_()
