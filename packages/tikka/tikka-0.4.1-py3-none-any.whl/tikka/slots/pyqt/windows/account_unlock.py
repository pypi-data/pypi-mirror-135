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
from typing import TYPE_CHECKING, Optional

from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import (
    ACCESS_TYPE_CLASSIC,
    ACCESS_TYPE_MNEMONIC,
    DATA_PATH,
)
from tikka.domains.entities.pubkey import PublicKey
from tikka.slots.pyqt.resources.gui.windows.account_unlock_rc import Ui_UnlockDialog

if TYPE_CHECKING:
    import _


class AccountUnlockWindow(QDialog, Ui_UnlockDialog):
    """
    AccountUnlockWindow class
    """

    def __init__(
        self,
        application: Application,
        account: Account,
        parent: Optional[QWidget] = None,
    ):
        """
        Init unlock account window

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

        # events
        self.showButton.clicked.connect(self.on_show_button_clicked)
        self.access_code_line_edit.textChanged.connect(
            self.on_access_code_line_edit_changed
        )
        self.cesium_password_line_edit.textChanged.connect(
            self.cesium_password_line_edit_changed
        )
        self.buttonBox.rejected.connect(self.on_rejected_button)

    def on_show_button_clicked(self):
        """
        Triggered when user click on show button

        :return:
        """
        if self.access_code_line_edit.echoMode() == QLineEdit.Password:
            self.access_code_line_edit.setEchoMode(QLineEdit.Normal)
            self.cesium_password_line_edit.setEchoMode(QLineEdit.Normal)
            self.showButton.setText(self._("Hide"))
        else:
            self.access_code_line_edit.setEchoMode(QLineEdit.Password)
            self.cesium_password_line_edit.setEchoMode(QLineEdit.Password)
            self.showButton.setText(self._("Show"))

    def on_access_code_line_edit_changed(self):
        """
        Triggered when the access code field is changed

        :return:
        """
        self._unlock_account()

    def cesium_password_line_edit_changed(self):
        """
        Triggered when the access code field is changed

        :return:
        """
        self._unlock_account()

    def _unlock_account(self) -> None:
        """
        Validate fields and unlock account to enabled ok button

        :return:
        """
        password = (
            None
            if self.cesium_password_line_edit.text().strip() == ""
            else self.cesium_password_line_edit.text().strip()
        )
        access_code = self.access_code_line_edit.text().strip()
        try:
            result = self.application.accounts.unlock_account(
                self.account, access_code, password
            )
        except Exception:
            self.error_label.setText(self._("Access code or password is not valid!"))
            self.buttonBox.setEnabled(False)
            return None

        if not result:
            self.error_label.setText(self._("Access code or password is not valid!"))
            self.buttonBox.setEnabled(False)
            return None

        password = (
            None
            if self.cesium_password_line_edit.text().strip() == ""
            else self.cesium_password_line_edit.text().strip()
        )
        if self.account.access_type is None:
            # save the account access type
            self.account.access_type = (
                ACCESS_TYPE_MNEMONIC if password is None else ACCESS_TYPE_CLASSIC
            )
            self.application.accounts.update_account(self.account)

        self.buttonBox.setEnabled(True)
        self.error_label.setText("")

        return None

    def on_rejected_button(self) -> None:
        """
        Triggered when user click on cancel button

        :return:
        """
        self.application.accounts.lock_account(self.account)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    account_ = Account("CUYYUnh7N49WZhs5DULkmqw5Zu5fwsRBmE5LLrUFRpgw")
    AccountUnlockWindow(application_, account_).exec_()
