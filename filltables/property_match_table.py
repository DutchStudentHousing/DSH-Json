def insert_property_match_data(cursor, property_match_data):
        # Insert the property data into the Property table
        cursor.executemany("""
            INSERT INTO Property_match (property_id, property_match_id, age_min, age_max, gender, match_status)
            VALUES (%s, %s, %s, %s, %s, %s::match_status_type[]);
        """, property_match_data)

        # Commit the changes
        cursor.connection.commit()
