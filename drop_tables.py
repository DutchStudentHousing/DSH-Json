def drop_all_tables(cursor):
    table_names = ["Users", "User_looking_to_rent", "user_rents_out_property", "Property", "Property_match", "Property_details", "Message"]
    types = ["prop_type", "match_status_type", "gender_type", "energy_label_type", "furnished_type", "gender_roommates_type", "statust_type"]
    try:
        for table in table_names:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
        cursor.connection.commit()
        print("Tables Dropped")
    except Exception as e:
        print("Error dropping tables:", str(e))

    # Drop the types
    try:
        for custom_type in types:
            cursor.execute(f"DROP TYPE IF EXISTS {custom_type} CASCADE;")
        cursor.connection.commit()
        print("Types Dropped")
    except Exception as e:
        print("Error dropping types:", str(e))

    # Commit the changes
