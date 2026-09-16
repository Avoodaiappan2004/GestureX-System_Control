# import cv2
# import mediapipe as mp
# import time

# from gesture_detector import detect_gesture
# from gesture_state import GestureState
# from mouse_controller import MouseController
# from scroll_controller import ScrollController

# last_click_time = 0
# double_click_window = 0.45

# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils


# hands = mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=1,
#     min_detection_confidence=0.6,
#     min_tracking_confidence=0.6
# )

# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("ERROR: Camera could not be opened.")
#     exit()


# gesture_state = GestureState(
#     history_size=7,
#     required_frames=5
# )

# mouse = MouseController(smoothing=0.20)
# scroll = ScrollController()

# mode = "NONE"

# print()
# print("========== GestureX System Control ==========")
# print("☝️  ONE FINGER  -> Mouse Mode")
# print("✌️  TWO FINGERS -> Scroll Mode")
# print("👍 THUMBS UP    -> Left Click")
# print("✊  FIST        -> Exit Mode")
# print("👎 THUMBS DOWN  -> Cancel / Exit")
# print("Q              -> Quit")
# print("=============================================")
# print()


# while True:

#     success, frame = cap.read()

#     if not success:
#         break

#     frame = cv2.flip(frame, 1)

#     rgb = cv2.cvtColor(
#         frame,
#         cv2.COLOR_BGR2RGB
#     )

#     results = hands.process(rgb)

#     detected_gesture = "NO HAND"

#     if results.multi_hand_landmarks:

#         hand_landmarks = results.multi_hand_landmarks[0]

#         detected_gesture, fingers = detect_gesture(
#             hand_landmarks
#         )

#         mp_draw.draw_landmarks(
#             frame,
#             hand_landmarks,
#             mp_hands.HAND_CONNECTIONS
#         )

#         # ======================================
#         # MOUSE MODE
#         # ======================================

#         if mode == "MOUSE":

#            if detected_gesture == "ONE FINGER":

#             index_tip = hand_landmarks.landmark[8]

#             mouse.move_to(
#                 index_tip.x,
#                 index_tip.y
#             )

#         # ======================================
#         # SCROLL MODE
#         # ======================================

#         elif mode == "SCROLL":

#            lm = hand_landmarks.landmark
#            palm_y = (
#             lm[0].y +
#             lm[5].y +
#             lm[9].y +
#             lm[17].y
#             ) / 4
#            scroll.update(palm_y)

#     else:

#         gesture_state.reset()

#         scroll.reset()

#     # ==========================================
#     # STABLE GESTURE
#     # ==========================================

#     confirmed = gesture_state.update(
#         detected_gesture
#     )

#     if confirmed:

#         print("Confirmed:", confirmed)

#         # --------------------------------------
#         # ONE FINGER
#         # --------------------------------------

#         if confirmed == "ONE FINGER":

#             mode = "MOUSE"
#             scroll.reset()

#             print(">>> MOUSE MODE")

#         # --------------------------------------
#         # TWO FINGERS
#         # --------------------------------------

#         elif confirmed == "TWO FINGERS":

#             mode = "SCROLL"
#             scroll.reset()

#             print(">>> SCROLL MODE")

#         # --------------------------------------
#         # FIST
#         # --------------------------------------

#         elif confirmed == "FIST":

#             mode = "NONE"
#             scroll.reset()

#             print(">>> CONTROL MODE OFF")

#         # --------------------------------------
#         # THUMBS DOWN
#         # --------------------------------------

#         elif confirmed == "THUMBS DOWN":

#             if mode == "MOUSE":

#                 print(">>> RIGHT CLICK")

#                 mouse.right_click()

#             else:

#                 mode = "NONE"
#                 scroll.reset()

#                 print(">>> CANCELLED")

#         # --------------------------------------
#         # THUMBS UP
#         # --------------------------------------

#         elif confirmed == "THUMBS UP":

#             if mode == "MOUSE":

#                 now = time.time()

#                 # Second thumbs-up within the time window
#                 if now - last_click_time <= double_click_window:

#                     print(">>> DOUBLE CLICK")

#                     mouse.double_click()

