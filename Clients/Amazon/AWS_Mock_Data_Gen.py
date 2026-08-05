# Author: Anthony Wong
# Email: Anw2727@gmail.com
# Mock Data Generator
import datetime

def mock_ec2_instance():
    '''
    Simulates the boto3 client.describe_instances() response.
    Returns a native Python dictionary matching the AWS structure.
    '''
    return {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-0abcd1234efgh5678",
                        "InstanceType": "t3.micro",
                        "State": {"Name": "running"},
                        "LaunchTime": datetime.datetime(2026, 7, 28, 14, 30, 0),
                        "Tags": [
                            {"Key": "Owner", "Value": "DataTeam"},
                            {"Key": "Project", "Value": "CloudAuditor"}
                        ]
                    },
                    {
                        "InstanceId": "i-0987654321fedcba0",
                        "InstanceType": "m5.large",
                        "State": {"Name": "stopped"},
                        "LaunchTime": datetime.datetime(2026, 6, 15, 9, 0, 0),
                        "Tags": [
                            {"Key": "Project", "Value": "LegacyApp"}
                        ]
                    }
                ]
            }
        ]
    }


def parse_aws(mock_response):
    '''
    Parses the nested dictionary provided by boto3 into a flat list
    that can be used by SQL database.
    '''

    inventory_rows = []

    for reservation in mock_response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            # extracting data
            instance_id = instance.get("InstanceId")
            status = instance.get("State", {}).get("Name")
            launch_time = instance.get("LaunchTime")
            raw_tag = instance.get("Tags")
            dict_tag = {tag["Key"]: tag["Value"] for tag in raw_tag}
            owner_tag = dict_tag.get("Owner")
            project_tag = dict_tag.get("Project")

            # building flat list
            inventory_rows.append({
                "resource_id": instance_id,
                "resource_type": "ec2",
                "status": status,
                "owner_tag": owner_tag,
                "project_tag": project_tag,
                "launch_time": launch_time.isoformat() if launch_time else None
            })

    return inventory_rows

if __name__ == "__main__":
    aws_payload = mock_ec2_instance()
    parsed_data = parse_aws(aws_payload)
    for row in parsed_data:
        print(row)

