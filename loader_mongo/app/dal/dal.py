from app.connection.mongo_connection import MongoConnection
from gridfs import GridFS
from fastapi import UploadFile

def get_db():
    return MongoConnection().get_db()


def load_binery_image_in_mongo(binary_file: UploadFile):
    db = get_db()
    gfs = GridFS(db)
    file_bytes = binary_file.file.read()

    print(len(file_bytes))

    gfs.put(file_bytes)
    return {"status":"ok"}