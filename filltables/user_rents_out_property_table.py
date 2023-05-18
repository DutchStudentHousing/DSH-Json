def insert_user_landlord_data(cursor, user_landlord_data):

    cursor.executemany("""        
        INSERT INTO user_rents_out_property (uid, property_id)
        VALUES (%s, %s);
    """, user_landlord_data)

    cursor.connection.commit()
