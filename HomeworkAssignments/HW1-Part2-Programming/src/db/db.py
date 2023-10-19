from typing import Any, Dict, List, Tuple, Union

import pymysql

KV = Dict[str, Any]
Query = Tuple[str, List]

class DB:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.conn = conn

    def get_cursor(self):
        return self.conn.cursor()
    
    def execute_query(self, query: str, args: List, ret_result: bool) -> Union[List[KV], int]:
        """Executes a query.

        :param query: A query string, possibly containing %s placeholders
        :param args: A list containing the values for the %s placeholders
        :param ret_result: If True, execute_query returns a list of dicts, each representing a returned
                           row from the table. If False, the number of rows affected is returned. Note
                           that the length of the list of dicts is not necessarily equal to the number
                           of rows affected.
        :returns: a list of dicts or a number, depending on ret_result
        """
        cur = self.get_cursor()
        count = cur.execute(query, args=args)
        if ret_result:
            return cur.fetchall()
        else:
            return count

    # TODO: all methods below

    @staticmethod
    def build_select_query(table: str, filters: KV) -> Query:
        """Builds a query that selects rows. See db_test for examples.

        :param table: The table to be selected from
        :param filters: Key-value pairs that the rows from table must satisfy
        :returns: A query string and any placeholder arguments
        """
        if not filters:
            return f"SELECT * FROM {table}", []
        keywords = " AND ".join([f"{keyword} = %s" for keyword in filters.keys()])
        args = list(filters.values())
        return f"SELECT * FROM {table} WHERE " + keywords, args

    def select(self, table: str, filters: KV) -> List[KV]:
        """Runs a select statement. You should use build_select_query and execute_query.

        :param table: The table to be selected from
        :param filters: Key-value pairs that the rows to be selected must satisfy
        :returns: The selected rows
        """
        query, args = self.build_select_query(table, filters)
        return self.execute_query(query, args, ret_result=True)

    @staticmethod
    def build_insert_query(table: str, values: KV) -> Query:
        """Builds a query that inserts a row. See db_test for examples.

        :param table: The table to be inserted into
        :param values: Key-value pairs that represent the values to be inserted
        :returns: A query string and any placeholder arguments
        """
        keys = ", ".join(values.keys())
        placeholders = ", ".join([r"%s" for _ in values])
        args = list(values.values())
        return f"INSERT INTO {table} (" + keys + ") VALUES (" + placeholders + ")", args

    def insert(self, table: str, values: KV) -> int:
        """Runs an insert statement. You should use build_insert_query and execute_query.

        :param table: The table to be inserted into
        :param values: Key-value pairs that represent the values to be inserted
        :returns: The number of rows affected
        """
        query, args = self.build_insert_query(table, values)
        return self.execute_query(query, args, ret_result=False)

    @staticmethod
    def build_update_query(table: str, values: KV, filters: KV) -> Query:
        """Builds a query that updates rows. See db_test for examples.

        :param table: The table to be updated
        :param values: Key-value pairs that represent the new values
        :param filters: Key-value pairs that the rows from table must satisfy
        :returns: A query string and any placeholder arguments
        """
        value_keys = ", ".join([f"{val} = %s" for val in values])
        args = list(values.values())
        if not filters:
            return f"UPDATE {table} SET " + value_keys, args
        filter_keys = " AND ".join([f"{fil} = %s" for fil in filters])
        args.extend(filters.values())
        return f"UPDATE {table} SET " + value_keys + " WHERE " + filter_keys, args

    def update(self, table: str, values: KV, filters: KV) -> int:
        """Runs an update statement. You should use build_update_query and execute_query.

        :param table: The table to be updated
        :param values: Key-value pairs that represent the new values
        :param filters: Key-value pairs that the rows to be updated must satisfy
        :returns: The number of rows affected
        """
        query, args = self.build_update_query(table, values, filters)
        return self.execute_query(query, args, ret_result=False)

    @staticmethod
    def build_delete_query(table: str, filters: KV) -> Query:
        """Builds a query that deletes rows. See db_test for examples.

        :param table: The table to be deleted from
        :param filters: Key-value pairs that the rows to be deleted must satisfy
        :returns: A query string and any placeholder arguments
        """
        if not filters:
            return f"DELETE FROM {table}", []
        keywords = " AND ".join([f"{keyword} = %s" for keyword in filters.keys()])
        args = list(filters.values())
        return f"DELETE FROM {table} WHERE " + keywords, args

    def delete(self, table: str, filters: KV) -> int:
        """Runs a delete statement. You should use build_delete_query and execute_query.

        :param table: The table to be deleted from
        :param filters: Key-value pairs that the rows to be deleted must satisfy
        :returns: The number of rows affected
        """
        query, args = self.build_delete_query(table, filters)
        return self.execute_query(query, args, ret_result=False)
