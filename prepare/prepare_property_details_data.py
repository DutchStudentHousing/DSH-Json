from datetime import datetime


def prepare_property_details_data(batch_data):
    property_details_data = []

    for item in batch_data:
        if item['internet'] == '':
            internet_included = True
        else:
            internet_included = False
        if item['pets'] == 'allowed' or item['pets'] == 'By mutual agreement':
            pets_allowed = True
        else:
            pets_allowed = False
        if item['toilet'] == 'Own':
            own_toilet = True
        else:
            own_toilet = False
        if item['bathroom'] == 'Own':
            own_bathroom = True
        else:
            own_bathroom = False
        if item['kitchen'] == 'Own':
            own_kitchen = True
        else:
            own_kitchen = False
        if item['smoking'] == 'Yes' or item['smoking'] == 'Not important':
            smoking_allowed = True
        else:
            smoking_allowed = False
        if item['furnished'] == '':
            furnished = 'Unfurnished'
        else:
            furnished = item['furnished']
        # Extract the date string from the 'last_seen_at' dictionary
        last_seen_at_str = item['last_seen_at']
        # Convert the date string to a datetime object
        last_seen_at_datetime = datetime.strptime(last_seen_at_str, "%d-%m-%YT%H:%M:%S.%f%z")

        record = (
            item['property_id'],
            item['property_details_id'],
            item['description'],
            item['description_translated'],
            # If not allowed/shared all are false
            item['roommates'],
            item['gender_roommates'],
            furnished,
            item['energy_label'],
            internet_included,
            pets_allowed,
            own_toilet,
            own_bathroom,
            own_kitchen,
            smoking_allowed,
            last_seen_at_datetime
        )
        property_details_data.append(record)
    return property_details_data
