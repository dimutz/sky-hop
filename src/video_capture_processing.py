import cv2


def capture_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame. Exiting ...")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the resulting frame
        cv2.imshow('Test video capture', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) == ord('q'):
            break
    # When finished, release the capture
    cap.release()
    cv2.destroyAllWindows()


def main():
    capture_video()


if __name__ == '__main__':
    main()
