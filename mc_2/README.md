# Introduction to DeepFace


## What is DeepFace?
Deepface is a lightweight face detection, face recognition and facial attribute analysis (age, gender, emotion and race) framework for python.

## Why DeepFace?
It is a hybrid face recognition framework wrapping state-of-the-art models: VGG-Face, Google FaceNet, OpenFace, Facebook DeepFace, DeepID, ArcFace, Dlib and SFace.

## Installation
```bash
pip install deepface
```

## How to use DeepFace?
```
from deepface import DeepFace
import cv2
```

### Detecting Face
```python
path_img = "images/peter.jpg"

# read images
img_1 = cv2.imread(path_img)

# face verification
result = DeepFace.extract_faces(
    img_1, detector_backend="yolov8", enforce_detection=False
)

# display result
for face in result:
    draw_bbox_face_detection(img_1, face)

cv2.imshow("frame", img_1)
cv2.waitKey(0)
```

### Face Verification
```python
path_img_1 = "images/rdj.jpg"
path_img_2 = "images/tony.jpg"
# path_img_2 = "img3.jpg"

# read images
img_1 = cv2.imread(path_img_1)
img_2 = cv2.imread(path_img_2)

# face verification
result = DeepFace.verify(
    img_1, img_2, model_name="Facenet512", detector_backend="yolov8"
)

# display result
frame = draw_verification_result(img_1, img_2, result)
cv2.imshow("frame", frame)
cv2.waitKey(0)
```

### Emotion Detection
```python
img = cv2.imread("images/emotions.jpg")

result = DeepFace.analyze(img, detector_backend="yolov8", actions=["emotion"])

for face in result:
    draw_emotion(img, face)

cv2.imshow("frame", img)
cv2.waitKey(0)
```
