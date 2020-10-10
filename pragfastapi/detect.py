## https://medium.com/swlh/real-time-object-detection-deployment-using-tensorflow-keras-and-aws-ec2-instance-1c1937c001d9

import urllib.request
import requests
import numpy as np

video_url = "http://127.0.0.1:8000/video"
fastapi_post_url = "http://127.0.0.1:4040/predict/"

num_cars = -999

while True:
  imgResp = urllib.request.urlopen(video_url)
  print(imgResp)
  imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
  print(imgNp)

  try:
   r = requests.post(fastapi_post_url, files={'file':imgNp})
   print(r)
   print(r.json())
   # num_cars = r.json()['num_cars']
  except Exception as e:
   pass
   print("Error: ",e)
  # print(f'Number of cars in the image is {num_cars}')
