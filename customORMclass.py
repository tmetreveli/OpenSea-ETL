import psycopg2


class Database:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


# Database configuration
db_config = {
    "user": "postgres",
    "password": "messi10",
    "host": "localhost",
    "port": "5432",
    "database": "opensea_collections"
}

# Creating a global database connection
db = Database(db_config)


class Model:
    __tablename__ = None

    def __init__(self, **fields):
        self.fields = fields

    @classmethod
    def create(cls, **kwargs):
        fields = ', '.join(kwargs.keys())
        values = tuple(kwargs.values())
        placeholders = ', '.join(['%s'] * len(kwargs))
        query = f"INSERT INTO {cls.__tablename__} ({fields}) VALUES ({placeholders})"
        db.execute(query, values)
        db.commit()

    @classmethod
    def all(cls, limit=None, order_by=None):
        query = f"SELECT * FROM {cls.__tablename__}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        cursor = db.execute(query)
        columns = [col[0] for col in cursor.description]
        return [cls(**dict(zip(columns, row))) for row in cursor.fetchall()]

    @classmethod
    def filter(cls, **conditions):
        condition_strings = [f"{field} = %s" for field in conditions]
        query = f"SELECT * FROM {cls.__tablename__} WHERE {' AND '.join(condition_strings)}"
        cursor = db.execute(query, tuple(conditions.values()))
        columns = [col[0] for col in cursor.description]
        return [cls(**dict(zip(columns, row))) for row in cursor.fetchall()]

class OpenseaCollection(Model):
    __tablename__ = 'opensea_collections_data'

# Creating a new record
OpenseaCollection.create(name="New Collection", description="This is a new collection")

# Retrieving all records with optional limit and order
collections = OpenseaCollection.all(limit=10, order_by='name ASC')
for collection in collections:
    print(collection.fields)

# Filtering records
filtered_collections = OpenseaCollection.filter(name="New Collection")
for collection in filtered_collections:
    print(collection.fields)

db.close()
