## Copyright (c) 2020 mangalbhaskar.
"""FastAPI based main application server.

https://fastapi.tiangolo.com/advanced/custom-response/
https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
https://techtutorialsx.com/2020/04/23/python-opencv-converting-camera-video-to-black-and-white/

cvlib with face_detection
https://www.analyticsvidhya.com/blog/2018/12/introduction-face-detection-video-deep-learning-python/
"""
__author__ = 'mangalbhaskar'


import io
import glob
import time

import fastapi
from fastapi.responses import StreamingResponse
# from fastapi.responses import FileResponse

from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

video_path = "data/videos/video.mp4"
video_path_big = "data/videos/big.mp4"
video_path_huge = "data/videos/4k.mp4"

image_basepath = 'data/images'
imagelist = glob.glob(image_basepath+'**/*.*')


def get_image():
  for f in imagelist:
    frame = open(f, 'rb').read()
    time.sleep(2)
    ## yield frame
    yield (b'--frame\r\n' b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
    ## yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def get_frame(show_edges=False):
  """Video streaming generator function."""
  import cv2
  import numpy as np

  # cap = cv2.VideoCapture(-1)
  cap = cv2.VideoCapture('/dev/video0')

  if not cap.isOpened():
    raise RuntimeError('Could not start camera.')

  ## configure camera for 720p @ 60 FPS
  ## https://elder.dev/posts/open-source-virtual-background/

  height, width = 720, 1280
  # cap.set(cv2.CAP_PROP_FRAME_WIDTH ,width)
  # cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
  cap.set(cv2.CAP_PROP_FPS, 30)
  while True:
    _, img = cap.read()

    frame = cv2.imencode('.jpg', img)[1].tobytes()
    if show_edges:
      ## converting BGR to HSV 
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
      ## define range of red color in HSV 
      lower_red = np.array([30,150,50]) 
      upper_red = np.array([255,255,180]) 
      ## create a red HSV colour boundary and 
      ## threshold HSV image 
      mask = cv2.inRange(hsv, lower_red, upper_red) 
      ## Bitwise-AND mask and original image 
      res = cv2.bitwise_and(img, img, mask= mask) 
      ## finds edges in the input image image and 
      ## marks them in the output map edges 
      edges = cv2.Canny(img, 100, 200) 
      # frame = cv2.imencode('.jpg', np.hstack(( np.stack((edges,edges,edges)), img)))[1].tobytes()
      frame = cv2.imencode('.jpg', edges)[1].tobytes()
      # frame = cv2.imencode('.jpg', np.hstack((edges, edges)))[1].tobytes()
      # frame = cv2.imencode('.jpg', np.hstack((edges, edges, edges)))[1].tobytes()
      # frame = cv2.imencode('.jpg', np.vstack((edges, edges, edges)))[1].tobytes()
      # frame = cv2.imencode('.jpg', np.hstack((np.vstack((edges, edges)), np.vstack((edges, edges))))   )[1].tobytes()
      # frame = cv2.imencode( '.jpg', np.hstack(np.vstack((edges, edges)), np.vstack((edges, edges))) )[1].tobytes()
      # cv2.imwrite("test.jpg", edges)
    else:
      frame = cv2.imencode('.jpg', img)[1].tobytes()

    yield (b'--frame\r\n'
           b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')


def detect_face_from_frame():
  """Video streaming generator function."""
  import cv2
  import numpy as np
  import face_recognition

  # cap = cv2.VideoCapture(-1)
  cap = cv2.VideoCapture('/dev/video0')
  if not cap.isOpened():
    raise RuntimeError('Could not start camera.')
  ## configure camera for 720p @ 60 FPS
  ## https://elder.dev/posts/open-source-virtual-background/

  height, width = 720, 1280
  # cap.set(cv2.CAP_PROP_FRAME_WIDTH ,width)
  # cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
  cap.set(cv2.CAP_PROP_FPS, 30)
  face_locations = []

  while True:
    _, img = cap.read()
    face_detection = True
    if face_detection:
      # pip install dlib
      # pip install face_recognition

      ## Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
      frame = img[:, :, ::-1]
      # frame = img

      ## Find all the faces in the current frame of video
      face_locations = face_recognition.face_locations(frame)
      print('face_locations', face_locations)
      ## Display the results
      for top, right, bottom, left in face_locations:
        # Draw a box around the face
        frame = cv2.cvtColor(np.float32(frame), cv2.COLOR_RGB2GRAY)
        # frame = cv2.cvtColor(np.float32(img), cv2.COLOR_RGB2GRAY)
        # frame = cv2.cvtColor(cv2.UMat(img), cv2.COLOR_RGB2GRAY)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    frame = cv2.imencode('.jpg', frame)[1].tobytes()

    yield (b'--frame\r\n'
           b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')


## https://stackoverflow.com/questions/62359413/how-to-return-an-image-in-fastapi
@app.post("/image/similar")
async def image_similarity(
  file: UploadFile = File(...)
  ,file1: UploadFile = File(...)
  ):
  import numpy as np
  # from cv2 import *
  import base64

  content = await file.read()
  nparr = np.fromstring(content, np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

  content1 = await file1.read()
  nparr1 = np.fromstring(content1, np.uint8)
  img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)

  akaze = cv2.AKAZE_create()
  kpts1, desc1 = akaze.detectAndCompute(img, None)
  kpts2, desc2 = akaze.detectAndCompute(img1, None)
  matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
  matches_1 = matcher.knnMatch(desc1, desc2, 2)
  good_points = []
  for m,n in matches_1:
    if m.distance < 0.7 * n.distance:
      good_points.append(m)
  mat = (round(len(kpts2)/len(good_points),2))

  return_img = cv2.processImage(img)
  _, encoded_img = cv2.imencode('.PNG', return_img)
  encoded_img = base64.b64encode(return_img)

  yield (b'--frame\r\n'
         b'Content-Type: image/jpg\r\n\r\n' + endcoded_img + b'\r\n')

  # return {"The similarity is": mat,'encoded_img': endcoded_img}



app = fastapi.FastAPI(
  title='Streaming - Camera, Video, Images'
  ,description='FastAPI based streaming server for ML'
)

app.add_middleware(
  CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def main():
  return {"message":"Streaming server using FastAPI"}


@app.get("/cam", tags=['camera'])
def stream_cam():
  # return StreamingResponse(get_frame())
  return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.get("/edges", tags=['camera'])
def stream_cam_with_edge_detection():
  # return StreamingResponse(get_frame())
  return StreamingResponse(get_frame(show_edges=True), media_type='multipart/x-mixed-replace; boundary=frame')


@app.get("/face", tags=['camera'])
def stream_cam_with_face_detection():
  return StreamingResponse(detect_face_from_frame(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.get("/images", tags=['image'])
async def stream_image():
  return StreamingResponse(get_image(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.get("/video", tags=['video'])
def stream_video():
  vfile = open(video_path, mode="rb")
  return StreamingResponse(vfile, media_type="video/mp4")


@app.get("/video_async", tags=["video"])
async def stream_video_async():
  return FileResponse(video_path_big, media_type="video/mp4")
  # return FileResponse(video_path_big)


@app.get("/video_4k", tags=["video"])
async def stream_video_async_4k():
  return FileResponse(video_path_huge, media_type="video/mp4")
  # return FileResponse(video_path_huge)



# @app.post("/vector_image")
# def image_endpoint(*, vector):
#   """
#   Returns a cv2 image array from the document vector

#   @reference
#   https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
#   """
#   import cv2
#   cv2img = my_function(vector)
#   res, im_png = cv2.imencode(".png", cv2img)
#   return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


# import tempfile

# @app.post("/vector_image2")
# def image_endpoint2(*, vector):
#   # Returns a raw PNG from the document vector (define here)
#   img = my_function(vector)

#   with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=False) as FOUT:
#     FOUT.write(img)
#     return FileResponse(FOUT.name, media_type="image/png")

# @app.get("/generate")
# def generate(data: str):
#   img = generate_image(data)
#   print('img=%s' % (img.shape,))
#   buf = BytesIO()
#   imsave(buf, img, format='JPEG', quality=100)
#   buf.seek(0) # important here!
#   return StreamingResponse(buf, media_type="image/jpeg",
#     headers={'Content-Disposition': 'inline; filename="%s.jpg"' %(data,)})

## Todo: work in progress
# @app.get("/file", tags=['file'])
# def stream_file():
#   file_like = open(some_file_path, mode="rb")
#   return StreamingResponse(some_generator, media_type='application/json')
