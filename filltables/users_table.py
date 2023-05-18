def insert_users_data(cursor, users_data):
    cursor.executemany("""
        INSERT INTO Users (uid, is_admin, name, email, hashed_pw, created, last_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (uid) DO NOTHING;
    """, users_data)
    cursor.connection.commit()
