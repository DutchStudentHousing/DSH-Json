def insert_user_renter_data(cursor, user_renter_data):

    cursor.executemany("""        
        INSERT INTO user_looking_to_rent (uid, age, gender, status)
        VALUES (%s, %s, %s, %s);
    """, user_renter_data)

    cursor.connection.commit()
