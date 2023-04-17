# importing Mongoclient from pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
from datetime import datetime
from settings import settings

no_db = settings.no_db

# Making Connection
if not no_db:
    myclient = MongoClient(settings.connection_string, tlsCAFile=certifi.where())
    db = myclient[settings.db_name]

def insert_word(word, description, lang="en"):
    if no_db:
        return
    record = {"_id": word,
              "word": word,
              "description": description}
    if lang == "it":
        collection = db["words_it"]
    else:
        collection = db["words"]
    collection.update_one({'_id': record['_id']}, {'$set': record, '$inc': {'popularity': 1}, '$setOnInsert': {'creation_time': datetime.now()}}, upsert=True)

def get_word(word, lang="en"):
    if no_db:
        return
    if lang == "it":
        collection = db["words_it"]
    else:
        collection = db["words"]
    result = collection.find_one({'_id': word})
    return eval(str(result["description"]).replace("', '",'", "').replace(".", "").replace("}{", ",").replace("]", "}").replace("}[", ",").replace(".", "").replace("} {", ",").replace(";", ",").replace("{'", '{"').replace("""": '""", '": "').replace('''': "''', '": "').replace("""", '""", '", "').replace('''': "''', '", "').replace("'}", '"}').replace("': '", '": "').replace("', '", '", "')) if result else {}


def get_words_user(lang="en"):
    if no_db:
        return
    if lang == "it":
        collection = db["words_it"]
    else:
        collection = db["words"]
    results = collection.find().sort("creation_time", -1).limit(32)
    return [result["word"] for result in results]