#                     # Reset so another thumbs-up starts fresh
#                     last_click_time = 0

#                 else:

#                     print(">>> LEFT CLICK")

#                     mouse.click()

#                     last_click_time = now

#     # ==========================================
#     # DISPLAY
#     # ==========================================

#     cv2.rectangle(
#         frame,
#         (10, 10),
#         (560, 115),
#         (0, 0, 0),
#         -1
#     )

#     cv2.putText(
#         frame,
#         f"Gesture: {detected_gesture}",
#         (25, 43),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.75,
#         (255, 255, 255),
#         2
#     )

#     cv2.putText(
#         frame,
#         f"Mode: {mode}",
#         (25, 80),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.75,
#         (0, 255, 0),
#         2
#     )

#     cv2.putText(
#         frame,
#         "Q = Quit",
#         (25, 107),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.5,
#         (200, 200, 200),
#         1
#     )

#     cv2.imshow(
#         "GestureX - System Controller",
#         frame
#     )

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break


# cap.release()
# hands.close()
# cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import time
import keyboard

from gesture_detector import detect_gesture
from gesture_state import GestureState
from mouse_controller import MouseController
from scroll_controller import ScrollController
from game_controller import GameController


# ============================================================
# SETTINGS
# ============================================================

last_click_time = 0
double_click_window = 0.45

# Game steering dead-zone
LEFT_ZONE = 0.38
RIGHT_ZONE = 0.62


# ============================================================
# MEDIAPIPE
# ============================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
# LEFT_ZONE = 0.38
# RIGHT_ZONE = 0.62

# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERROR: Camera could not be opened.")

    exit()


# ============================================================
# GESTURE STABILITY
# ============================================================

gesture_state = GestureState(
    history_size=7,
    required_frames=5
)


# ============================================================
# CONTROLLERS
# ============================================================

mouse = MouseController(
    smoothing=0.20
)

scroll = ScrollController()

game = GameController()


# ============================================================
# MODE
# ============================================================

mode = "NONE"


# ============================================================
# START MESSAGE
# ============================================================

print()
print("======================================================")
print("                 GESTUREX CONTROLLER")
print("======================================================")

print()
print("MODE CONTROL")
print("----------------------------")
print("F1  -> SYSTEM MODE")
print("F2  -> GAME MODE")
print("ESC -> EMERGENCY STOP")
print("Q   -> QUIT")
print()

print("SYSTEM MODE")
print("----------------------------")
print("ONE FINGER   -> Mouse")
print("TWO FINGERS  -> Scroll")
print("THUMBS UP    -> Left Click")
print("THUMBS DOWN  -> Right Click")
print("FIST         -> Stop current control")
print()

print("GAME MODE")
print("----------------------------")
print("OPEN PALM    -> Accelerate / UP")
print("FIST         -> Brake / DOWN")
print("ONE FINGER   -> Left / Right steering")
print("THUMBS UP    -> Space / Action")
print("THUMBS DOWN  -> Exit Game Mode")
print()

print("======================================================")
print()


# ============================================================
# HELPER: CHANGE MODE
# ============================================================

def set_mode(new_mode):

    global mode

    # Release everything before changing modes
    game.release_all()

    scroll.reset()

    # Clear previous gesture history
    gesture_state.reset()

    mode = new_mode

    print()
    print("====================================")

    if mode == "SYSTEM":
        print(">>> SYSTEM MODE ON")

    elif mode == "GAME":
        print(">>> GAME MODE ON")

    else:
        print(">>> NO CONTROL MODE")

    print("====================================")
    print()


# ============================================================
# MAIN LOOP
# ============================================================

