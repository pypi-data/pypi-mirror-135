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

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import AccountEvent
from tikka.domains.entities.pubkey import PublicKey
from tikka.slots.pyqt.entities.constants import (
    ICON_ACCOUNT_LOCKED,
    ICON_ACCOUNT_UNLOCKED,
)
from tikka.slots.pyqt.resources.gui.widgets.account_rc import Ui_AccountWidget
from tikka.slots.pyqt.widgets.account_menu import AccountPopupMenu


class AccountWidget(QWidget, Ui_AccountWidget):
    """
    AccountWidget class
    """

    def __init__(
        self,
        application: Application,
        account: Account,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Init AccountWidget instance

        :param application: Application instance
        :param account: Account instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self.pubkey = account.pubkey

        self.BalanceLabel.setText(str(0))
        self.PublicKeyLabel.setText(str(PublicKey.from_pubkey(account.pubkey)))

        self._update_ui_from_account(account)

        # events
        self.customContextMenuRequested.connect(self.on_context_menu)
        self.application.event_dispatcher.add_event_listener(
            AccountEvent.EVENT_TYPE_UPDATE, self.on_account_update_event
        )

    def on_account_update_event(self, event: AccountEvent):
        """
        Triggered when the account is updated

        :param event: AccountEvent instance
        :return:
        """
        if event.account.pubkey != self.pubkey:
            return

        self._update_ui_from_account(event.account)

    def _update_ui_from_account(self, account: Account):
        """
        Update UI from account

        :param account: Account instance
        :return:
        """
        if account.signing_key is None:
            self.LockStatusIcon.setPixmap(QPixmap(ICON_ACCOUNT_LOCKED))
        else:
            self.LockStatusIcon.setPixmap(QPixmap(ICON_ACCOUNT_UNLOCKED))

    def on_context_menu(self, position: QPoint):
        """
        When right button on account tab

        :return:
        """
        # get selected account
        account = self.application.accounts.get_by_pubkey(self.pubkey)
        if account is not None:
            # display popup menu at click position
            menu = AccountPopupMenu(self.application, account)
            position.setY(position.y() + menu.heightMM())
            menu.exec_(position)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)
    account_ = Account("732SSfuwjB7jkt9th1zerGhphs6nknaCBCTozxUcPWPU")

    main_window = QMainWindow()
    main_window.show()

    main_window.setCentralWidget(AccountWidget(application_, account_, main_window))

    sys.exit(qapp.exec_())
