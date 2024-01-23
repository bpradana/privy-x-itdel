import cv2
from deepface import DeepFace

from helpers.draw import draw_emotion

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()

        # face detection
        result = DeepFace.analyze(
            frame,
            detector_backend="yolov8",
            actions=["emotion"],
            enforce_detection=False,
        )

        for face in result:
            draw_emotion(frame, face)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
