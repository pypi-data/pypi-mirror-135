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
from typing import Optional

from PyQt5.QtWidgets import QApplication, QDialog, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import ACCESS_TYPE_MNEMONIC, DATA_PATH
from tikka.domains.entities.pubkey import PublicKey
from tikka.domains.entities.signing_key import TikkaSigningKey
from tikka.libs.secret import generate_dubp_scrypt_salt, generate_mnemonic
from tikka.slots.pyqt.resources.gui.windows.account_create_rc import (
    Ui_AccountCreateDialog,
)


class AccountCreateWindow(QDialog, Ui_AccountCreateDialog):
    """
    AccountCreateWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init create account window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application

        # events
        self.change_button.clicked.connect(self._generate_mnemonic_and_pubkey)
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

        # fill form
        self._generate_mnemonic_and_pubkey()

    def _generate_mnemonic_and_pubkey(self):
        """
        Generate mnemonic access_code and pubkey

        :return:
        """
        access_code = generate_mnemonic(self.application.config.get("language"))
        self.access_code_line_edit.setText(access_code)
        self.cesium_password_line_edit.setText(
            generate_dubp_scrypt_salt(access_code).hex()
        )
        self.public_key_line_edit.setText(
            str(
                PublicKey.from_pubkey(
                    TikkaSigningKey.from_dubp_mnemonic(access_code).pubkey
                )
            )
        )

    def on_accepted_button(self):
        """
        Triggered when user click on ok button

        :return:
        """
        # create pubkey instance
        pubkey = PublicKey.from_pubkey_with_checksum(self.public_key_line_edit.text())
        # create account instance
        account = Account(pubkey.base58, access_type=ACCESS_TYPE_MNEMONIC)
        # add instance in application
        self.application.accounts.add_account(account)

        # close window
        self.close()


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    AccountCreateWindow(application_).exec_()