try:

    while True:

        # ====================================================
        # KEYBOARD MODE SELECTION
        # ====================================================

        if keyboard.is_pressed("f1"):

            if mode != "SYSTEM":
                set_mode("SYSTEM")


        elif keyboard.is_pressed("f2"):

            if mode != "GAME":
                set_mode("GAME")


        elif keyboard.is_pressed("esc"):

            set_mode("NONE")

            print(">>> EMERGENCY STOP")


        # ====================================================
        # CAMERA
        # ====================================================

        success, frame = cap.read()

        if not success:
            print("ERROR: Could not read camera frame.")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # BGR -> RGB
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ====================================================
        # MEDIAPIPE
        # ====================================================

        results = hands.process(rgb)

        detected_gesture = "NO HAND"

        hand_landmarks = None


        # ====================================================
        # HAND DETECTED
        # ====================================================

        if results.multi_hand_landmarks:

            hand_landmarks = (
                results.multi_hand_landmarks[0]
            )

            detected_gesture, fingers = detect_gesture(
                hand_landmarks
            )

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


        else:

            # ------------------------------------------------
            # NO HAND
            # ------------------------------------------------

            gesture_state.reset()

            scroll.reset()

            # Never leave game keys pressed
            if mode == "GAME":
                game.release_all()


        # ====================================================
        # SYSTEM MODE - REAL-TIME CONTROL
        # ====================================================

        # ====================================================
# SYSTEM MODE - REAL-TIME CONTROL
# ====================================================

        if (
            mode == "SYSTEM"
            and hand_landmarks is not None
        ):

            # =================================================
            # ONE FINGER -> MOUSE
            # =================================================

            if detected_gesture == "ONE FINGER":

                index_tip = hand_landmarks.landmark[8]

                mouse.move_to(
                    index_tip.x,
                    index_tip.y
                )


            # =================================================
            # TWO FINGERS -> VERTICAL + HORIZONTAL SCROLL
            # =================================================

            elif detected_gesture == "TWO FINGERS":

                lm = hand_landmarks.landmark

                # ---------------------------------------------
                # PALM CENTER X
                # ---------------------------------------------

                palm_x = (
                    lm[0].x +
                    lm[5].x +
                    lm[9].x +
                    lm[17].x
                ) / 4

                # ---------------------------------------------
                # PALM CENTER Y
                # ---------------------------------------------

                palm_y = (
                    lm[0].y +
                    lm[5].y +
                    lm[9].y +
                    lm[17].y
                ) / 4

                # ---------------------------------------------
                # UPDATE SCROLL
                # ---------------------------------------------

                scroll.update(
                    palm_x,
                    palm_y
                )

        # ====================================================
        # GAME MODE - REAL-TIME CONTROL
        # ====================================================

        # ====================================================
