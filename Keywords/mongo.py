import pymongo
import os

client = pymongo.MongoClient(os.environ['MONGO_URL'])

# database level
db = client['catchup']

# collection level
catchup = db['catchup']

def set_keyword_data(source, keywords_data):
    query = {"source": source}

    if not catchup.find_one(query):
        catchup.insert_one({"source": source, "keywords": keywords_data})
    else:
        update = {"$set": {"keywords": keywords_data}}
        catchup.update_one(query, update)
