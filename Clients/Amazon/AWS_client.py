# Project_Alpha - A cost reducing program for AWS services.
from . import AWS_Mock_Data_Gen as data
from contextlib import closing
import sqlite3

def create_table(data):
    '''
    Takes the flat list containing a dictionary with all the data
    and creates a new table for the user using sqlite3.
    '''
    file = sqlite3.connect("AWS_Inventory.db")
    try:
        with closing(file.cursor()) as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS AWS_Inventory (
                    resource_id TEXT PRIMARY KEY,
                    resource_type TEXT,
                    status TEXT,
                    launch_time TEXT,
                    owner_tag TEXT,
                    project_tag TEXT
                )
            ''')
            for row in data:
                if row["status"] == "running":
                    cursor.execute('''
                        INSERT OR REPLACE INTO AWS_Inventory (resource_id, resource_type, status, launch_time, owner_tag, project_tag)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (row["resource_id"], row["resource_type"], row["status"], row["launch_time"], row["owner_tag"], row["project_tag"]))
            file.commit()
    finally:
        file.close()

mock_response = data.mock_ec2_instance()
parsed_data = data.parse_aws(mock_response)
create_table(parsed_data)