# GAME MODE - REAL-TIME CONTROL
# ====================================================

        elif (
            mode == "GAME"
            and hand_landmarks is not None
        ):

            # =================================================
            # OPEN PALM
            # ACCELERATE + STEER
            # =================================================

            if detected_gesture == "OPEN PALM":

                # Keep UP pressed continuously
                game.hold("up")

                lm = hand_landmarks.landmark

                # ---------------------------------------------
                # Palm center X
                # ---------------------------------------------

                palm_x = (
                    lm[0].x +
                    lm[5].x +
                    lm[9].x +
                    lm[17].x
                ) / 4

                # ---------------------------------------------
                # LEFT
                # ---------------------------------------------

                if palm_x < LEFT_ZONE:

                    game.release("right")
                    game.hold("left")


                # ---------------------------------------------
                # RIGHT
                # ---------------------------------------------

                elif palm_x > RIGHT_ZONE:

                    game.release("left")
                    game.hold("right")


                # ---------------------------------------------
                # CENTER / STRAIGHT
                # ---------------------------------------------

                else:

                    game.release("left")
                    game.release("right")


            # =================================================
            # FIST
            # BRAKE
            # =================================================

            elif detected_gesture == "FIST" or detected_gesture == "THUMBS DOWN":

                game.release("up")

                game.release("left")
                game.release("right")

                game.hold("down")


            # =================================================
            # THUMBS UP
            # Don't move the car
            # Action handled below after confirmation
            # =================================================

            elif detected_gesture == "THUMBS UP":

                game.release_movement()


            # =================================================
            # THUMBS DOWN
            # Exit handled below
            # =================================================

            # elif detected_gesture == "THUMBS DOWN":

            #     game.release_movement()


            # =================================================
            # OTHER / UNKNOWN
            # =================================================

            else:

                game.release_movement()
        # ====================================================
        # STABLE GESTURE
        # ====================================================

        confirmed = gesture_state.update(
            detected_gesture
        )


        if confirmed is not None:

            print(
                f"Confirmed: {confirmed}"
            )


            # =================================================
            # SYSTEM MODE ACTIONS
            # =================================================

            if mode == "SYSTEM":


                # =============================================
                # THUMBS UP -> LEFT CLICK / DOUBLE CLICK
                # =============================================

                if confirmed == "THUMBS UP":

                    now = time.time()


                    # -----------------------------------------
                    # DOUBLE CLICK
                    # -----------------------------------------

                    if (
                        now - last_click_time
                        <= double_click_window
                    ):

                        print(
                            ">>> DOUBLE CLICK"
                        )

                        mouse.double_click()

                        last_click_time = 0


                    # -----------------------------------------
                    # SINGLE CLICK
                    # -----------------------------------------

                    else:

                        print(
                            ">>> LEFT CLICK"
                        )

                        mouse.click()

                        last_click_time = now


                # =============================================
                # THUMBS DOWN -> RIGHT CLICK
                # =============================================

                elif confirmed == "THUMBS DOWN":

                    print(
                        ">>> RIGHT CLICK"
                    )

                    mouse.right_click()


                # =============================================
                # FIST -> STOP
                # =============================================

                elif confirmed == "FIST":

                    scroll.reset()

                    print(
                        ">>> SYSTEM CONTROL STOPPED"
                    )


            # =================================================
            # GAME MODE ACTIONS
            # =================================================

            elif mode == "GAME":


                # =============================================
                # THUMBS UP -> SPACE
                # =============================================

                if confirmed == "THUMBS UP":

                    print(
                        ">>> GAME ACTION: SPACE"
                    )

                    game.action()


                # =============================================
                # THUMBS DOWN -> EXIT GAME MODE
                # =============================================

                elif confirmed == "THUMBS DOWN":

                    game.release_all()

                    set_mode("GAME")

                    print(
                        ">>> GAME MODE OFF"
                    )


                # =============================================
                # OPEN PALM
                # =============================================

                elif confirmed == "OPEN PALM":

                    print(
                        ">>> ACCELERATE"
                    )


                # =============================================
                # FIST
                # =============================================

                elif confirmed == "FIST":

                    print(
                        ">>> BRAKE"
                    )


        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.rectangle(
            frame,
            (10, 10),
            (640, 145),
            (0, 0, 0),
            -1
        )


        # ====================================================
        # CURRENT GESTURE
        # ====================================================

        cv2.putText(
            frame,
            f"Gesture: {detected_gesture}",
            (25, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.70,
            (255, 255, 255),
            2
        )


        # ====================================================
        # MODE
        # ====================================================

        mode_text = {
            "NONE": "NO MODE",
            "SYSTEM": "SYSTEM MODE",
            "GAME": "GAME MODE"
        }

        cv2.putText(
            frame,
            f"Mode: {mode_text[mode]}",
            (25, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.70,
            (0, 255, 0),
            2
        )


        # ====================================================
        # MODE HELP
        # ====================================================

        if mode == "SYSTEM":

            help_text = (
                "1F=Mouse  2F=Scroll  "
                "UP=Click  DOWN=Right"
            )

        elif mode == "GAME":

            help_text = (
                "Palm=UP  Fist=DOWN  "
                "1F=Steer  UP=Action"
            )

        else:

            help_text = (
                "F1=SYSTEM  F2=GAME  "
                "ESC=STOP  Q=QUIT"
            )


        cv2.putText(
            frame,
            help_text,
            (25, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
            (0, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "F1 System | F2 Game | ESC Stop | Q Quit",
            (25, 135),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.43,
            (200, 200, 200),
            1
        )


        # ====================================================
        # SHOW WINDOW
        # ====================================================

        cv2.imshow(
            "GestureX - System + Game Controller",
            frame
        )


        # ====================================================
        # Q = QUIT
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# ============================================================
# CLEANUP
# ============================================================

finally:

    # VERY IMPORTANT:
    # Release all game keys if program stops.

    game.release_all()

    cap.release()

    hands.close()

    cv2.destroyAllWindows()

    print()
    print("GestureX stopped safely.")