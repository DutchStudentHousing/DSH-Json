import json
import random


def generate_fake_messages(cursor):
    try:

        # Fetch user_ids and property_ids
        cursor.execute("SELECT uid FROM User_looking_to_rent;")
        tenant_ids = [record[0] for record in cursor.fetchall()]

        cursor.execute("SELECT uid, property_id FROM user_rents_out_property;")
        landlord_records = cursor.fetchall()

        messages = []

        for record in landlord_records:
            landlord_id = record[0]
            property_id = record[1]

            # Fetch the property listing date
            cursor.execute("SELECT date_published FROM Property WHERE property_id = %s;", (property_id,))
            listing_date = cursor.fetchone()[0]

            # Compute the difference in seconds between the listing date and the end date
            cursor.execute("SELECT EXTRACT(EPOCH FROM TIMESTAMP '01-01-2019' - %s);", (listing_date,))
            seconds_diff = cursor.fetchone()[0]

            for tenant_id in random.sample(tenant_ids, 5):  # Choose 5 tenants to send messages
                # Generate a random timestamp between the listing date and the end date
                cursor.execute("SELECT %s + INTERVAL '1 second' * ROUND((random() * %s)::numeric);",
                            (listing_date, seconds_diff))
                timestamp = cursor.fetchone()[0]

                message = {
                    "sender_id": tenant_id,
                    "receiver_id": landlord_id,
                    "property_id": property_id,
                    "message": "Hello, I am interested in your property!",
                    "sent_at": timestamp.strftime('%d-%m-%YT%H:%M:%S')
                }
                messages.append(message)

                if random.choice([True, False]):  # Randomly decide whether the landlord replies
                    # Generate a random timestamp for landlord's reply, 1 to 60 minutes later
                    cursor.execute("SELECT %s + INTERVAL '1 minute' * ROUND((random() * 60)::numeric);", (timestamp,))
                    timestamp_reply = cursor.fetchone()[0]

                    reply = {
                        "sender_id": landlord_id,
                        "receiver_id": tenant_id,
                        "property_id": property_id,
                        "message": "Thanks for your interest. When can you move in?",
                        "sent_at":  timestamp_reply.strftime('%d-%m-%YT%H:%M:%S')  # date in dd-mm-yyyy time format
                    }
                    messages.append(reply)

                    if random.choice([True, False]):  # Randomly decide whether there's a third message
                        # Generate a random timestamp for tenant's second message, 1 to 60 minutes after the reply
                        cursor.execute("SELECT %s + INTERVAL '1 minute' * ROUND((random() * 60)::numeric);",
                                    (timestamp_reply,))
                        timestamp_second_message = cursor.fetchone()[0]

                        second_message = {
                            "sender_id": tenant_id,
                            "receiver_id": landlord_id,
                            "property_id": property_id,
                            "message": "I can move in next month.",
                            "sent_at": timestamp_second_message.strftime('%d-%m-%YT%H:%M:%S')  # date in dd-mm-yyyy time format
                        }
                        messages.append(second_message)

        # Save the messages to a JSON file
        with open('json/fake_messages.json', 'w') as file:
            json.dump(messages, file)

    except Exception as e:
        print("Error:", e)

