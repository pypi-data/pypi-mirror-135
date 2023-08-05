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

from typing import List

from tikka.adapters.repository.sqlite3 import Sqlite3Client
from tikka.domains.entities.account import TABLE_NAME, Account
from tikka.domains.interfaces.repository.accounts import AccountRepositoryInterface


class Sqlite3AccountRepository(AccountRepositoryInterface):
    """
    Sqlite3AccountRepository class
    """

    def __init__(self, client: Sqlite3Client) -> None:
        """
        Init Sqlite3AccountRepository instance with sqlite3 client

        :param client: Sqlite3Client instance
        :return:
        """
        self.client = client

    def list(self) -> List[Account]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountRepositoryInterface.list.__doc__
        )

        result_set = self.client.select("SELECT * FROM accounts")

        list_ = []
        for row in result_set:
            list_.append(Account(*row))

        return list_

    def unselect_all(self) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountRepositoryInterface.unselect_all.__doc__
        )

        self.client.update(TABLE_NAME, "1", selected=False)

    def add(self, account: Account) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountRepositoryInterface.add.__doc__
        )

        # insert only non hidden fields
        self.client.insert(
            TABLE_NAME,
            **{
                key: value
                for (key, value) in account.__dict__.items()
                if not key.startswith("_")
            },
        )

    def update(self, account: Account) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountRepositoryInterface.update.__doc__
        )

        # update only non hidden fields
        self.client.update(
            TABLE_NAME,
            f"pubkey='{account.pubkey}'",
            **{
                key: value
                for (key, value) in account.__dict__.items()
                if not key.startswith("_")
            },
        )

    def delete(self, account: Account) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountRepositoryInterface.delete.__doc__
        )

        self.client.delete(TABLE_NAME, pubkey=account.pubkey)
