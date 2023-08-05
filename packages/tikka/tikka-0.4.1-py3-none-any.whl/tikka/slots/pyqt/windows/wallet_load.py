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

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QLineEdit, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.interfaces.repository.preferences import (
    WALLET_LOAD_DEFAULT_DIRECTORY,
)
from tikka.slots.pyqt.resources.gui.windows.wallet_load_rc import Ui_WalletLoadDialog

if TYPE_CHECKING:
    import _


class WalletLoadWindow(QDialog, Ui_WalletLoadDialog):
    """
    WalletLoadWindow class
    """

    def __init__(
        self,
        application: Application,
        parent: Optional[QWidget] = None,
    ):
        """
        Init load wallet window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self.wallet = None
        self._ = self.application.translator.gettext

        # events
        self.show_button.clicked.connect(self._on_show_button_clicked)
        self.browse_files_button.clicked.connect(self._on_browse_files_button_clicked)
        self.access_code_line_edit.editingFinished.connect(
            self._on_access_code_line_edit_finished
        )
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self._on_accepted_button)

    def _on_show_button_clicked(self):
        """
        Triggered when user click on show button

        :return:
        """
        if self.access_code_line_edit.echoMode() == QLineEdit.Password:
            self.access_code_line_edit.setEchoMode(QLineEdit.Normal)
            self.show_button.setText(self._("Hide"))
        else:
            self.access_code_line_edit.setEchoMode(QLineEdit.Password)
            self.show_button.setText(self._("Show"))

    def _on_browse_files_button_clicked(self):
        """
        Triggered when user click on browse files button

        :return:
        """
        # clear path
        self.path_value_label.setText("")

        # open file dialog
        filepath = self.open_file_dialog()
        if filepath is not None:
            # update default dir preference
            self.application.preferences_repository.set(
                WALLET_LOAD_DEFAULT_DIRECTORY,
                str(Path(filepath).expanduser().absolute().parent),
            )
            self.path_value_label.setText(filepath)

    def open_file_dialog(self) -> Optional[str]:
        """
        Open file dialog and return the selected filepath or None

        :return:
        """
        default_dir = self.application.preferences_repository.get(
            WALLET_LOAD_DEFAULT_DIRECTORY
        )
        if default_dir is not None:
            default_dir = str(Path(default_dir).expanduser().absolute())
        else:
            default_dir = ""

        result = QFileDialog.getOpenFileName(
            self, self._("Choose wallet file"), default_dir, "EWIF Files (*.dunikey)"
        )
        if result[0] == "":
            return None

        return result[0]

    def _on_access_code_line_edit_finished(self):
        """
        Triggered when the access code field editing is finished

        :return:
        """
        access_code = self.access_code_line_edit.text().strip()

        if access_code == "":
            return
        try:
            self.wallet = self.application.wallets.load(
                self.path_value_label.text(), access_code
            )
        except Exception:
            self.error_label.setText(self._("Unable to decrypt file!"))
            self.buttonBox.setEnabled(False)
            return

        if not self.wallet.signing_key:
            self.error_label.setText(self._("Access code is not valid!"))
            self.buttonBox.setEnabled(False)
            return

        # wallet decrypted
        self.error_label.setText("")
        self.buttonBox.setEnabled(True)

    def _on_accepted_button(self):
        """
        Triggered when user click on cancel button

        :return:
        """
        if self.wallet is not None:
            self.application.accounts.load_wallet(self.wallet)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    WalletLoadWindow(
        application_,
    ).exec_()
