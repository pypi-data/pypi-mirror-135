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

from PyQt5.QtWidgets import QApplication, QDialog, QRadioButton, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.slots.pyqt.resources.gui.windows.configuration_rc import (
    Ui_ConfigurationDialog,
)

RADIO_BUTTON_VALUES = {
    "radioButtonLanguage_en_US": "en_US",
    "radioButtonLanguage_fr_FR": "fr_FR",
    "radioButtonCurrency_g1": "g1",
    "radioButtonCurrency_g1_test": "g1-test",
}


class ConfigurationWindow(QDialog, Ui_ConfigurationDialog):
    """
    ConfigurationWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init configuration window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application

        # language
        selected_language_radio_button_name = list(RADIO_BUTTON_VALUES.keys())[
            list(RADIO_BUTTON_VALUES.values()).index(
                self.application.config.get("language")
            )
        ]
        selected_language_radio_button: Optional[QRadioButton] = self.findChild(
            QRadioButton, selected_language_radio_button_name
        )
        if selected_language_radio_button is not None:
            selected_language_radio_button.setChecked(True)
        self.radioButtonLanguage_en_US.toggled.connect(self.language_select)
        self.radioButtonLanguage_fr_FR.toggled.connect(self.language_select)

        # currency
        selected_currency_radio_button_name = list(RADIO_BUTTON_VALUES.keys())[
            list(RADIO_BUTTON_VALUES.values()).index(
                self.application.config.get("currency")
            )
        ]
        selected_currency_radio_button: Optional[QRadioButton] = self.findChild(
            QRadioButton, selected_currency_radio_button_name
        )
        if selected_currency_radio_button is not None:
            selected_currency_radio_button.setChecked(True)
        self.radioButtonCurrency_g1.toggled.connect(self.currency_select)
        self.radioButtonCurrency_g1_test.toggled.connect(self.currency_select)

    def language_select(self, checked: bool):
        """
        User has selected a language radio button

        :param checked: True if sender checked
        :return:
        """
        if checked:
            self.application.select_language(
                RADIO_BUTTON_VALUES[self.sender().objectName()]
            )

    def currency_select(self, checked: bool):
        """
        User has toggled a currency radio button

        :param checked: True if sender checked
        :return:
        """
        if checked:
            self.application.select_currency(
                RADIO_BUTTON_VALUES[self.sender().objectName()]
            )


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    ConfigurationWindow(application_).exec_()
