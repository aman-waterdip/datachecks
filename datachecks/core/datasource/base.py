#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from abc import ABC
from sqlite3 import Connection
from typing import Any, Dict, Union

from sqlalchemy import text


class DataSource(ABC):
    """
    Abstract class for data sources
    """

    def __init__(self, data_source_name: str, data_connection: Dict):
        self.data_source_name: str = data_source_name
        self.data_connection: Dict = data_connection

    def connect(self) -> Any:
        """
        Connect to the data source
        """
        raise NotImplementedError("connect method is not implemented")

    def is_connected(self) -> bool:
        """
        Check if the data source is connected
        """
        raise NotImplementedError("is_connected method is not implemented")


class SearchIndexDataSource(DataSource):
    """
    Abstract class for search index data sources
    """

    def __init__(self, data_source_name: str, data_connection: Dict):
        super().__init__(data_source_name, data_connection)

        self.client = None

    def query_get_document_count(self, index_name: str, filter: str = None) -> int:
        """
        Get the document count
        :param index_name: name of the index
        :param filter: optional filter
        :return: count of documents
        """
        raise NotImplementedError("query_get_document_count method is not implemented")

    def query_get_max(self, index_name: str, field: str, filter: str = None) -> int:
        """
        Get the max value
        :param index_name: name of the index
        :param field: field name
        :param filter: optional filter
        :return: max value
        """
        raise NotImplementedError("query_get_max method is not implemented")


class SQLDatasource(DataSource):
    """
    Abstract class for SQL data sources
    """

    def __init__(self, data_source_name: str, data_source_properties: Dict):
        super().__init__(data_source_name, data_source_properties)

        self.connection: Union[Connection, None] = None

    def is_connected(self) -> bool:
        """
        Check if the data source is connected
        """
        return self.connection is not None

    def query_get_row_count(self, table: str, filter: str = None) -> int:
        """
        Get the row count
        :param table: name of the table
        :param filter: optional filter
        """
        query = "SELECT COUNT(*) FROM {}".format(table)
        if filter:
            query += " WHERE {}".format(filter)

        return self.connection.execute(text(query)).fetchone()[0]

    def query_get_max(self, table: str, field: str, filter: str = None) -> int:
        """
        Get the max value
        :param table: table name
        :param field: column name
        :param filter: filter condition
        :return:
        """
        query = "SELECT MAX({}) FROM {}".format(field, table)
        if filter:
            query += " WHERE {}".format(filter)

        return self.connection.execute(text(query)).fetchone()[0]
