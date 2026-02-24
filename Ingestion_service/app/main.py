from fastapi import FastAPI
from app.utils.id_generation import IdGeneration, build_event, build_http_request
from app.ingestion.watcher import Watcher
from app.ingestion.metadata_extractor import MetaDataExtractor
from app.ocr.ocr_engine import ExtractText
from app.kafka.producer import ProducerConn
from app.logger.logger import get_logger




logger = get_logger("ingestion_service")

logger.info("Service started")
logger.error("Failed to process image")

def managment():
    images = Watcher.watch_dir()
    for image in images:
        image_details = IdGeneration.add_id(image)
        image_id = image_details['id']
        file_path = image_details['file_path']
        metadata = MetaDataExtractor.extract_metadata(file_path)
        image_text = ExtractText.extract_text_from_image(file_path)
        event = build_event(image_id, metadata, image_text)
        response = build_http_request(file_path)
        ProducerConn.send_event_to_kafka(event)
    ProducerConn.close_flush()
    return response
        
        
app = FastAPI()


@app.get("/Ingestion")
def Ingestion_service():
    try: 
        return managment()
    except Exception as e:
        return e
    



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)