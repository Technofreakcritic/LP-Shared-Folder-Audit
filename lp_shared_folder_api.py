import json
import requests
import csv

# Configuration
url = 'https://lastpass.com/enterpriseapi.php'
json_file_path = '/Users/meowmeow/Desktop/LP_JSON_Detailed.json'
csv_file_path = '/Users/meowmeow/Desktop/LP_Cleaned_Version.csv'

# Fetch data from the API
payload = {
    "cid": your_cid,
    "provhash": "your_provisioning_hash",
    "cmd": "getsfdata",
    "data": "all"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print('Request successful!')

    # Load JSON data
    json_data = json.loads(response.text)

    # Count objects with "deleted": true
    count_deleted_true = sum(1 for obj in json_data.values() if obj.get("deleted") is True)
    print("Number of objects with 'deleted': true:", count_deleted_true)

    # Count objects with "deleted": False
    count_deleted_false = sum(1 for obj in json_data.values() if obj.get("deleted") is False)
    print("Number of objects with 'deleted': False:", count_deleted_false)

    ## All IAM members have Admin access, remove them
    email_addresses_to_remove = [
        "bro12@gmail.com",
        "abc123@gnail.com",

    ]

    # Remove nested objects for specific email addresses and filter users
    for obj in json_data.values():
        obj["users"] = [user for user in obj["users"] if user.get("username") not in email_addresses_to_remove]
        obj["users"] = [user for user in obj["users"] if user.get("can_administer") == "1"]

    # Filter and print objects with "deleted": false
    filtered_data = {key: value for key, value in json_data.items() if value.get("deleted") is False}

    # Create a CSV file
    csv_headers = ["Shared Folder Name", "Score", "List of Admin", "Active"]

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_headers)

        # Generate CSV data from filtered JSON
        for obj in filtered_data.values():
            shared_folder_name = obj.get("sharedfoldername")
            score = obj.get("score")
            admin_list = ', '.join(user.get("username").split('@')[0] for user in obj["users"])
            active_status = "Active" if not obj.get("deleted") else "Deleted"

            csv_writer.writerow([shared_folder_name, score, admin_list, active_status])

    print("CSV file created:", csv_file_path)

    # Print the first 10 rows of the CSV
    print("First 10 rows of the CSV:")
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            if i < 10:  # Print first 10 rows
                print(', '.join(row))
else:
    print('Request failed. Status code:', response.status_code)
