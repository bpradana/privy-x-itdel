import cv2
from deepface import DeepFace

from helpers.draw import draw_bbox_face_detection

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()

        # face detection
        result = DeepFace.extract_faces(
            frame, detector_backend="yolov8", enforce_detection=False
        )

        for face in result:
            draw_bbox_face_detection(frame, face)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
