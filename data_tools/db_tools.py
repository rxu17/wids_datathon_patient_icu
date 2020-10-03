
'''
Description: General commmon db tools used throughout
data pipeline
How To Use: import db_tools and call functions
Contributors: rxu17
'''

import sqlite3
import getpass
from datetime import datetime
from contextlib import closing
from sqlalchemy import create_engine


def get_default_settings():
    ''' Returns: dict,
            default time columns to be included with data to be uploaded
    '''
    return{'date_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
           'updated_by': getpass.getuser()}


def get_connect_cursor(db_name):
    '''
        Args: db_name - str, 
                    name of database
        Returns: Connection obj
    '''
    user = getpass.getuser()
    connection = sqlite3.connect("/Users/{}/{}".format(user, db_name))
    return(connection)


def run_query(connection, query):
    ''' Args: 
            connection - Connection object, 
                            name of database
            query - str,
                    SQL query to be run
        Returns: None
    '''
    with closing(connection) as connection:
        with closing(connection.cursor()) as cursor:
            if "SELECT" in query:
                rows = cursor.execute(query).fetchall()
                return(rows)
            elif q_type == "result":
                cursor.execute(query)
                return()


def get_table(connection, table):
    ''' Retrieves database table

        Args: 
            connection - Connection object, 
                            name of database
            table - str,
                        name of table to retrieve
        Returns: DataFrame,
                    queried database table
    '''
    with closing(connection) as connection:
        with closing(connection.cursor()) as cursor:
            query = "SELECT * FROM {};".format(table)
            table = cursor.execute(query).fetchall()
            print("Table fetched!")
            return(table)


def delete_table(connection, table):
    '''
    '''
    with closing(connection) as connection:
        with closing(connection.cursor()) as cursor:
            query = "DROP TABLE {};".format(table)
            cursor.execute(query)
            print("Table deleted!")


def upload_data(connection, df, table, action):
    ''' Uploads data frame to database table

        Args: 
            df - DataFrame,
                        dataframe object to be uploaded
            table - str,
                        name of table to upload to
            action - str, ['update', 'replace']
                        add to table or replace
    '''
    # add get_default_settings
    settings = get_default_settings()
    df.assign(**settings)
    if action == "update":
        df.to_sql(table, connection, if_exists='append', index=False)    
    elif action == "replace":
        df.to_sql(table, connection, if_exists='replace', index=False)