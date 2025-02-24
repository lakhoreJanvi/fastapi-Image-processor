from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import pandas as pd
from database import SessionLocal, ImageRequest
from image_tasks import process_image
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """ Upload CSV file and store data in the database """
    df = pd.read_csv(file.file)

    input_urls = ",".join(df["Image URLs"].tolist())
    session = SessionLocal()
    request = ImageRequest(
        product_name="Bulk Upload",
        input_urls=input_urls,
        status="Pending"
    )
    session.add(request)
    session.commit()
    session.refresh(request)

    # Start processing asynchronously
    background_tasks.add_task(process_image, request.id, input_urls.split(","))

    return {"request_id": request.id, "message": "Processing started"}  

@app.get("/status/{request_id}")
def get_status(request_id: int):
    """ Check processing status of an image request """
    session = SessionLocal()
    request = session.query(ImageRequest).filter(ImageRequest.id == request_id).first()
    
    if request:
        return {"request_id": request.id, "status": request.status, "output_urls": request.output_urls}

    return {"error": "Request not found"}

app.mount("/processed_images", StaticFiles(directory="processed_images"), name="processed_images")
