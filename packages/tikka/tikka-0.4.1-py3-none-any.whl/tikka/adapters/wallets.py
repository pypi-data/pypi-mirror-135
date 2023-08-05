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
from pathlib import Path
from typing import Optional, Union

from tikka.domains.entities.signing_key import (
    DEWIF_CURRENCY_CODE_G1,
    DEWIF_CURRENCY_CODE_G1_TEST,
    TikkaSigningKey,
)
from tikka.domains.entities.wallet import Wallet
from tikka.domains.interfaces.wallets import WalletsInterface


class FileWallets(WalletsInterface):
    """
    Class to deal with file wallets
    """

    def load(self, path: Union[str, Path], password: Optional[str] = None) -> Wallet:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            WalletsInterface.load.__doc__
        )
        if isinstance(path, str):
            path = Path(path)

        type_ = self.get_type(path)
        is_encrypted = type_ in ("EWIF", "DEWIF")
        signing_key = None
        if not is_encrypted:
            if type_ == "WIF":
                signing_key_ = TikkaSigningKey.from_wif_file(str(path))  # type: ignore
                signing_key = TikkaSigningKey(signing_key_.seed)
            elif type_ == "PUBSEC":
                signing_key_ = TikkaSigningKey.from_pubsec_file(
                    str(path)
                )  # mypy: ignore
                signing_key = TikkaSigningKey(signing_key_.seed)
        elif password is not None:
            if type_ == "EWIF":
                signing_key_ = TikkaSigningKey.from_ewif_file(
                    str(path), password
                )  # type: ignore
                signing_key = TikkaSigningKey(signing_key_.seed)
            elif type_ == "DEWIF":
                signing_key = TikkaSigningKey.from_dewif_file(str(path), password)

        return Wallet(path, type_, is_encrypted, signing_key)

    def save(self, wallet: Wallet, password: str, currency: str) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            WalletsInterface.save.__doc__
        )
        if wallet.signing_key is None:
            raise ValueError("Wallet.signing_key should not be None")

        if Path(wallet.path).suffix == ".dewif":
            if currency == "g1":
                currency_code = DEWIF_CURRENCY_CODE_G1
            else:
                currency_code = DEWIF_CURRENCY_CODE_G1_TEST

            # save dewif wallet file
            wallet.signing_key.save_dewif_v1_file(wallet.path, password, currency_code)
        else:
            # save ewif wallet file
            wallet.signing_key.save_ewif_file(str(wallet.path), password)

    @staticmethod
    def get_type(path: Union[str, Path]) -> str:
        """
        Get format type of the file

        :param path: Path instance or string of the file
        :return:
        """
        if isinstance(path, str):
            path = Path(path)

        if path.suffix == ".dewif":
            type_ = "DEWIF"

        if path.suffix == ".dunikey":
            with path.open("r", encoding="utf-8") as file_handle:
                _type = file_handle.readline().strip()

                if "Type: EWIF" in _type:
                    type_ = "EWIF"
                elif "Type: WIF" in _type:
                    type_ = "WIF"
                elif "Type: PubSec" in _type:
                    type_ = "PUBSEC"

        return type_
