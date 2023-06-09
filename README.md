How to run:

        - Adjust example.env to hold your local authentication variables, rename to .env.
        - Add properties.json(sold seperately) in the json_input directory.
        - Run main.py.
        - Wait.
        
The script will first connect to the database, Drop all tables and types, create Tables and Types as listed below.
If the file is present in Json_input, it'll split properties.json values over multiple temporary json files, 
which it then uses to insert the data that we need in the database.
Then it'll read the database for existing users, and generate fake message chains between user_looking_to_rent and user_renting_out_property,
and insert those messages in the Message table.
Finally, it'll remove the temporary files again. 

Table naming:

        Users (
        uid SERIAL PRIMARY KEY,
        is_admin BOOLEAN NOT NULL DEFAULT FALSE,
        name VARCHAR(60),
        email TEXT,
        hashed_pw TEXT,
        created DATE, //(%Y-%m-%d)
        last_active DATE  //(%Y-%m-%d)
        )
        
        User_looking_to_rent (
        uid INTEGER REFERENCES Users(uid),
        age INTEGER,
        gender gender_type,
        status status_type
        )
        
        user_rents_out_property (
        uid INTEGER REFERENCES Users(uid),
        property_id TEXT
        )
        
        Property (
        property_id TEXT PRIMARY KEY,
        name VARCHAR(80),
        city VARCHAR(40),
        lat FLOAT,
        long FLOAT,
        cover_image_url TEXT,

        date_published TIMESTAMP WITH TIME ZONE, //(%Y-%m-%dT%H:%M:%S.%f%z)

        rent FLOAT,
        rent_incl BOOLEAN,
        deposit FLOAT,
        additional_cost VARCHAR(10), 
        sqm INTEGER,
        postal_code VARCHAR(7),
        type prop_type,
        availability_start DATE, //(\'y-m-d)
        availability_end TEXT //("Indefinite period") || (\'y-m-d)
        )
        
        Property_match (
        property_Id TEXT REFERENCES Property(property_id),
        property_match_id SERIAL PRIMARY KEY,
        age_min INTEGER,
        age_max INTEGER,
        gender gender_match_type,
        match_status match_status_type[] 
        )
        
        Property_details (
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
        last_seen_at TIMESTAMP WITH TIME ZONE// (%Y-%m-%dT%H:%M:%S.%f%z)
        )
        
        
        Message (
        message_id SERIAL PRIMARY KEY,
        sender_id INTEGER REFERENCES Users(uid),
        receiver_id INTEGER REFERENCES Users(uid),
        property_id TEXT REFERENCES Property(property_id),
        content TEXT,
        timestamp TIMESTAMP
        )
       
Enum Types: 

        prop_type('Room', 'Apartment', 'Studio', 'Anti-squat', 'Student residence', 'Other')
        match_status_type('Student','Working Student', 'Working', 'Looking for a job', 'Not important')
        gender_type_match('Female', 'Male','Mixed', 'Not important')
        energy_label_type('A','B','C','D','E', 'F', 'G', 'Unknown')
        furnished_type('Furnished', 'Unfurnished', 'Uncarpeted')
        gender_roommates_type('Female', 'Male', 'Mixed', 'Unknown')
        gender_type('Female', 'Male','Other')
        status_type('Student','Working Student', 'Working', 'Looking for a job')
        
        
