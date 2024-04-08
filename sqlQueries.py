import psycopg2

# Connect to your PostgreSQL database
connection = psycopg2.connect(
        user="postgres",
        password="messi10",
        host="localhost",
        port="5432",
        database="opensea_collections"
    )
# Create a cursor object
cur = connection.cursor()


#cur.execute("DROP TABLE IF EXISTS opensea_collections_data;") #execute if you want to delete table

# Add columns to a table
cur.execute("ALTER TABLE opensea_collections_data ADD COLUMN name TEXT;")

# Remove columns from a table
cur.execute("ALTER TABLE opensea_collections_data DROP COLUMN name;")

# Change data types of columns
cur.execute("ALTER TABLE opensea_collections_data ALTER COLUMN name TYPE TEXT;")

# Perform SELECT statements
cur.execute("SELECT * FROM opensea_collections_data;")

# Implement the LIMIT clause to restrict the number of returned rows
cur.execute("SELECT * FROM opensea_collections_data LIMIT 10;")

# Implement the ORDER BY clause to sort the results
cur.execute("SELECT * FROM opensea_collections_data ORDER BY name ASC;")

# Implement filtering operators like LIKE and ILIKE, IN in SELECT statements
cur.execute("SELECT * FROM opensea_collections_data WHERE name LIKE '%ethereum%';")
cur.execute("SELECT * FROM opensea_collections_data WHERE name ILIKE '%ethereum%';")
cur.execute("SELECT * FROM opensea_collections_data WHERE chain IN (ethereum, dodge);")

# Commit the transaction
connection.commit()

# Close the cursor and connection
cur.close()
connection.close()

