def prepare_user_data(batch_data, seen_user_ids):
    users_data =[]
    for item in batch_data:
        user_id = item['user_id']
        
        if user_id is not None or user_id in seen_user_ids:

            record = (
                item['user_id'],
                item['isAdmin'],
                item['name'],
                item['email'],
                item['password'],
                item['user_member_since'],
                item['last_active']
            )
            users_data.append(record)
            seen_user_ids.add(user_id)
    return users_data
