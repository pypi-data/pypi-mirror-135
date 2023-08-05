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
from typing import TYPE_CHECKING, Any, List, Optional

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget

from tikka import __version__
from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import CURRENCIES, DATA_PATH
from tikka.domains.entities.events import AccountEvent, CurrencyEvent
from tikka.domains.entities.pubkey import PublicKey
from tikka.domains.entities.tab import Tab
from tikka.domains.interfaces.repository.preferences import SELECTED_TAB_PAGE_KEY
from tikka.slots.pyqt.resources.gui.windows.main_window_rc import Ui_MainWindow
from tikka.slots.pyqt.widgets.account import AccountWidget
from tikka.slots.pyqt.widgets.account_list import AccountListWidget
from tikka.slots.pyqt.widgets.licence import LicenceWidget
from tikka.slots.pyqt.windows.about import AboutWindow
from tikka.slots.pyqt.windows.account_add import AccountAddWindow
from tikka.slots.pyqt.windows.account_create import AccountCreateWindow
from tikka.slots.pyqt.windows.configuration import ConfigurationWindow
from tikka.slots.pyqt.windows.wallet_load import WalletLoadWindow

if TYPE_CHECKING:
    import _


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    MainWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init main window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext

        self.update_title()

        # tab widgets
        self.account_list_widget: Optional[AccountListWidget] = None

        # signals
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        # connect functions to menu actions
        self.actionQuit.triggered.connect(self.close)
        self.actionAccount_list.triggered.connect(self.add_account_list_tab)
        self.actionAdd_existing_account.triggered.connect(self.open_add_account_window)
        self.actionCreate_account.triggered.connect(self.open_create_account_window)
        self.actionLoad_a_Wallet.triggered.connect(self.open_load_wallet_window)
        self.actionG1_licence.triggered.connect(self.add_licence_tab)
        self.actionConfiguration.triggered.connect(self.open_configuration_window)
        self.actionAbout.triggered.connect(self.open_about_window)

        # subscribe to application events
        self.application.event_dispatcher.add_event_listener(
            CurrencyEvent.EVENT_TYPE_CHANGED, self.on_currency_event
        )
        self.application.event_dispatcher.add_event_listener(
            AccountEvent.EVENT_TYPE_ADD, self.on_add_account_event
        )
        self.application.event_dispatcher.add_event_listener(
            AccountEvent.EVENT_TYPE_DELETE, self.on_delete_account_event
        )

        # open saved tabs
        self.init_tabs()

    def closeEvent(
        self, event: QtGui.QCloseEvent  # pylint: disable=unused-argument
    ) -> None:
        """
        Override close event

        :param event:
        :return:
        """
        # save tabs in repository
        self.save_tabs()

        # save tab selection in preferences
        self.application.preferences_repository.set(
            SELECTED_TAB_PAGE_KEY, self.tabWidget.currentIndex()
        )

    def init_tabs(self):
        """
        Init tabs from repository

        :return:
        """
        # close all tabs
        self.tabWidget.clear()

        # fetch tabs from repository
        for tab in self.application.tab_repository.list():
            # if account tab...
            if tab.panel_class == AccountWidget.__name__:
                # get account from list
                for account in self.application.accounts.list:
                    if account.pubkey == tab.id:
                        self.add_account_tab(account)
            elif tab.panel_class == LicenceWidget.__name__:
                self.add_licence_tab()
            elif tab.panel_class == AccountListWidget.__name__:
                self.add_account_list_tab()

        # get preferences
        preferences_selected_page = self.application.preferences_repository.get(
            SELECTED_TAB_PAGE_KEY
        )
        if preferences_selected_page is not None:
            self.tabWidget.setCurrentIndex(int(preferences_selected_page))

    def save_tabs(self):
        """
        Save tabs in tab repository

        :return:
        """
        # clear table
        self.application.tab_repository.delete_all()
        # save tabwidget tabs in repository
        for index in range(0, self.tabWidget.count()):
            widget = self.tabWidget.widget(index)
            if isinstance(widget, AccountWidget):
                # save account tab in repository
                tab = Tab(widget.pubkey, str(widget.__class__.__name__))
            else:
                tab = Tab(
                    str(widget.__class__.__name__), str(widget.__class__.__name__)
                )

            self.application.tab_repository.add(tab)

    def close_tab(self, index: int):
        """
        Close tab on signal

        :param index: Index of tab requested to close
        :return:
        """
        self.tabWidget.removeTab(index)

    def add_account_list_tab(self) -> None:
        """
        Open account list tab

        :return:
        """
        if len(self.get_tab_widgets_by_class(AccountListWidget)) == 0:
            account_list_widget = AccountListWidget(self.application, self.tabWidget)
            self.tabWidget.addTab(account_list_widget, self._("Account list"))
            # catch account list double click signal
            account_list_widget.tableWidget.itemDoubleClicked.connect(
                self.on_account_list_double_click
            )
            self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    def add_account_tab(self, account: Account):
        """
        Open account list tab

        :return:
        """
        if (
            len(
                [
                    widget
                    for widget in self.get_tab_widgets_by_class(AccountWidget)
                    if widget.pubkey == account.pubkey
                ]
            )
            == 0
        ):
            self.tabWidget.addTab(
                AccountWidget(self.application, account, self.tabWidget),
                str(PublicKey.from_pubkey(account.pubkey).shorten_checksum),
            )
            self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    def add_licence_tab(self):
        """
        Open licence tab

        :return:
        """
        if len(self.get_tab_widgets_by_class(LicenceWidget)) == 0:
            self.tabWidget.addTab(
                LicenceWidget(self.application, self.tabWidget), self._("Ğ1 licence")
            )
            self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    def update_title(self):
        """
        Update window title with version and currency

        :return:
        """
        self.setWindowTitle(
            "Tikka {version} - {currency}".format(  # pylint: disable=consider-using-f-string
                version=__version__,
                currency=CURRENCIES[self.application.config.get("currency")],
            )
        )

    def open_add_account_window(self) -> None:
        """
        Open add account window

        :return:
        """
        AccountAddWindow(self.application, self).exec_()

    def open_create_account_window(self) -> None:
        """
        Open create account window

        :return:
        """
        AccountCreateWindow(self.application, self).exec_()

    def open_load_wallet_window(self) -> None:
        """
        Open create account window

        :return:
        """
        WalletLoadWindow(self.application, self).exec_()

    def open_configuration_window(self) -> None:
        """
        Open configuration window

        :return:
        """
        ConfigurationWindow(self.application, self).exec_()

    def open_about_window(self) -> None:
        """
        Open about window

        :return:
        """
        AboutWindow(self).exec_()

    def on_currency_event(self):
        """
        When a currency event is triggered

        :return:
        """
        self.update_title()

    def on_account_list_double_click(self, item: QTableWidgetItem):
        """
        When an account is double clicked in account list

        :param item: QTableWidgetItem instance
        :return:
        """
        account = self.application.accounts.list[item.row()]
        self.add_account_tab(account)

    def on_add_account_event(self, event: AccountEvent) -> None:
        """
        Triggered when an account is created

        :param event: AccountEvent instance
        :return:
        """
        self.add_account_tab(event.account)

    def on_delete_account_event(self, event: AccountEvent) -> None:
        """
        Triggered when an account is deleted

        :param event: AccountEvent instance
        :return:
        """
        for widget in self.get_tab_widgets_by_class(AccountWidget):
            if widget.pubkey == event.account.pubkey:
                self.tabWidget.removeTab(self.tabWidget.indexOf(widget))

    def get_tab_widgets_by_class(self, widget_class: Any) -> List[QWidget]:
        """
        Return a list of widget which are instance of widget_class

        :param widget_class: Widget class
        :return:
        """
        widgets = []
        for index in range(0, self.tabWidget.count()):
            widget = self.tabWidget.widget(index)
            if isinstance(widget, widget_class):
                widgets.append(widget)

        return widgets


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    MainWindow(application_).show()
    sys.exit(qapp.exec_())
