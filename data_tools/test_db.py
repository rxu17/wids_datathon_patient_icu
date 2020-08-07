import os
import unittest
import sqlite3
import getpass
import datetime
from unittest import TestCase
from mock import patch
import utils
import db_tools as dbt

# ideas:

class TestDB(TestCase):
    @classmethod
    def setUpClass(self):
        conn = dbt.get_connect_cursor(db_name)
        cursor = conn.cursor()

        try:
            cursor.execute("DROP DATABASE {}".format(db_name))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(db_name, err))

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    '''
    @mock.patch('mymodule.os')
    def test_fields(self, mock_os):
        rm("any path")
        # test that rm called os.remove with the right parameters
        mock_os.remove.assert_called_with("any path")
    '''

    @classmethod
    def tearDownClass(cls):
        conn = dbt.get_connect_cursor("")
        cursor = conn.cursor()

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        cnx.close()


if __name__ == '__main__':
    unittest.main()