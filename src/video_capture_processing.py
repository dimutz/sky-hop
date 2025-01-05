import cv2
import mediapipe as mp
from character import Character
from frame_handler import draw_landmarks_on_image, get_index_fingertip_position


def capture_video_demo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    detector = mp.solutions.hands.Hands(max_num_hands=1,
                                        min_detection_confidence=0.5,
                                        min_tracking_confidence=0.5)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # If frame is read correctly ret is True
        if not ret:
            print("Can't receive frame. Exiting ...")
            break
        # Convert frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Detect hand landmarks
        results = detector.process(rgb_frame)
        # Pass the detection results to the drawing function
        if results.multi_hand_landmarks:
            processed_frame = draw_landmarks_on_image(rgb_frame, results)
        # Display the processed frame
        cv2.imshow("Test Hand Landmark",
                   cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) == ord('q'):
            break
    # When finished, release the capture
    cap.release()
    cv2.destroyAllWindows()


def capture_video(character: Character, cap, detector):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame. Exiting ...")
        return
    # Convert frame to RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Detect hand landmarks
    results = detector.process(rgb_frame)
    # Pass the detection results to the tracking function
    if results.multi_hand_landmarks:
        new_x = get_index_fingertip_position(rgb_frame, results)
        if new_x != -1:
            character.handle_motion(new_x)


def main():
    capture_video_demo()


if __name__ == '__main__':
    main()
