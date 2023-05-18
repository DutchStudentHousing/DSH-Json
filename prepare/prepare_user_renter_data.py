def prepare_user_renter_data(batch_data):
    user_renter_data =[]
    for item in batch_data:
        user_id = item['user_id']
        if user_id is not None:
            record = (
                item['user_id'],
                item['age'],
                item['gender']
            )
            user_renter_data.append(record)
    return user_renter_data
