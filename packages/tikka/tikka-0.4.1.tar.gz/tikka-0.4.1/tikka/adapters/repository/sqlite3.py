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

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, List

from yoyo import get_backend, read_migrations

from tikka.domains.entities.constants import (
    CURRENCIES,
    DATABASE_FILE_EXTENSION,
    DATABASE_MIGRATIONS_PATH,
)


class Sqlite3Client:
    """
    Database abstraction class

    """

    path: Path

    def __init__(self, connection_name: str, path: Path):
        """
        Init a Database adapter instance

        :param connection_name: Name of connection
        :param path: Path to database data
        """
        self.path = path

        # update database
        self.migrate()

        db_path = self.path.joinpath(
            f"{connection_name}{DATABASE_FILE_EXTENSION}"
        ).expanduser()
        self.connection = sqlite3.connect(str(db_path))

    def close(self):
        """
        Close connection

        :return:
        """
        # Closing the connection
        self.connection.close()

    def insert(self, table: str, **kwargs):
        """
        Create a new entry in table, with field=value kwargs

        :param table: Table name
        :param kwargs: fields with their values
        :return:
        """
        # Creating a cursor object using the cursor() method
        cursor = self.connection.cursor()
        fields_string = ",".join(kwargs.keys())
        values_string = ",".join(["?" for _ in range(len(kwargs))])
        filtered_values = []
        for value in kwargs.values():
            # serialize dict to json string
            filtered_values.append(
                json.dumps(value) if isinstance(value, dict) else value
            )

        sql = f"INSERT INTO {table} ({fields_string}) VALUES ({values_string})"
        try:
            cursor.execute(sql, filtered_values)
        except Exception as exception:
            logging.exception(exception)
            raise
        try:
            self.connection.commit()
        except Exception as exception:
            logging.exception(exception)
            raise

    def select(self, sql: str, *args: Any) -> List[tuple]:
        """
        Execute SELECT sql query

        :param sql: SELECT query
        :return:
        """
        # Creating a cursor object using the cursor() method
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, args)
        except Exception as exception:
            logging.exception(exception)
            raise
        return cursor.fetchall()

    def select_one(self, sql: str, *args: Any) -> tuple:
        """
        Execute SELECT sql query and return first result

        :param sql: SELECT query
        :return:
        """
        # Creating a cursor object using the cursor() method
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, args)
        except Exception as exception:
            logging.exception(exception)
            raise
        return cursor.fetchone()

    def update(self, table: str, where: str, **kwargs):
        """
        Update rows of table selected by where from **kwargs

        :param table: Table name
        :param where: WHERE statement
        :param kwargs: field=values kwargs
        :return:
        """
        set_statement = ",".join([f"{field}=?" for field in kwargs])

        sql = f"UPDATE {table} SET {set_statement} WHERE {where}"
        values = list(kwargs.values())

        self._update(sql, values)

    def _update(self, sql: str, values: list):
        """
        Send update request sql with values

        :param sql: SQL query
        :param values: Values to inject as sql params
        :return:
        """
        filtered_values = []
        for value in values:
            # serialize dict to json string
            filtered_values.append(
                json.dumps(value) if isinstance(value, dict) else value
            )

        # Creating a cursor object using the cursor() method
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, filtered_values)
        except Exception as exception:
            logging.exception(exception)
            raise
        try:
            self.connection.commit()
        except Exception as exception:
            logging.exception(exception)
            raise

    def delete(self, table: str, **kwargs):
        """
        Delete a row from table where key=value (AND) from kwargs

        :param table: Table to delete from
        :param kwargs: Key/Value conditions (AND)
        :return:
        """
        # Creating a cursor object using the cursor() method
        cursor = self.connection.cursor()
        conditions = " AND ".join([f"{key}=?" for key in kwargs])

        sql = f"DELETE FROM {table} WHERE {conditions}"
        try:
            cursor.execute(sql, list(kwargs.values()))
        except Exception as exception:
            logging.exception(exception)
            raise
        try:
            self.connection.commit()
        except Exception as exception:
            logging.exception(exception)
            raise

    def clear(self, table: str):
        """
        Clear table entries

        :param table: Name of the table
        :return:
        """
        # Creating a cursor object using the cursor() method
        cursor = self.connection.cursor()
        try:
            # delete all entries
            cursor.execute(f"DELETE FROM {table}")
        except Exception as exception:
            logging.exception(exception)
            raise
        try:
            self.connection.commit()
        except Exception as exception:
            logging.exception(exception)
            raise
        try:
            # clear unused space
            cursor.execute("VACUUM")
        except Exception as exception:
            logging.exception(exception)
            raise

    def migrate(self):
        """
        Use Python library to handle database migrations

        :return:
        """
        migrations_path = str(
            Path(__file__).parent.parent.joinpath(DATABASE_MIGRATIONS_PATH).expanduser()
        )
        migrations = read_migrations(migrations_path)

        for currency_code in CURRENCIES.keys():
            sqlite_file_path = self.path.joinpath(
                f"{currency_code}{DATABASE_FILE_EXTENSION}"
            ).expanduser()
            backend = get_backend("sqlite:///" + str(sqlite_file_path))
            with backend.lock():
                # Apply any outstanding migrations
                backend.apply_migrations(backend.to_apply(migrations))
                logging.debug(backend.applied_migrations_sql)


class NoConnectionError(Exception):
    pass
