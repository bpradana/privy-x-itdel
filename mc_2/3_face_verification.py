import cv2
from deepface import DeepFace

from helpers.draw import draw_verification_result

if __name__ == "__main__":
    path_img_1 = "images/jeremy1.jpg"
    path_img_2 = "images/jeremy2.jpg"
    path_img_2 = "images/james.jpg"

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
