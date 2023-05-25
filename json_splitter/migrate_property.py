import json
from datetime import datetime



def migrate_property_json():

    # Open the main JSON file
    with open('json_input/properties.json', encoding='utf-8') as f:
        data = []
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip this line if it's not valid JSON
                pass

        # Create a list to store the extracted data for Property table
        new_data = []
        # property_id = 1  # start with ID 1
        # instead of fresh id, use externalId
        # Loop through each entry in the main JSON file
        for entry in data:
            # Set time format
            date_str = entry.get('firstSeenAt').get('$date')

            # Convert the string to a datetime object
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            # CamelCase type
            type_value = entry.get('propertyType')
            if type_value == "Anti-squat":
                type_value = "AntiSquat"
            elif type_value == "Student residence":
                type_value = "StudentResidence"

            # Convert the datetime object back to a string with the desired format
            formatted_date = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            # Extract the relevant data fields for the Property table
            property_data = {
                'property_id': entry.get('externalId'),
                'name': entry.get('title'),
                'city': entry.get('city'),
                'lat': entry.get('latitude'),
                'long': entry.get('longitude'),
                'cover_image_url': entry.get('coverImageUrl'),
                'date_published': formatted_date,  # change date format here
                'rent': entry.get('rent'),
                'rent_incl': entry.get('rentDetail'),
                'deposit': entry.get('deposit'),
                'additional_cost': entry.get('additionalCosts'),
                'sqm': entry.get('areaSqm'),
                'postal_code': entry.get('postalCode'),
                'type': type_value,
                'availability': entry.get('rawAvailability')
            }

            # Append the new entry to the list
            new_data.append(property_data)

            # property_id += 1  # increment property_id for the next entry

        # Create lists to store the extracted data for Property_match and Property_details tables
        property_match_data = []
        property_details_data = []

        property_id = 1  # reset property_id to 1

        # Loop through each entry in the main JSON file again to extract data
        # for Property_match and Property_details tables
        for entry in data:
            # Extract the relevant data fields for the Property_match table
            match_status_types = entry.get('matchStatus').split(",") if entry.get('matchStatus') else ["NotImportant"]

            for i, match_status_type in enumerate(match_status_types):
                if match_status_type.strip() == "Working student":
                    match_status_types[i] = "WorkingStudent"
                elif match_status_type.strip() == "Looking for a job":
                    match_status_types[i] = "LookingForAJob"
                elif match_status_type == " Working":
                    match_status_types[i] = "Working"
                elif match_status_type.strip() == "Not important":
                    match_status_types[i] = "NotImportant"

            match_gender_type = entry.get('matchGender')
            if match_gender_type == "Not important":
                match_gender_type = "NotImportant"

            match_age = entry.get('matchAge')
            if match_age and 'Not important' in match_age:

                age_min = "16"
                age_max = "99"
            else:
                age_min = match_age.split()[0] if match_age else "16"
                age_max = match_age.split()[-2] if match_age else "99"

            property_match_data.append({
                'property_id': entry.get('externalId'),
                'property_match_id': property_id,
                'age_min': age_min,
                'age_max': age_max,
                'match_status': match_status_types,  # working, student, etc
                'gender': match_gender_type if entry.get("matchGender") else "NotImportant"
            })

            last_seen_date_str = entry.get('lastSeenAt').get('$date')
            last_seen_date_obj = datetime.strptime(last_seen_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            last_seen_formatted_date = last_seen_date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

            # Extract the relevant data fields for the Property_details table
            property_details_data.append({
                'property_id': entry.get('externalId'),
                'property_details_id': property_id,
                'description': entry.get('descriptionNonTranslated'),
                'description_translated': entry.get('descriptionTranslated'),
                'last_seen_at': last_seen_formatted_date,
                'roommates': entry.get('roommates'),  # Amount of roommates.
                'gender_roommates': entry.get('gender'),  # genders in house.
                'furnished': entry.get('furnish'),  # furnished true, unfurnished false, uncarpeted
                'energy_label': entry.get('energyLabel'),  # EnergyLabel letter or null.
                'internet': entry.get(''),  # yes, is true, no is false, else no.
                'pets': entry.get('pets'),  # if anything but not allowed, true, else false.
                'toilet': entry.get('toilet'),  # if own, true, else if shared, false, else null.
                'bathroom': entry.get('shower'),  # if own, true, else if shared, false, else null.
                'kitchen': entry.get('kitchen'),  # if own, true, else if shared, false, else null.
                'smoking': entry.get('smokingInside')  # if anything but not allowed, true, else false.
            })

            property_id += 1  # increment property_id for the next entry

        # Save the extracted data as separate JSON files
        with open('json/property.json', 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

        with open('json/property_match.json', 'w', encoding='utf-8') as f:
            json.dump(property_match_data, f, ensure_ascii=False, indent=4)

        with open('json/property_details.json', 'w', encoding='utf-8') as f:
            json.dump(property_details_data, f, ensure_ascii=False, indent=4)
