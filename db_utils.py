def create_tables(cursor):
    
    #Create types.
    cursor.execute("""
    CREATE TYPE match_status_type as ENUM ('Student','WorkingStudent', 'Working', 
    'LookingForAJob', 'NotImportant');
    CREATE TYPE gender_match_type as ENUM ('Female', 'Male','Mixed', 'NotImportant');
    CREATE TYPE gender_type as ENUM ('Female', 'Male','Other');
    CREATE TYPE status_type as ENUM ('Student','WorkingStudent', 'Working', 
    'LookingForAJob');
    CREATE TYPE prop_type AS ENUM ('Room', 'Apartment', 'Studio', 'AntiSquat', 
    'StudentResidence', 'Other');
    CREATE TYPE energy_label_type AS ENUM('A','B','C','D','E', 'F', 'G', 'Unknown');
    CREATE TYPE furnished_type as ENUM('Furnished', 'Unfurnished', 'Uncarpeted');
    CREATE TYPE gender_roommates_type as ENUM('Female', 'Male', 'Mixed', 'Unknown');
    """)
    # Create the User table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        uid SERIAL PRIMARY KEY,
        is_admin BOOLEAN NOT NULL DEFAULT FALSE,
        name VARCHAR(60),
        email TEXT,
        hashed_pw TEXT,
        created DATE,
        last_active DATE
    );
    """)

    # Create the User_looking_to_rent table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User_looking_to_rent (
        uid INTEGER REFERENCES Users(uid),
        age INTEGER,
        gender gender_type,
        status status_type
    );
    """)

    # Create the user_rents_out_property table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_rents_out_property (
        uid INTEGER REFERENCES Users(uid),
        property_id TEXT
    );
    """)

    # Create the Property table
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS Property (
        property_id TEXT PRIMARY KEY,
        name VARCHAR(80),
        city VARCHAR(40),
        lat FLOAT,
        long FLOAT,
        cover_image_url TEXT,
        date_published TIMESTAMP WITH TIME ZONE,
        rent FLOAT,
        rent_incl BOOLEAN,
        deposit FLOAT,
        additional_cost VARCHAR(10), 
        sqm INTEGER,
        postal_code VARCHAR(7),
        type prop_type,
        availability_start DATE,
        availability_end TEXT
    );
    """)

    # Create the Property_match table
    cursor.execute("""

        CREATE TABLE IF NOT EXISTS Property_match (
        property_Id TEXT REFERENCES Property(property_id),
        property_match_id SERIAL PRIMARY KEY,
        age_min INTEGER,
        age_max INTEGER,
        gender gender_match_type,
        match_status match_status_type[] 
    );
    """)

    # Create the Property_details table
    cursor.execute('''

    CREATE TABLE IF NOT EXISTS Property_details (
        property_id TEXT REFERENCES Property(property_id),
        property_details_id SERIAL PRIMARY KEY,
        description TEXT,
        description_translated TEXT,
        roommates VARCHAR(20),
        gender_roommates gender_roommates_type,
        furnished furnished_type,
        energy_label energy_label_type,
        internet BOOLEAN,
        pets_allowed BOOLEAN,
        own_toilet BOOLEAN,
        own_bathroom BOOLEAN,
        own_kitchen BOOLEAN,
        smoking_allowed BOOLEAN, 
        last_seen_at TIMESTAMP WITH TIME ZONE
    );
    ''')

    # Create the Message table
    cursor.execute('''
    CREATE TABLE Message (
        message_id SERIAL PRIMARY KEY,
        sender_id INTEGER REFERENCES Users(uid),
        receiver_id INTEGER REFERENCES Users(uid),
        property_id TEXT REFERENCES Property(property_id),
        content TEXT,
        timestamp TIMESTAMP
    );
    ''')

    # Commit the changes
    print("Tables made")
    cursor.connection.commit()
