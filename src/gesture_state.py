from collections import deque


class GestureState:
    """
    Stabilizes gesture detection over multiple frames.

    A gesture must appear consistently for several frames
    before it becomes the confirmed gesture.
    """

    def __init__(self, history_size=7, required_frames=5):
        self.history = deque(maxlen=history_size)

        self.required_frames = required_frames

        self.current_gesture = "NO HAND"
        self.last_confirmed_gesture = "NO HAND"

    def update(self, gesture):
        """
        Add a new gesture observation.

        Returns:
            confirmed gesture
            OR
            None if the gesture is not stable yet.
        """

        self.history.append(gesture)

        # Not enough samples yet
        if len(self.history) < self.required_frames:
            return None

        recent = list(self.history)[-self.required_frames:]

        # All recent frames must be the same
        if len(set(recent)) != 1:
            return None

        stable_gesture = recent[0]

        self.current_gesture = stable_gesture

        # Return only when gesture changes
        if stable_gesture != self.last_confirmed_gesture:

            self.last_confirmed_gesture = stable_gesture

            return stable_gesture

        return None

    def reset(self):
        self.history.clear()

        self.current_gesture = "NO HAND"
        self.last_confirmed_gesture = "NO HAND"