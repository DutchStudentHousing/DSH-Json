def prepare_message_data(batch_data):
    message_data = []
    for item in batch_data:
        record = (
            item["sender_id"],
            item["receiver_id"],
            item["property_id"],
            item["message"],
            item["sent_at"],
        )

        message_data.append(record)
    return message_data
