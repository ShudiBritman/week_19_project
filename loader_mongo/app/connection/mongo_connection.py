from pymongo import MongoClient
import os

def build_mongo_uri():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    if uri:
        return uri

class MongoConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = cls._connect_with_retry()
        return cls._instance

    @staticmethod
    def _connect_with_retry():
        uri = build_mongo_uri()
        client = MongoClient(uri)
        return client

    def get_client(self):
        return self.client

    def get_db(self):
        db_name = "binary_images"
        client = self.get_client()
        return client[db_name]

    def get_collection(self):
        db = self.get_db()
        return db["binary_images"]
    