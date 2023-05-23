import json
from datetime import datetime


def prepare_property_data(batch_data):
    property_data = []
    for item in batch_data:
        if item['rent_incl'] == 'Utilities incl.':
            rent_incl_flag = True
        else:
            rent_incl_flag = False
        if item['additional_cost'] is None:
            additional_cost = "0"
        else:
            additional_cost = item['additional_cost']
        if item['deposit'] is None:
            deposit = "0"
        else:
            deposit = item['deposit']
        date_published = datetime.strptime(item['date_published'], "%Y-%m-%dT%H:%M:%S.%f%z")
        availability_parts = item['availability'].split(' - ')
        availability_parts[0].strip()

        # Parse the date in the provided format and then format it again in the desired format
        availability_start = datetime.strptime(availability_parts[0], '%d-%m-\'%y').date()
        availability_start = availability_start.strftime('%Y-%m-%d')

        period = availability_parts[1].strip()

        if(period.lower()) == 'indefinite period':
            formatted_period = period
        else:
            # Parse the date in the provided format and then format it again in the desired format
            formatted_period = datetime.strptime(availability_parts[1].strip(), '%d-%m-\'%y').date()
            formatted_period = formatted_period.strftime('%Y-%m-%d')

        record = (
            item['property_id'],
            item['name'],
            item['city'],
            float(item['lat']),
            float(item['long']),
            item['cover_image_url'],
            date_published,
            item['rent'],
            rent_incl_flag,
            deposit,
            additional_cost,
            item['sqm'],
            item['postal_code'],
            item['type'],
            availability_start,
            formatted_period

        )
        property_data.append(record)
    return property_data
