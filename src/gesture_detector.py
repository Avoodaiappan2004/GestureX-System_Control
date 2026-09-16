import math


def distance(p1, p2):
    """Euclidean distance between two MediaPipe landmarks."""
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def dot(ax, ay, bx, by):
    return ax * bx + ay * by


def normalize(x, y):
    length = math.hypot(x, y)

    if length == 0:
        return 0.0, 0.0

    return x / length, y / length


def finger_states(hand_landmarks):
    """
    Returns:
        [thumb, index, middle, ring, pinky]

    True  = open
    False = closed
    """

    lm = hand_landmarks.landmark

    # Other four fingers
    index_open = lm[8].y < lm[6].y
    middle_open = lm[12].y < lm[10].y
    ring_open = lm[16].y < lm[14].y
    pinky_open = lm[20].y < lm[18].y

    # Thumb extension
    thumb_length = distance(lm[4], lm[2])
    palm_width = distance(lm[5], lm[17])

    thumb_open = thumb_length > palm_width * 0.65

    return [
        thumb_open,
        index_open,
        middle_open,
        ring_open,
        pinky_open
    ]


def four_fingers_closed(lm):
    """
    Check that index, middle, ring and pinky are clearly folded.
    Distance-based check is more reliable than Y-only check.
    """

    wrist = lm[0]

    palm_size = distance(lm[0], lm[9])

    if palm_size == 0:
        return False

    fingers = [
        (8, 6),    # index tip / PIP
        (12, 10),  # middle
        (16, 14),  # ring
        (20, 18)   # pinky
    ]

    for tip, pip in fingers:

        tip_to_wrist = distance(lm[tip], wrist)
        pip_to_wrist = distance(lm[pip], wrist)

        # Tip should be closer to wrist than its PIP
        # when the finger is folded.
        if tip_to_wrist > pip_to_wrist * 1.05:
            return False

    return True


def detect_thumb_gesture(lm):
    """
    Detect THUMBS UP / THUMBS DOWN.

    Requirements:
    - Index, middle, ring and pinky must be folded.
    - Thumb must be clearly extended.
    - Thumb tip must be clearly above or below the palm.
    """

    # ------------------------------------------------
    # 1. Check the four non-thumb fingers
    # ------------------------------------------------
    wrist = lm[0]

    folded_fingers = 0

    for tip, pip in [
        (8, 6),    # index
        (12, 10),  # middle
        (16, 14),  # ring
        (20, 18)   # pinky
    ]:
        tip_dist = distance(lm[tip], wrist)
        pip_dist = distance(lm[pip], wrist)

        # Folded finger -> fingertip is closer to wrist
        if tip_dist < pip_dist * 1.10:
            folded_fingers += 1

    if folded_fingers < 3:
        return None

    # ------------------------------------------------
    # 2. Thumb must be extended
    # ------------------------------------------------
    thumb_tip = lm[4]
    thumb_ip = lm[3]
    thumb_mcp = lm[2]

    palm_size = distance(lm[0], lm[9])

    if palm_size == 0:
        return None

    thumb_length = (
        distance(thumb_mcp, thumb_ip)
        + distance(thumb_ip, thumb_tip)
    )

    if thumb_length < palm_size * 0.55:
        return None

    # ------------------------------------------------
    # 3. Thumb must be separated from the palm
    # ------------------------------------------------
    thumb_from_wrist = distance(thumb_tip, wrist)

    if thumb_from_wrist < palm_size * 0.65:
        return None

    # ------------------------------------------------
    # 4. Compare thumb tip with wrist vertically
    #
    # MediaPipe image coordinates:
    # smaller Y = higher on screen
    # larger Y  = lower on screen
    # ------------------------------------------------
    vertical_difference = thumb_tip.y - wrist.y

    # Minimum vertical separation
    threshold = palm_size * 0.20

    # ------------------------------------------------
    # 5. THUMBS UP
    # ------------------------------------------------
    if vertical_difference < -threshold:
        return "THUMBS UP"

    # ------------------------------------------------
    # 6. THUMBS DOWN
    # ------------------------------------------------
    if vertical_difference > threshold:
        return "THUMBS DOWN"

    return None


def detect_gesture(hand_landmarks):

    lm = hand_landmarks.landmark

    fingers = finger_states(hand_landmarks)

    thumb, index, middle, ring, pinky = fingers

    # ==========================================
    # THUMBS UP / DOWN
    # ==========================================

    thumb_gesture = detect_thumb_gesture(lm)

    if thumb_gesture is not None:
        return thumb_gesture, fingers

    # ==========================================
    # OPEN PALM
    # ==========================================

    if (
        thumb
        and index
        and middle
        and ring
        and pinky
    ):
        return "OPEN PALM", fingers

    # ==========================================
    # FIST
    # ==========================================

    if (
        not index
        and not middle
        and not ring
        and not pinky
        and not thumb
    ):
        return "FIST", fingers

    # ==========================================
    # ONE FINGER
    # ==========================================

    if (
        index
        and not middle
        and not ring
        and not pinky
    ):
        return "ONE FINGER", fingers

    # ==========================================
    # TWO FINGERS
    # ==========================================

    if (
        index
        and middle
        and not ring
        and not pinky
    ):
        return "TWO FINGERS", fingers

    return "UNKNOWN", fingers