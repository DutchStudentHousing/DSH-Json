
def drop_all_tables(cursor):
    try:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        for table in cursor.fetchall():
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")
        cursor.connection.commit()
        print("Tables Dropped")
    except Exception as e:
        print("Error dropping tables:", str(e))

    # Drop the types
    try:
        cursor.execute("""
            SELECT typname 
            FROM pg_type 
            WHERE typcategory = 'E'
        """)
        for custom_type in cursor.fetchall():
            cursor.execute(f"DROP TYPE IF EXISTS {custom_type[0]} CASCADE;")
        cursor.connection.commit()
        print("Types Dropped")
    except Exception as e:
        print("Error dropping types:", str(e))

    # Commit the changes
