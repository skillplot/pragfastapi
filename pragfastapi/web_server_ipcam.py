## https://medium.com/swlh/real-time-object-detection-deployment-using-tensorflow-keras-and-aws-ec2-instance-1c1937c001d9

import sys, os
import io

from fastapi import FastAPI, UploadFile, File
from starlette.requests import Request

from pydantic import BaseModel

import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import numpy as np


app = FastAPI()


class ImageType(BaseModel):
  url: str


@app.get("/")
def home():
  return "Home"


@app.post("/predict/") 
def prediction(request: Request, 
  file: bytes = File(...)):
  if request.method == "POST":
      image_stream = io.BytesIO(file)
      image_stream.seek(0)
      file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
      frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
      bbox, label, conf = cv.detect_common_objects(frame)
      output_image = draw_bbox(frame, bbox, label, conf)
      num_cars = label.count('car')
      print('Number of cars in the image is '+ str(num_cars))
      return {"num_cars":num_cars}
  return "No post request found"

## gunicorn -w 4 -k uvicorn.workers.UvicornWorker myApp:app
