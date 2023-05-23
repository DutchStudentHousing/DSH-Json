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
                'type': entry.get('propertyType'),
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
            property_match_data.append({
                'property_id': entry.get('externalId'),
                'property_match_id': property_id,
                'age_min': entry.get('matchAge').split()[0] if entry.get('matchAge') else None,
                'age_max': entry.get('matchAge').split()[-2] if entry.get('matchAge') else None,
                'match_status': entry.get('matchStatus'),  # working, student, etc
                'gender': entry.get('matchGender')
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
