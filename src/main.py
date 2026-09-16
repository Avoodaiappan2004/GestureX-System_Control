import cv2
import mediapipe as mp

from gesture_detector import detect_gesture
from gesture_state import GestureState


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()


gesture_state = GestureState(
    history_size=7,
    required_frames=5
)


confirmed_gesture = "NO HAND"


while True:

    success, frame = cap.read()

    if not success:
        print("ERROR: Could not read camera frame.")
        break

    # Mirror view
    frame = cv2.flip(frame, 1)

    # BGR -> RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    detected_gesture = "NO HAND"

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        detected_gesture, fingers = detect_gesture(
            hand_landmarks
        )

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

    else:

        gesture_state.reset()

    # -----------------------------------------
    # Stable gesture detection
    # -----------------------------------------

    new_confirmed = gesture_state.update(
        detected_gesture
    )

    if new_confirmed is not None:

        confirmed_gesture = new_confirmed

        print(
            f"Confirmed Gesture: {confirmed_gesture}"
        )

    # -----------------------------------------
    # Display detected gesture
    # -----------------------------------------

    cv2.rectangle(
        frame,
        (10, 10),
        (620, 95),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        f"Detected: {detected_gesture}",
        (25, 43),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Confirmed: {confirmed_gesture}",
        (25, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "GestureX - Stable Gesture Detection",
        frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
hands.close()
cv2.destroyAllWindows()