import os
import threading
from dotenv import load_dotenv
import psycopg2
from db_utils import create_tables
from drop_tables import drop_all_tables
from message_generator.generate_message_json import generate_fake_messages
from prepare.prepare_user_renter_data import prepare_user_renter_data
from read_in_batches import read_json_file_in_batches
from prepare.prepare_property_data import prepare_property_data
from prepare.prepare_property_details_data import prepare_property_details_data
from prepare.prepare_property_match_data import prepare_property_match_data
from prepare.prepare_user_data import prepare_user_data
from prepare.prepare_user_landlord_data import prepare_user_landlord_data
from prepare.prepare_message_data import prepare_message_data
from filltables.property_table import insert_property_data
from filltables.property_details_table import insert_property_details_data
from filltables.property_match_table import insert_property_match_data
from filltables.users_table import insert_users_data
from filltables.user_looking_to_rent_table import insert_user_renter_data
from filltables.user_rents_out_property_table import insert_user_landlord_data
from filltables.message_table import insert_message_data
from json_splitter.migrate_property import migrate_property_json
from json_splitter.migrate_user import migrate_user_json

# convert JSON properties.json to multiple files if they don't already exist.

load_dotenv()
# Establish a connection to the database
db = psycopg2.connect(
    host=os.environ.get('DSH_HOST'),  # host = db # local os.environ.get('DSH_HOST')
    port=os.environ.get('DSH_PORT'),  # post = 5432 # local os.environ.get('DSH_PORT')
    database=os.environ.get('DSH_DB'),  # dsh = dsh # local os.environ.get('DSH_DB')
    user=os.environ.get('DSH_USER'),  # user = dsh # local os.environ.get('DSH_USER')
    password=os.environ.get("DSH_PASSWORD"),  # pw = dsh # local os.environ.get("DSH_PASSWORD")
)

# Open a cursor to execute SQL statements
cur = db.cursor()

#temp drop tables
drop_all_tables(cur)

#if Messages exists with data, exit
# Check if Messages table exists
cur.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE LOWER(table_name) = 'message'
    )
""")
table_exists = cur.fetchone()[0]

if table_exists:
    print("Message table exists.", flush=True)
    print("Exiting program", flush=True)
    exit(0)
else:
    print("Message table does not exist.", flush=True)
    print("Continuing", flush=True)
#rest of the program
create_tables(cur)
cursor = db.cursor()


print("Checking if properties.json exists", flush=True)
if not os.path.isfile('json_input/properties.json'):
    print("Please place the properties.json file in the json_input directory.", flush=True)
    exit(0)
    # check for json directory
if not os.path.isdir('json'):
    os.mkdir('json')

print("Checking if migrated data files exist.", flush=True)
# convert JSON properties.json to multiple files if they don't already exist at the same time.
threads = []
if not os.path.isfile('json/property.json'):
    threads.append(threading.Thread(target=migrate_property_json))
    print("Migrating property related data", flush=True)
else:
    print("Property.json found", flush=True)
if not os.path.isfile('json/user.json'):
    threads.append(threading.Thread(target=migrate_user_json))
    print("Migrating User related data", flush=True)
else:
    print("User.json found", flush=True)
    # Start the threads
for thread in threads:
    thread.start()

    # Wait for all threads to complete
for thread in threads:
    thread.join()
    print("data migrated", flush=True)

# Read the JSON data in batches and insert into the tables
batch_size = 150

property_filename = "json/property.json"
for batch_data in read_json_file_in_batches(property_filename, batch_size):
    property_data = prepare_property_data(batch_data)
    insert_property_data(cursor, property_data)
print("property table filled", flush=True)
# os.remove("json/property.json")

property_details_filename = "json/property_details.json"
for batch_data in read_json_file_in_batches(property_details_filename, batch_size):
    property_details_data = prepare_property_details_data(batch_data)
    insert_property_details_data(cursor, property_details_data)
print("property_details table filled", flush=True)
# os.remove("json/property_details.json")

property_match_filename = "json/property_match.json"
for batch_data in read_json_file_in_batches(property_match_filename, batch_size):
    property_match_data = prepare_property_match_data(batch_data)
    insert_property_match_data(cursor, property_match_data)
print("property_match table filled", flush=True)
# os.remove("json/property_match.json")

user_filename = 'json/user.json'
seen_user_ids = set()
# To prevent multiple users of the same ID from getting imported from the JSON
for batch_data in read_json_file_in_batches(user_filename, batch_size):
    users_data = prepare_user_data(batch_data, seen_user_ids)
    insert_users_data(cursor, users_data)
print("users table filled", flush=True)
# os.remove("json/user.json")

user_landlord_filename = "json/user_landlord.json"
for batch_data in read_json_file_in_batches(user_landlord_filename, batch_size):
    user_landlord_data = prepare_user_landlord_data(batch_data)
    insert_user_landlord_data(cursor, user_landlord_data)
print("User_rents_out_property table filled", flush=True)
# os.remove("json/user_landlord.json")

user_renter_filename = "json/user_renter.json"
for batch_data in read_json_file_in_batches(user_renter_filename, batch_size):
    user_renter_data = prepare_user_renter_data(batch_data)
    insert_user_renter_data(cursor, user_renter_data)
print("User_looking_to_rent table filled")
# os.remove("json/user_renter.json")

# create fake messages here if they don't already exist.
if not os.path.isfile('json/fake_messages.json'):
    print("Generating fake messages.", flush=True)
    generate_fake_messages(cursor)

message_filename = "json/fake_messages.json"
for batch_data in read_json_file_in_batches(message_filename, batch_size):
    message_data = prepare_message_data(batch_data)
    insert_message_data(cursor, message_data)
print("Messages table filled", flush=True)
# os.remove("json/fake_messages.json")

# Close the database connection
cursor.close()
db.close()

print("Should be migrated over successfully")

exit(0)
