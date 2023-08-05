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
import struct
from os import PathLike
from typing import TypeVar, Union

from duniterpy.key import SigningKey
from duniterpy.key.scrypt_params import ScryptParams
from pyaes import AESModeOfOperationECB

DEWIF_CURRENCY_CODE_NONE = 0x00000000
DEWIF_CURRENCY_CODE_G1 = 0x00000001
DEWIF_CURRENCY_CODE_G1_TEST = 0x10000001
DEWIF_ALGORITHM_CODE_ED25519 = 0x00
DEWIF_ALGORITHM_CODE_BIP32_ED25519 = 0x01


def chunkstring(data: bytes, length: int):
    """
    Return a tuple of chunks sized at length from the data bytes

    :param data: Data to split
    :param length: Size of  chunks
    :return:
    """
    return (data[0 + i : length + i] for i in range(0, len(data), length))


TikkaSigningKeyType = TypeVar("TikkaSigningKeyType", bound="TikkaSigningKey")


class TikkaSigningKey(SigningKey):
    @classmethod
    def from_dubp_mnemonic(cls, mnemonic: str, scrypt_params: ScryptParams = None):
        """
        Generate key pair instance from a DUBP mnemonic passphrase

        :param mnemonic: Passphrase generated from a mnemonic algorithm
        :param scrypt_params: ScryptParams instance (default=None)
        :return:
        """
        if scrypt_params is None:
            scrypt_params = ScryptParams()

        _password = mnemonic.encode("utf-8")  # type: bytes
        _salt = hashlib.sha256(b"dubp" + _password).digest()  # type: bytes
        _seed = hashlib.scrypt(
            password=_password,
            salt=_salt,
            n=scrypt_params.N,  # 4096
            r=scrypt_params.r,  # 16
            p=scrypt_params.p,  # 1
            dklen=scrypt_params.seed_length,  # 32
        )  # type: bytes
        return cls(_seed)

    @classmethod
    def from_dewif_file(
        cls, path: Union[str, PathLike], password: str
    ) -> TikkaSigningKeyType:
        """
        Load a DEWIF encrypted file using the password to decrypt

        Add dewif_version and dewif_currency properties to the instance

        :param path: Path of the file
        :param password: Password to decrypt the file
        :return:
        """
        scrypt_params = ScryptParams()
        aes_key = hashlib.scrypt(
            password=password.encode("utf-8"),
            salt=hashlib.sha256(f"dewif{password}".encode("utf-8")).digest(),
            n=scrypt_params.N,  # 4096
            r=scrypt_params.r,  # 16
            p=scrypt_params.p,  # 1
            dklen=scrypt_params.seed_length,  # 32
        )
        aes = AESModeOfOperationECB(aes_key)

        with open(path, "rb") as file_handler:
            file_handler.seek(8)
            # header = file_handler.read(8)
            # version, currency = struct.unpack("ii", header)
            encrypted_data = file_handler.read()

        data = b"".join(map(aes.decrypt, chunkstring(encrypted_data, 16)))

        seed = data[:32]
        public_key = data[32:]
        signing_key = cls(seed)
        assert signing_key.vk == public_key

        return signing_key

    def save_dewif_v1_file(
        self,
        path: Union[str, PathLike],
        password: str,
        currency: int = DEWIF_CURRENCY_CODE_G1,
    ) -> None:
        """
        Save the instance seed in an encrypted DEWIF V1 file
        Use the password to encrypt data

        :param path: Path of the file to save
        :param password: Password to encrypt data
        :param currency: Currency code (default=tikka.domain.dewif.DEWIF_CURRENCY_CODE_G1)
        :return:
        """
        scrypt_params = ScryptParams()
        aes_key = hashlib.scrypt(
            password=password.encode("utf-8"),
            salt=hashlib.sha256(f"dewif{password}".encode("utf-8")).digest(),
            n=scrypt_params.N,  # 4096
            r=scrypt_params.r,  # 16
            p=scrypt_params.p,  # 1
            dklen=scrypt_params.seed_length,  # 32
        )
        header = struct.pack(">ii", 1, currency)
        data = self.seed + self.vk

        aes = AESModeOfOperationECB(aes_key)
        encrypted_data = b"".join(map(aes.encrypt, chunkstring(data, 16)))

        with open(path, "wb") as file_handler:
            file_handler.write(header + encrypted_data)
