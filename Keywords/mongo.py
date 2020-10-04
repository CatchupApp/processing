import pymongo
import os

client = pymongo.MongoClient(os.environ['MONGO_URL'], connect=False)

def set_keyword_data(source, keywords_data):
    videos = (client['catchup'])['videos']

    query = {"source": source}

    if not videos.find_one(query):
        videos.insert_one({"source": source, "transcription": keywords_data})
    else:
        update = {"$set": {"transcription": keywords_data}}
        videos.update_one(query, update)
