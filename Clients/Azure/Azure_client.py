'''
Author: Anthony Wong
Email: Anw2727@gmai.com
creates a table in a sqlite3 database for the user to store their Azure inventory data.
'''

from contextlib import closing
import sqlite3
from . import Azure_Mock_Data_Gen as data

def create_table(data):
    '''
    Takes the flat list containing a dictionary with all the data
    and creates a new table for the user using sqlite3.
    '''
    file = sqlite3.connect("Azure_Inventory.db")
    try:
        with closing(file.cursor()) as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Azure_Inventory (
                    resource_id TEXT PRIMARY KEY,
                    resource_type TEXT,
                    status TEXT,
                    time_created TEXT,
                    owner_tag TEXT,
                    project_tag TEXT
                )
            ''')
            for row in data:
                if row["status"] == "running":
                    cursor.execute('''
                        INSERT OR REPLACE INTO Azure_Inventory (resource_id, resource_type, status, time_created, owner_tag, project_tag)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (row["resource_id"], row["resource_type"], row["status"], row["launch_time"], row["owner_tag"], row["project_tag"]))
            file.commit()
    finally:
        file.close()

mock_response = data.get_mock_azure_vms()
parsed_data = data.parse_azure(mock_response)
create_table(parsed_data)