import os
import psycopg2

password = os.environ.get('DB_PASSWORD')
# Create a connection object to the database.
conn = psycopg2.connect(database="postgres", user="postgres",
                        password=password, host="localhost", port="5432")

# Create a cursor object from the connection object.
cur = conn.cursor()

# Execute an INSERT statement to insert data into the database.
cur.execute(
    "INSERT INTO sample (exercise_string) VALUES (%s)",
    ("John Doe",)
)

# Commit the changes.
conn.commit()

# Close the cursor and connection objects.
cur.close()
conn.close()
