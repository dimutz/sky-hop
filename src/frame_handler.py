import math

import cv2
import numpy as np
from mediapipe import solutions

MARGIN = 10
FONT_SIZE = 0.8
FONT_THICKNESS = 1
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
CYAN_COLOR = (0, 255, 240)


def draw_landmarks_on_image(rgb_image: np.ndarray, results):
    annotated_image = np.copy(rgb_image)
    if results.multi_hand_landmarks:
        # Only tracking 1 hand at a time
        hand_landmarks = results.multi_hand_landmarks[0]
        # Get image dimensions
        image_rows, image_cols, _ = rgb_image.shape
        # Index tip landmark no. according to documentation
        index_tip_landmark = hand_landmarks.landmark[8]
        # Check for minimum visibility and presence
        if ((index_tip_landmark.HasField('visibility') and
             index_tip_landmark.visibility < 0.5) or
                (index_tip_landmark.HasField('presence') and
                 index_tip_landmark.presence < 0.5)):
            return annotated_image
        # Check for normalized values
        if (0 < index_tip_landmark.x < 1 and
                0 < index_tip_landmark.y < 1):
            # Get pixel coordinates
            x_px = min(math.floor(index_tip_landmark.x * image_cols), image_cols - 1)
            y_px = min(math.floor(index_tip_landmark.y * image_rows), image_rows - 1)
            landmark_px = (x_px, y_px)
            drawing_spec = solutions.drawing_utils.DrawingSpec(color=CYAN_COLOR)
            # Draw index tip landmark
            circle_border_radius = max(drawing_spec.circle_radius + 1,
                                       int(drawing_spec.circle_radius * 1.2))
            cv2.circle(annotated_image, landmark_px, circle_border_radius, WHITE_COLOR,
                       drawing_spec.thickness)
            cv2.circle(annotated_image, landmark_px, drawing_spec.circle_radius,
                       drawing_spec.color, drawing_spec.thickness)
            # Draw coordinates of index fingertip
            cv2.putText(annotated_image, f"x={hand_landmarks.landmark[8].x:.4f}",
                        (0, rgb_image.shape[0] // 2), cv2.FONT_HERSHEY_TRIPLEX,
                        FONT_SIZE, BLACK_COLOR, FONT_THICKNESS, cv2.LINE_AA)
    return annotated_image
