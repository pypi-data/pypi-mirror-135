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

import hashlib
import re
from typing import Type, TypeVar

import base58
from duniterpy.constants import PUBKEY_REGEX

# required to type hint cls in classmethod
PublicKeyType = TypeVar("PublicKeyType", bound="PublicKey")


class PublicKey:
    """
    Class to handle base58 public key and checksum
    """

    re_checksum_pubkey = re.compile(f"({PUBKEY_REGEX}):([A-Za-z0-9]{{3}})")

    def __init__(self, pubkey: str, checksum: str) -> None:
        """
        Creates a pubkey with a checksum

        :param pubkey: Public key
        :param checksum: Checksum
        """
        self.checksum = checksum

        try:
            self.binary = self.get_binary_from_base58(pubkey)
        except ValueError as e:
            raise PubkeyNotValid(f"Invalid base58 public key {pubkey}") from e

        self.base58 = base58.b58encode(self.binary).decode("utf-8")

        if not self.pubkey_is_valid():
            raise PubkeyNotValid(f"Invalid base58 public key {pubkey}")
        if not self.checksum_is_valid():
            raise PubkeyChecksumNotValid(
                f"Invalid checksum {self.checksum} for key {pubkey}"
            )

    @staticmethod
    def get_binary_from_base58(base58_: str) -> bytearray:
        """
        Set self.binary from base58_

        See RFC 0016: https://git.duniter.org/documents/rfcs/-/blob/master/rfc/0016_public_key_checksum.md

        :param base58_: Public key in base58
        :return:
        """
        # convert public key string to bytes
        pubkey_byte = bytearray(base58.b58decode(base58_))

        # prepend zero-bytes until the public key is 32 bytes long
        while len(pubkey_byte) < 32:
            pubkey_byte = bytearray(b"\x00") + pubkey_byte

        # remove leading zero-bytes if length is superior to 32
        while len(pubkey_byte) > 32:
            if pubkey_byte[0] == 0:
                del pubkey_byte[0]
            # raise error if leading byte is not null
            else:
                raise PubkeyNotValid("Invalid public key: bytes length is too long")

        return pubkey_byte

    @staticmethod
    def calculate_checksum(base58_: str) -> str:
        """
        Return the first three characters of pubkey checksum

        See RFC 0016: https://git.duniter.org/documents/rfcs/-/blob/master/rfc/0016_public_key_checksum.md

        :param base58_: Base58 public key
        :return:
        """
        try:
            sha256_checksum = hashlib.sha256(base58.b58decode(base58_))
        except ValueError as e:
            raise PubkeyNotValid(e) from e

        b58_checksum = base58.b58encode(sha256_checksum.digest())

        return b58_checksum[0:3].decode("utf-8")

    @classmethod
    def from_pubkey_with_checksum(
        cls: Type[PublicKeyType], pubkey_checksum: str
    ) -> PublicKeyType:
        """
        Return PublicKey instance from public_key:checksum string

        :param pubkey_checksum: Public key with checksum
        :return:
        """
        pubkey, checksum = pubkey_checksum.split(":", 2)
        return cls(pubkey, checksum)

    @classmethod
    def from_pubkey(cls: Type[PublicKeyType], pubkey: str) -> PublicKeyType:
        """
        Return PublicKey instance from public key string

        :param pubkey: Public key
        :return:
        """
        checksum = cls.calculate_checksum(pubkey)
        return cls(pubkey, checksum)

    def pubkey_is_valid(self) -> bool:
        """
        Return True if base58 pubkey is valid

        :return:
        """
        re_pubkey = re.compile(PUBKEY_REGEX)

        data = re_pubkey.match(self.base58)
        return data is not None

    def checksum_is_valid(self) -> bool:
        """
        Return True if checksum is valid

        :return:
        """
        return self.calculate_checksum(self.base58) == self.checksum

    @property
    def shorten(self) -> str:
        """
        Return a shorten version of public key (first 4 and last 4 characters)

        :return:
        """
        return f"{self.base58[0:4]}…{self.base58[-4:]}"

    @property
    def shorten_checksum(self) -> str:
        """
        Return a shorten version of public key (8 characters) + checksum

        :return:
        """
        return f"{self.shorten}:{self.checksum}"

    def __str__(self) -> str:
        """
        Return string representation of instance

        :return:
        """
        return f"{self.base58}:{self.checksum}"

    def __eq__(self, other) -> bool:
        """
        Test PublicKey equality

        :param other: Other PublicKey instance
        :return:
        """
        if not isinstance(other, PublicKey):
            return False

        if self.base58 == other.base58:
            return True

        return False

    def __hash__(self):
        return self.base58


class PubkeyNotValid(Exception):
    pass


class PubkeyChecksumNotValid(Exception):
    pass
