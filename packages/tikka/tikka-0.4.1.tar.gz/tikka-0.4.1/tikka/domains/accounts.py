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
import copy
import logging
from pathlib import Path
from typing import Optional

from mnemonic import Mnemonic

from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import MNEMONIC_LANGUAGES
from tikka.domains.entities.events import AccountEvent
from tikka.domains.entities.pubkey import PublicKey
from tikka.domains.entities.signing_key import TikkaSigningKey
from tikka.domains.entities.wallet import Wallet
from tikka.domains.events import EventDispatcher
from tikka.domains.interfaces.repository.accounts import AccountRepositoryInterface
from tikka.domains.interfaces.wallets import WalletsInterface


class Accounts:

    list: list = []

    """
    Account domain class
    """

    def __init__(
        self,
        repository: AccountRepositoryInterface,
        wallets: WalletsInterface,
        event_dispatcher: EventDispatcher,
        language: str,
    ):
        """
        Init Accounts domain

        :param repository: Database adapter instance
        :param wallets: Wallets adapter instance
        :param event_dispatcher: EventDispatcher instance
        :param language: Language for mnemonic

        """
        self.repository = repository
        self.wallets = wallets
        self.event_dispatcher = event_dispatcher
        self.language = language

        # init account list from database
        self.init_accounts()

    def init_accounts(self):
        """
        Init accounts from currency database connection

        :return:
        """
        # get accounts from database
        self.list = self.repository.list()

    def add_account(self, account: Account):
        """
        Add account action

        :param account: Account instance
        :return:
        """
        # add account
        self.list.append(account)
        self.repository.add(account)

        # dispatch event
        event = AccountEvent(
            AccountEvent.EVENT_TYPE_ADD,
            copy.copy(account),
        )
        self.event_dispatcher.dispatch_event(event)

    def update_account(self, account: Account):
        """
        Update account in database

        :param account: Account instance
        :return:
        """
        # update only non hidden fields
        self.repository.update(account)

    def get_by_index(self, index: int) -> Account:
        """
        Return account instance from index

        :param index: Index in account list
        :return:
        """
        return self.list[index]

    def get_by_pubkey(self, pubkey: str) -> Optional[Account]:
        """
        Return account instance from pubkey

        :param pubkey: Account public key
        :return:
        """
        for account in self.list:
            if account.pubkey == pubkey:
                return account

        return None

    def delete_account(self, account: Account) -> None:
        """
        Delete account in list and database

        :param account: Account instance to delete
        :return:
        """
        index = self.list.index(account)
        del self.list[index]
        self.repository.delete(account)

        # dispatch event
        event = AccountEvent(
            AccountEvent.EVENT_TYPE_DELETE,
            copy.copy(account),
        )
        self.event_dispatcher.dispatch_event(event)

    def unlock_account(
        self, account: Account, passphrase: str, password: Optional[str] = None
    ) -> bool:
        """
        Unlock account if credentials match pubkey, if not, return False

        :param account: Account instance
        :param passphrase: Passphrase
        :param password: Password
        :return:
        """
        # create signing_key from credentials
        if password is None:
            signing_key = TikkaSigningKey.from_dubp_mnemonic(
                passphrase
            )  # type: TikkaSigningKey
            # store mnemonic entropy needed to save wallet
            account.entropy = Mnemonic(MNEMONIC_LANGUAGES[self.language]).to_entropy(
                passphrase
            )
        else:
            signing_key = TikkaSigningKey.from_credentials(passphrase, password)

        # create pubkey instance
        account_pubkey = PublicKey.from_pubkey(account.pubkey)

        if signing_key is not None and account_pubkey == PublicKey.from_pubkey(
            signing_key.pubkey
        ):
            # save keypair in account instance
            account.signing_key = signing_key

            # dispatch event
            event = AccountEvent(
                AccountEvent.EVENT_TYPE_UPDATE,
                copy.copy(account),
            )
            self.event_dispatcher.dispatch_event(event)
            return True

        return False

    def lock_account(self, account: Account):
        """
        Lock account by removing signing_key

        :param account: Account instance
        :return:
        """
        account.signing_key = None

        # dispatch event
        event = AccountEvent(
            AccountEvent.EVENT_TYPE_UPDATE,
            copy.copy(account),
        )
        self.event_dispatcher.dispatch_event(event)

    def load_wallet(self, wallet: Wallet) -> Optional[Account]:
        """
        Create/Update an account from a wallet instance

        :param wallet: Wallet instance
        :return:
        """
        if wallet.signing_key is None:
            return None

        for account in self.list:
            # if account exists in list...
            if account.pubkey == wallet.signing_key.pubkey:
                account.signing_key = wallet.signing_key

                # dispatch event
                event = AccountEvent(
                    AccountEvent.EVENT_TYPE_UPDATE,
                    copy.copy(account),
                )
                self.event_dispatcher.dispatch_event(event)
                return account

        # create pubkey instance
        pubkey = PublicKey.from_pubkey(wallet.signing_key.pubkey)
        # create account instance
        account = Account(pubkey.base58)
        account.signing_key = wallet.signing_key
        self.add_account(account)

        return account

    def save_wallet(
        self, account: Account, path: str, password: str, currency: str
    ) -> bool:
        """
        Save account on disk as Wallet

        :param account: Account instance
        :param path: Path of the wallet on disk
        :param password: Wallet password
        :param currency: Currency codename
        :return:
        """
        if account.signing_key is None:
            return False

        wallet = Wallet(
            Path(path),
            "DEWIF" if Path(path).suffix == ".dewif" else "EWIF",
            True,
            account.signing_key,
        )

        try:
            self.wallets.save(wallet, password, currency)
        except Exception as exception:
            logging.error(exception)
            return False

        return True
