import cv2
from deepface import DeepFace

from helpers.draw import draw_bbox_face_detection

if __name__ == "__main__":
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
