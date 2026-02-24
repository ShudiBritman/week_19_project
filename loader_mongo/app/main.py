from fastapi import FastAPI, UploadFile, File
from app.dal.dal import load_binery_image_in_mongo
from app.logger.logger import get_logger



logger = get_logger("ingestion_service")

logger.info("Service started")
logger.error("Failed to process image")

app = FastAPI()


@app.post("/load_image")
async def upload(binary_file: UploadFile = File(...)):
    try:
        return load_binery_image_in_mongo(binary_file)
    except Exception as e:
        return e



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)