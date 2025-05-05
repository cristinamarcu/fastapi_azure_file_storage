import pyodbc
from secrets_connections import *


class AzureDatabaseAccessor():

    def __init__(self,connection_string_mysql):
        self.connection_string_mysql=connection_string_mysql
 
    def insert_new_file_database(self,owner_name, file_name, file_size):
        try:
            with pyodbc.connect(self.connection_string_mysql) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO Files_Info (OwnerName, FileName, FileSize) VALUES (?, ?, ?)""",
                        owner_name,
                        file_name,
                        file_size,
                    )
                    conn.commit()
            return True

        except Exception as e:
            print(e)
            return False
        

    def check_file_exists_database(self,owner_name, file_name):
        with pyodbc.connect(self.connection_string_mysql) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM Files_Info WHERE OwnerName=? AND FileName=?;""",
                    owner_name,
                    file_name,
                )
                row = cursor.fetchone()

        if row:
            return True
        else:
            return False
        
    
    def delete_file_from_database(self,owner_name, file_name):
        try:
            with pyodbc.connect(self.connection_string_mysql) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM Files_Info WHERE OwnerName=? and FileName=?;""",
                        owner_name,
                        file_name,
                    )
                    conn.commit()
            return True

        except Exception as e:
            print(e)
            return False
