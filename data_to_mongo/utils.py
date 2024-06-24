# 1st part upserting the data from local to mongodb
#feature pipeline
import pymongo
import os

client=pymongo.MongoClient(os.getenv("MONGODB_CREDENTIALS"))

class EnvironmentVariables(object):
    def __init__(self):
        # environemt variables
        self.data_file_path=os.getenv("DATA_FILE_NAME")
        self.database_name=os.getenv("DATABASE_NAME")
        self.collection_name=os.getenv("COLLECTION_NAME")

env=EnvironmentVariables()
