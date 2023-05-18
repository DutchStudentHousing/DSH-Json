def prepare_property_match_data(batch_data):
    property_match_data =[]
    for item in batch_data:
        record = (
            item['property_id'],
            item['property_match_id'],
            item['age_min'],
            item['age_max'],
            item['gender']
        )
        property_match_data.append(record)
    return property_match_data
