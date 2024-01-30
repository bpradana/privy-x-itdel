import cv2
import numpy as np

if __name__ == "__main__":
    # # reading image
    # image = cv2.imread("path/to/image.jpg")

    # # reading video from webcam
    # cap = cv2.VideoCapture(0)
    # while True:
    #     _, frame = cap.read()
    #     cv2.imshow("frame", frame)
    #     if cv2.waitKey(1) & 0xFF == ord("q"):
    #         break

    # # drawing rectangle
    # cv2.rectangle(
    #     img=image,
    #     pt1=(100, 100),
    #     pt2=(200, 200),
    #     color=(0, 255, 0),
    #     thickness=2,
    # )

    # drawing text
    image = np.zeros((512, 512, 3), np.uint8)
    cv2.putText(
        img=image,
        text="Hello World",
        org=(0, 0),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        color=(0, 255, 0),
        thickness=2,
    )
    cv2.imshow("image", image)
    cv2.waitKey(0)
