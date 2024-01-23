import cv2
from deepface import DeepFace

from helpers.draw import draw_emotion

if __name__ == "__main__":
    img = cv2.imread("images/emotions.jpg")

    result = DeepFace.analyze(img, detector_backend="yolov8", actions=["emotion"])

    for face in result:
        draw_emotion(img, face)

    cv2.imshow("frame", img)
    cv2.waitKey(0)
