import json
import random
import string
from datetime import datetime, timedelta
from faker import Faker


def migrate_user_json():

    # Function to generate a random passwordAC
    def generate_password(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # Open the properties JSON file
    with open('json_input/properties.json', encoding='utf-8') as f:
        data = []
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip this line if it's not valid JSON
                pass

    # Create a list to store the extracted user data
    user_data_list = []
    # Create a list to store the extracted user landlord data
    user_landlord_data_list = []
    # property_id = 1

    # Loop through each entry in the properties JSON file
    for entry in data:
        # Extract the relevant data fields for the User table
        user_data = {
            'user_id': entry.get('userId'),
            'isAdmin': False,
            'name': entry.get('userDisplayName') or 'Unknown',
            'email': (entry.get('userDisplayName') or 'Unknown') + str(entry.get('userId')) + '@dsh.nl',
            # remove space from Email.
            'password': generate_password(),
            'user_member_since': datetime.strptime(entry.get('userMemberSince'), "%d-%m-%Y").strftime('%Y-%m-%d') if entry.get('userMemberSince') else datetime.now().strftime('%Y-%m-%d'),
            'last_active': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        }
        user_data['email'] = user_data['email'].replace(',', '')
        user_data['email'] = user_data['email'].replace(' ', '')
        # Append the new user entry to the list
        user_data_list.append(user_data)

        # Extract the relevant data fields for the User_landlord table
        user_landlord_data = {
            'user_id': entry.get('userId'),
            'property_id': entry.get('externalId')
        }

        # Append the new user landlord entry to the list
        user_landlord_data_list.append(user_landlord_data)
    #   property_id += 1

    # Save the extracted data as separate JSON files
    with open('json/user.json', 'w', encoding='utf-8') as f:
        json.dump(user_data_list, f, ensure_ascii=False, indent=4)

    with open('json/user_landlord.json', 'w', encoding='utf-8') as f:
        json.dump(user_landlord_data_list, f, ensure_ascii=False, indent=4)

    # fake user looking to rent data (user_renter.json)
    # Filter out instances where user_id is None or not of type str, and consider them as 0
    filtered_user_data = [user for user in user_data_list if
                          user['user_id'] is not None and isinstance(user['user_id'], str)]
    max_user_id = max([int(user['user_id']) for user in filtered_user_data] or [0])

    fake = Faker()
    # Generate 20,000 fake users in 'user.json'
    for i in range(20000):
        fake_user_id = max_user_id + i + 1
        fake_name = fake.name()
        user_data = {
            'user_id': fake_user_id,
            'isAdmin': False,
            'name': fake_name,
            'email': f'{fake_name}{fake_user_id}@dsh.nl',
            'password': generate_password(),
            'user_member_since': datetime.now().strftime('%Y-%m-%d'),
            'last_active': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        }

        user_data['email'] = user_data['email'].replace(' ', '')
        user_data_list.append(user_data)

    # Save the updated data as 'user.json'
    with open('json/user.json', 'w', encoding='utf-8') as f:
        json.dump(user_data_list, f, ensure_ascii=False, indent=4)

    # Generate fake user_renter data in 'user_renter.json'
    user_renter_data_list = []
    for i in range(2000):
        user_renter_data = {
            'user_id': max_user_id + i + 1,
            'age': random.randint(16, 50),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'status': random.choice(['Student','WorkingStudent', 'Working', 'LookingForAJob'])
        }
        user_renter_data_list.append(user_renter_data)

    # Save user_renter_data_list as 'user_renter.json'
    with open('json/user_renter.json', 'w', encoding='utf-8') as f:
        json.dump(user_renter_data_list, f, ensure_ascii=False, indent=4)
