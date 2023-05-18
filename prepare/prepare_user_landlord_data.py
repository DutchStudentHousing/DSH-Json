def prepare_user_landlord_data(batch_data):
    user_landlord_data =[]
    for item in batch_data:
        user_id = item['user_id']
        if user_id is not None:
            record = (
                item['user_id'],
                item['property_id']
            )
            user_landlord_data.append(record)
    return user_landlord_data
