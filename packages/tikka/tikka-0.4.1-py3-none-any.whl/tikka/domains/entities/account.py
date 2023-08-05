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

from dataclasses import dataclass
from typing import Optional, TypeVar

from tikka.domains.entities.pubkey import PublicKey
from tikka.domains.entities.signing_key import TikkaSigningKey

AccountType = TypeVar("AccountType", bound="Account")

TABLE_NAME = "accounts"


@dataclass
class Account:

    pubkey: str
    uid: Optional[str] = None
    selected: bool = True
    access_type: Optional[str] = None
    _signing_key: Optional[TikkaSigningKey] = None
    _entropy: Optional[bytearray] = None

    @property
    def signing_key(self) -> Optional[TikkaSigningKey]:
        """
        SigningKey instance getter

        :return:
        """
        return self._signing_key

    @signing_key.setter
    def signing_key(self, signing_key: TikkaSigningKey):
        """
        SigningKey instance setter

        :param signing_key: SigningKey instance
        :return:
        """
        self._signing_key = signing_key

    @property
    def entropy(self) -> Optional[bytearray]:
        """
        entropy getter

        :return:
        """
        return self._entropy

    @entropy.setter
    def entropy(self, entropy: bytearray):
        """
        entropy setter

        :param entropy: Entropy as bytes
        :return:
        """
        self._entropy = entropy

    def __str__(self):
        """
        Return string representation

        :return:
        """
        if self.uid:
            return f"{PublicKey.from_pubkey(self.pubkey)} - {self.uid}"
        return f"{PublicKey.from_pubkey(self.pubkey)}"

    def __eq__(self, other):
        """
        Test equality on pubkey

        :param other: Account instance
        :return:
        """
        if not isinstance(other, self.__class__):
            return False
        return other.pubkey == self.pubkey

    def __hash__(self):
        return hash(self.pubkey)
