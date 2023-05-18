def insert_property_details_data(cursor, property_details_data):
    # Insert the property data into the Property table
    cursor.executemany("""
        INSERT INTO Property_details (property_id, property_details_id, description, description_translated, 
        roommates, gender_roommates, furnished, energy_label, 
        internet, pets_allowed, own_toilet, own_bathroom, 
        own_kitchen, smoking_allowed, last_seen_at)
        VALUES (%s, %s, %s, %s, 
        %s, %s, %s, %s, 
        %s, %s, %s, %s,
         %s, %s, %s);
    """, property_details_data)

    # Commit the changes
    cursor.connection.commit()
