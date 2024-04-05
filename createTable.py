import psycopg2
import json

# Read JSON data from file
with open('table_schema.json') as json_file:
    data = json.load(json_file)

try:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        user="postgres",
        password="messi10",
        host="localhost",
        port="5432",
        database="opensea_collections"
    )

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Define your SQL statement to create a table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS opensea_collections_data (
        id SERIAL PRIMARY KEY,
        {}
    );
    '''.format(',\n'.join([f"{key} VARCHAR" for key in data.keys() if key != "contracts"] +
                          ["{}_{} VARCHAR".format("contracts", subkey) for subkey in data.get("contracts")[0].keys()]))

    # Execute the SQL statement
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")