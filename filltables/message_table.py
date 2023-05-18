def insert_message_data(cursor, message_data):
    cursor.executemany('''
        INSERT INTO message (sender_id, receiver_id, property_id, content, timestamp)
        VALUES (%s, %s, %s, %s, %s);
    ''', message_data)
    cursor.connection.commit()
