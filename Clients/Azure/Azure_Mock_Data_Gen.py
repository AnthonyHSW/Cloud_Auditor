'''
Author: Anthony Wong
Email: Anw2727@gmail.com
A mock data generator for Azure. 
This is used to generate mock data for testing purposes.
In theory I could just use the api key and get the data from Azure.
'''

def get_mock_azure_vms():
    """
    Simulates calling `list_all()` using the Azure SDK and calling 
    `.as_dict()` on the returned virtual machine objects.
    """
    return [
        {
            "id": "/subscriptions/sub-123/resourceGroups/rg-data/providers/Microsoft.Compute/virtualMachines/db-server-01",
            "name": "db-server-01",
            "type": "Microsoft.Compute/virtualMachines",
            "location": "eastus",
            "tags": {
                "Owner": "DataTeam",
                "Project": "CloudAuditor"
            },
            "properties": {
                "provisioningState": "Succeeded",
                "timeCreated": "2026-07-28T14:30:00.000Z",
                "instanceView": {
                    "statuses": [
                        {"code": "ProvisioningState/succeeded"},
                        {"code": "PowerState/running"} 
                    ]
                }
            }
        },
        {
            "id": "/subscriptions/sub-123/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/old-app-server",
            "name": "old-app-server",
            "type": "Microsoft.Compute/virtualMachines",
            "location": "westus2",
            "tags": {
                "Project": "LegacyApp",
                "Owner": "OpsTeam"
            },
            "properties": {
                "provisioningState": "Succeeded",
                "timeCreated": "2026-06-15T09:00:00.000Z",
                "instanceView": {
                    "statuses": [
                        {"code": "ProvisioningState/succeeded"},
                        {"code": "PowerState/stopped"} 
                    ]
                }
            }
        }
    ]

def parse_azure(mock_response):
    """
    Parses the list of dictionaries returned by `get_mock_azure_vms()` into a flat list
    that can be used by SQL database.
    """
    inventory_rows = []

    for vm in mock_response:
        # extracting data
        resource_id = vm.get("id")
        resource_type = vm.get("type")
        status = next((status["code"].split("/")[-1] for status in vm.get("properties", {}).get("instanceView", {}).get("statuses", []) if "PowerState" in status["code"]), None)
        launch_time = vm.get("properties", {}).get("timeCreated")
        tags = vm.get("tags", {})
        owner_tag = tags.get("Owner")
        project_tag = tags.get("Project")

        # building flat list
        inventory_rows.append({
            "resource_id": resource_id,
            "resource_type": resource_type,
            "status": status,
            "launch_time": launch_time,
            "owner_tag": owner_tag,
            "project_tag": project_tag
        })

    return inventory_rows

if __name__ == "__main__":
    print("--- Simulating Azure API Call ---")
    azure_payload = get_mock_azure_vms()
    
    print("\n--- Parsing Azure Data for SQL Insertion ---")
    flat_azure_data = parse_azure(azure_payload)
    
    for row in flat_azure_data:
        print(row)