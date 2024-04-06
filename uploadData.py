import psycopg2
import json
import psycopg2.pool


desired_fields = ['collection', 'name', 'description', 'image_url', 'owner', 'twitter_username']

# Initialize a connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1,  # Minimum number of connections
    10,  # Maximum number of connections
    user="postgres",
    password="messi10",
    host="localhost",
    port="5432",
    database="opensea_collections"
)

def upload_data(datas):
    try:
        # Acquire a connection from the connection pool
        connection = connection_pool.getconn()
        print('In Try')
        collections = datas['collections']
        # Extract only the desired fields from the JSON data
      #  data_list = json.loads(datas)
        for data in collections:
            data_to_upload = {key: data[key] for key in desired_fields if key in data}

            if 'contracts' in data:
                contracts_data = data.get("contracts", [])  # Get the value associated with "contracts", or an empty list if not found
                if contracts_data:  # Check if contracts_data is not None and not an empty list
                    # Extract subkeys from the contracts_data
                    for key, value in contracts_data[0].items():
                        data_to_upload[f"contracts_{key}"] = value
                else:
                    # Handle case when "contracts" key is present but the value is empty
                    print("No contracts data available.")
            else:
                # Handle case when "contracts" key is not present in data
                print("No contracts data available.")

            # Create a cursor object using the connection
            cursor = connection.cursor()

            # Define the SQL statement to insert data into the table
            insert_query = '''
            INSERT INTO opensea_collections_data ({}) VALUES ({});
            '''.format(','.join(data_to_upload.keys()), ','.join(['%s'] * len(data_to_upload)))

            # Execute the SQL statement to insert data into the table
            cursor.execute(insert_query, list(data_to_upload.values()))
            connection.commit()
            print("Data uploaded successfully")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # Release the connection back to the connection pool
        if connection:
            cursor.close()
            connection_pool.putconn(connection)
            print("Database connection released")