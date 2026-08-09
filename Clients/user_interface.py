'''
Author: Anthony Wong
Email: Anw2727@gmail.com
A general user interface for all clients to use. 
This is the main entry point for the program.

###TODO make this a GUI instead of a CLI.
'''

import time
import datetime
from Clients.Amazon import AWS_client
from Clients.Azure import Azure_client

def collect_data():
    '''
    Collects data from the client and makes the user choose the type of
    cloud they are using and how often they want the auditor to run.
    '''
    type_of_cloud = input("Please enter the type of cloud you are using (1. AWS, 2. Azure, 3. GCP): ")
    frequency = input("Please enter how often you want the auditor to run (1. daily, 2. weekly, 3. monthly): ")
    return type_of_cloud, frequency

def schedule_auditor(frequency):
    '''
    Schedules the auditor to run at the specified frequency.
    '''
    current_time = datetime.datetime.now()

    if frequency == "1":
        print("Auditor will run daily.")
        current_time = current_time + datetime.timedelta(days=1)
    elif frequency == "2":
        print("Auditor will run weekly.")
        current_time = current_time + datetime.timedelta(weeks=1)
    elif frequency == "3":
        print("Auditor will run monthly.")
        current_time = current_time + datetime.timedelta(days=30)
    else:
        print("Invalid input. Please enter a valid option.")

    return current_time

def execute_auditor(type_of_cloud):
    '''
    Executes the auditor for the specified cloud type.
    '''
    if type_of_cloud == "1":
        AWS_client.main()
    elif type_of_cloud == "2":
        Azure_client.main()
    elif type_of_cloud == "3":
        print("GCP client is not yet implemented.")
    else:
        print("Invalid input. Please enter a valid option.")

def main():
    '''
    Main function that runs the program.
    '''
    type_of_cloud, frequency = collect_data()
    execute_auditor(type_of_cloud)
    next_run = schedule_auditor(frequency)
    while True:
        current_time = datetime.datetime.now()
        if current_time >= next_run:
            execute_auditor(type_of_cloud)
            next_run = schedule_auditor(frequency)
        time.sleep(120)  # Check every 2 minutes
    
    


if __name__ == "__main__":
    main()