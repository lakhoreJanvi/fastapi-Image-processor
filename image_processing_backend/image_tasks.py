from PIL import Image
import requests
from io import BytesIO
from worker import app
from database import SessionLocal
from models import ImageRequest
import os

PROCESSED_FOLDER = "processed_images"

@app.task
def process_image(request_id: int, input_urls: list):
    session = SessionLocal()
    request = session.query(ImageRequest).filter(ImageRequest.id == request_id).first()

    if not os.path.exists(PROCESSED_FOLDER):
        os.makedirs(PROCESSED_FOLDER)

    output_urls = []
    for index, url in enumerate(input_urls):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")

        output_path = f"{PROCESSED_FOLDER}/{request_id}_{index}.jpg"
        img.save(output_path, "JPEG", quality=50)

        output_urls.append(f"http://localhost:8000/{output_path}")

    request.output_urls = ",".join(output_urls)
    request.status = "Completed"
    session.commit()
    session.close()
    
    return output_urls
