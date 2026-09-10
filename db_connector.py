"""
Database connection manager for StrongHold.
Keeps one persistent connection to MySQL alive, with automatic
reconnection if the connection drops. Every sensor/module goes
through this class instead of talking to pymysql directly.
"""
import pymysql
import pymysql.cursors
from typing import Optional

from config import Config


class DBConnector:
    """
    Manages the connection to MySQL for StrongHold.
    """

    def __init__(self):
        self._connection: Optional[pymysql.connections.Connection] = None

    def connect(self) -> pymysql.connections.Connection:
        """
        Opens a new connection to MySQL using the parameters from Config.
        Raises a clear error instead of letting the program crash with a
        raw traceback if the connection fails.
        """
        params = Config.get_db_connection_params()

        try:
            connection = pymysql.connect(
                host=params['host'],
                user=params['user'],
                password=params['password'],
                database=params['database'],
                port=params['port'],
                autocommit=params['autocommit'],
                connect_timeout=params['connect_timeout'],
                charset=params['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f" Connected to MySQL at {params['host']}:{params['port']} / {params['database']}")
            return connection

        except pymysql.err.OperationalError as e:
            print(
                f" Connection error: {e}\n"
                f"Possible causes:\n"
                f"  - MySQL container not running (check: docker ps)\n"
                f"  - Wrong host/port/database name in .env\n"
                f"  - MySQL not fully started yet (wait a few seconds)"
            )
            raise

    def get_connection(self) -> pymysql.connections.Connection:
        """
        Returns a live connection. Opens one if it doesn't exist yet,
        or reconnects automatically if the existing one has dropped.
        Every sensor should call this each time it needs to run a
        query — don't hold onto the connection object yourself.
        """
        if self._connection is None:
            self._connection = self.connect()
            return self._connection

        try:
            self._connection.ping(reconnect=True)
        except pymysql.err.OperationalError:
            self._connection = self.connect()

        return self._connection

    def close(self) -> None:
        """
        Closes the connection cleanly. Call this when the program
        is shutting down.
        """
        if self._connection is not None:
            try:
                self._connection.close()
                print(" MySQL connection closed.")
            except pymysql.err.Error:
                pass
            finally:
                self._connection = None


# ============ QUICK TEST (optional) ============
if __name__ == "__main__":
    connector = DBConnector()
    try:
        conn = connector.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION() AS version;")
            result = cursor.fetchone()
            print(f" MySQL version: {result['version']}")
    finally:
        connector.close()
