def insert_property_data(cursor, property_data):
    # Insert the property data into the Property table

    cursor.executemany('''
        INSERT INTO Property (property_id, name, city, lat, long, 
        cover_image_url, date_published, rent, rent_incl, deposit,
        additional_cost, sqm, postal_code, type, availability_start, 
        availability_end)
        VALUES (%s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s);
    ''', property_data)
    # Commit
    cursor.connection.commit()
