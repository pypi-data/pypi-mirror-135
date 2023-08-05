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

from PyQt5.QtWidgets import QApplication, QMenu, QMessageBox, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.pubkey import PublicKey
from tikka.slots.pyqt.windows.account_unlock import AccountUnlockWindow
from tikka.slots.pyqt.windows.wallet_load import WalletLoadWindow
from tikka.slots.pyqt.windows.wallet_save import WalletSaveWindow


class AccountPopupMenu(QMenu):
    """
    AccountPopupMenu class
    """

    def __init__(
        self,
        application: Application,
        account: Account,
        parent: Optional[QWidget] = None,
    ):
        """
        Init AccountPopupMenu instance

        :param application: Application instance
        :param account: Account instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)

        self.application = application
        self.account = account

        # menu actions
        copy_pubkey_to_clipboard_action = self.addAction("Copy public key to clipboard")
        copy_pubkey_to_clipboard_action.triggered.connect(self.copy_pubkey_to_clipboard)

        if account.signing_key is None:
            unlock_account_action = self.addAction("Unlock account access")
            unlock_account_action.triggered.connect(self.unlock_account)
            unlock_account_by_file_action = self.addAction("Unlock by file")
            unlock_account_by_file_action.triggered.connect(self.unlock_account_by_file)
        else:
            lock_account_action = self.addAction("Lock account access")
            lock_account_action.triggered.connect(self.lock_account)
            save_wallet_action = self.addAction("Save wallet to disk")
            save_wallet_action.triggered.connect(self.save_wallet)

        withdraw_account_action = self.addAction("Withdraw account")
        withdraw_account_action.triggered.connect(self.confirm_withdraw_account)

    def copy_pubkey_to_clipboard(self):
        """
        Copy pubkey of selected row to clipboard

        :return:
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(str(PublicKey.from_pubkey(self.account.pubkey)))

    def unlock_account(self):
        """
        Open account unlock window

        :return:
        """
        AccountUnlockWindow(self.application, self.account, self).exec_()

    def unlock_account_by_file(self):
        """
        Open account unlock by file window

        :return:
        """
        WalletLoadWindow(self.application, self).exec_()

    def lock_account(self):
        """
        Lock account

        :return:
        """
        self.application.accounts.lock_account(self.account)

    def save_wallet(self):
        """
        Open save wallet window

        :return:
        """
        WalletSaveWindow(self.application, self.account, self).exec_()

    def confirm_withdraw_account(self):
        """
        Display confirm dialog then withdraw account if confirmed

        :return:
        """
        # display confirm dialog and get response
        button = QMessageBox.question(
            self,
            "Withdraw account",
            f"Withdraw account {PublicKey.from_pubkey(self.account.pubkey)}?",
        )
        if button == QMessageBox.Yes:
            self.application.accounts.delete_account(self.account)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)
    account_ = Account("732SSfuwjB7jkt9th1zerGhphs6nknaCBCTozxUcPWPU")

    menu = AccountPopupMenu(application_, account_)
    menu.exec_()

    sys.exit(qapp.exec_())
