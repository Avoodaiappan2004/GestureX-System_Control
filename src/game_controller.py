import pyautogui


class GameController:

    def __init__(self):
        self.keys_down = set()

    # =========================================
    # PRESS ONCE
    # =========================================

    def press(self, key):
        pyautogui.press(key)

    # =========================================
    # HOLD KEY
    # =========================================

    def hold(self, key):
        if key not in self.keys_down:
            pyautogui.keyDown(key)
            self.keys_down.add(key)

    # =========================================
    # RELEASE KEY
    # =========================================

    def release(self, key):
        if key in self.keys_down:
            pyautogui.keyUp(key)
            self.keys_down.remove(key)

    # =========================================
    # RELEASE ALL
    # =========================================

    def release_all(self):
        for key in list(self.keys_down):
            pyautogui.keyUp(key)

        self.keys_down.clear()

    # =========================================
    # ACCELERATE
    # =========================================

    def accelerate(self):
        self.release("down")
        self.release("left")
        self.release("right")

        self.hold("up")

    # =========================================
    # BRAKE
    # =========================================

    def brake(self):
        self.release("up")
        self.release("left")
        self.release("right")

        self.hold("down")

    # =========================================
    # STEER LEFT
    # =========================================

    def steer_left(self):
        self.release("up")
        self.release("down")

        self.hold("left")

    # =========================================
    # STEER RIGHT
    # =========================================

    def steer_right(self):
        self.release("up")
        self.release("down")

        self.hold("right")

    # =========================================
    # RELEASE MOVEMENT
    # =========================================

    def release_movement(self):
        self.release("up")
        self.release("down")
        self.release("left")
        self.release("right")

    # =========================================
    # GAME ACTION
    # =========================================

    def action(self):
        pyautogui.press("space")