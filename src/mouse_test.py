import cv2
import mediapipe as mp
import pyautogui

from gesture_detector import detect_gesture
from gesture_state import GestureState
from mouse_controller import MouseController


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
    print("ERROR: Camera could not be opened.")
    exit()


gesture_state = GestureState(
    history_size=7,
    required_frames=5
)

mouse = MouseController(smoothing=0.20)

mouse_mode = False

print("GestureX Mouse Test")
print("-------------------")
print("☝️  One Finger = Mouse Mode")
print("✊  Fist = Exit Mouse Mode")
print("👍  Thumbs Up = Left Click")
print("Press Q = Quit")


while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

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

        # =====================================
        # MOUSE MOVEMENT
        # =====================================

        if mouse_mode:

            index_tip = hand_landmarks.landmark[8]

            mouse.move_to(
                index_tip.x,
                index_tip.y
            )

    else:

        gesture_state.reset()

    # =========================================
    # STABLE GESTURE
    # =========================================

    confirmed = gesture_state.update(
        detected_gesture
    )

    if confirmed:

        print("Confirmed:", confirmed)

        # One finger → enter mouse mode
        if confirmed == "ONE FINGER":

            mouse_mode = True

            print(">>> MOUSE MODE ON")

        # Fist → exit mouse mode
        elif confirmed == "FIST":

            mouse_mode = False

            print(">>> MOUSE MODE OFF")

        # Thumbs up → click
        elif confirmed == "THUMBS UP":

            if mouse_mode:

                print(">>> LEFT CLICK")

                mouse.click()

    # =========================================
    # UI
    # =========================================

    mode_text = (
        "MOUSE MODE ON"
        if mouse_mode
        else "MOUSE MODE OFF"
    )

    cv2.rectangle(
        frame,
        (10, 10),
        (500, 100),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        f"Gesture: {detected_gesture}",
        (25, 43),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        mode_text,
        (25, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 0) if mouse_mode else (0, 0, 255),
        2
    )

    cv2.imshow(
        "GestureX - Mouse Control",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
hands.close()
cv2.destroyAllWindows()