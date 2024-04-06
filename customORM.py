import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

# Define the SQLAlchemy engine
engine = create_engine('postgresql://postgres:messi10@localhost:5432/opensea_collections')

# Define a base class for declarative class definitions
Base = sqlalchemy.orm.declarative_base()

# Define your SQLAlchemy model
class OpenseaCollection(Base):
    __tablename__ = 'opensea_collections_data'
    id = Column(Integer, primary_key=True)
    collection = Column(String)
    name = Column(String)
    description = Column(String)
    image_url = Column(String)
    owner = Column(String)
    twitter_username = Column(String)
    contracts_address = Column(String)
    contracts_chain = Column(String)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Read JSON data and insert into database
def upload_data(datas):
    Session = sessionmaker(bind=engine)
    session = Session()
    collections = datas['collections']
    for data in collections:
        # Extract fields from data
        collection = data.get('collection')
        name = data.get('name')
        description = data.get('description')
        image_url = data.get('image_url')
        owner = data.get('owner')
        twitter_username = data.get('twitter_username')
        contracts_data = data.get("contracts", [])  # Get the value associated with "contracts", or an empty list if not found
        if contracts_data:  # Check if contracts_data is not None and not an empty list
            contracts_data = contracts_data[0]
            contracts_address = contracts_data.get('address')
            contracts_chain = contracts_data.get('chain')
        else:
            # Handle case when "contracts" key is present but the value is empty
            print("No contracts data available.")
            contracts_address = None
            contracts_chain = None
        # Create a new OpenseaCollection object
        opensea_collection = OpenseaCollection(collection=collection, name=name, description=description,
                                               image_url=image_url, owner=owner, twitter_username=twitter_username,
                                               contracts_address=contracts_address, contracts_chain=contracts_chain)

        # Add the object to the session
        session.add(opensea_collection)

    # Commit the session to save changes to the database
    session.commit()

    # Close the session
    session.close()