from celery import Celery
from PIL import Image
import requests
from io import BytesIO

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
