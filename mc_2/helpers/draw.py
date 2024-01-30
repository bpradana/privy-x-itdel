import cv2
import numpy as np


def _crop_face(frame, x, y, w, h, padding=0.0, crop_size=None):
    face_width = w
    face_height = h
    side = max(face_width, face_height)
    pad = int(side * padding)
    dx = (x + (face_width - side) // 2) - pad
    dy = (y + (face_height - side) // 2) - pad
    side = side + pad * 2

    # check if the crop area is within the frame's boundaries
    if dx < 0:
        dx = 0
    if dy < 0:
        dy = 0
    if dx + side > frame.shape[1]:
        dx = frame.shape[1] - side
    if dy + side > frame.shape[0]:
        dy = frame.shape[0] - side

    cropped_face = frame[dy : dy + side, dx : dx + side]
    if crop_size is not None:
        cropped_face = cv2.resize(cropped_face, crop_size)

    return cropped_face


def _draw_bbox(frame, x, y, w, h):
    cv2.rectangle(
        frame, (x, y), (x + w, y + h), (0, 255, 0), 2
    )  # draw box to main image


def draw_bbox_face_detection(frame, face_object):
    x = face_object["facial_area"]["x"]
    y = face_object["facial_area"]["y"]
    w = face_object["facial_area"]["w"]
    h = face_object["facial_area"]["h"]

    _draw_bbox(frame, x, y, w, h)  # draw box to main image

    cv2.putText(
        frame,
        f"{face_object['confidence']*100:.2f}%",
        (x + 5, y - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )  # write confidence percentage on top of bbox


def draw_verification_result(img1, img2, result):
    x1 = result["facial_areas"]["img1"]["x"]
    y1 = result["facial_areas"]["img1"]["y"]
    w1 = result["facial_areas"]["img1"]["w"]
    h1 = result["facial_areas"]["img1"]["h"]

    x2 = result["facial_areas"]["img2"]["x"]
    y2 = result["facial_areas"]["img2"]["y"]
    w2 = result["facial_areas"]["img2"]["w"]
    h2 = result["facial_areas"]["img2"]["h"]

    _draw_bbox(img1, x1, y1, w1, h1)
    _draw_bbox(img2, x2, y2, w2, h2)

    img1 = _crop_face(img1, x1, y1, w1, h1, padding=0.2, crop_size=(512, 512))
    img2 = _crop_face(img2, x2, y2, w2, h2, padding=0.2, crop_size=(512, 512))

    frame = np.append(img1, img2, axis=1)
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]

    cv2.putText(
        frame,
        "Verified" if result["verified"] else "Not Verified",
        (int(frame_width / 2) - 50, int(frame_height / 2)),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if result["verified"] else (0, 0, 255),
        2,
    )  # write distance on top of bbox

    return frame


def draw_emotion(frame, face_object):
    x = face_object["region"]["x"]
    y = face_object["region"]["y"]
    w = face_object["region"]["w"]
    h = face_object["region"]["h"]

    emotion = face_object["dominant_emotion"]

    _draw_bbox(frame, x, y, w, h)  # draw box to main image

    cv2.putText(
        frame,
        emotion,
        (x + 5, y - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )  # write confidence percentage on top of bbox
