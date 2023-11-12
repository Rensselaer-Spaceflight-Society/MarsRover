import cv2

class VisionInput(object):
    pass

if __name__ == "__main__":
    camera_front = cv2.VideoCapture(0)
    camera_rear = cv2.VideoCapture(1)

    ret_front, frame_front = camera_front.read()
    ret_rear, frame_rear = camera_rear.read()

    while ret_front and ret_rear:
        cv2.imshow("Front View", frame_front)
        cv2.imshow("Rear", frame_rear)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("Waiting...")