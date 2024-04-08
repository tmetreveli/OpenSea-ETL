import psycopg2

# Initialize connection and cursor to None
connection = None
cursor = None

try:
    # Establish a connection to the default 'postgres' database
    connection = psycopg2.connect(
        user="postgres",
        password="messi10",
        host="localhost",
        port="5432"
    )

    # Set autocommit to True
    connection.autocommit = True

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Create a new database
    cursor.execute("CREATE DATABASE opensea_collections;")

    print("Database created successfully")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
