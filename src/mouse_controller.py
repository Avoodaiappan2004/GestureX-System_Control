import pyautogui


class MouseController:

    def __init__(self, smoothing=0.20):
        self.screen_width, self.screen_height = pyautogui.size()

        self.smoothing = smoothing

        self.current_x = self.screen_width // 2
        self.current_y = self.screen_height // 2

        self.camera_left = 0.15
        self.camera_right = 0.85
        self.camera_top = 0.15
        self.camera_bottom = 0.85

        # Keep cursor away from the exact screen corners.
        self.screen_margin = 10

    def move_to(self, x, y):

        x = max(self.camera_left, min(x, self.camera_right))
        y = max(self.camera_top, min(y, self.camera_bottom))

        normalized_x = (
            x - self.camera_left
        ) / (
            self.camera_right - self.camera_left
        )

        normalized_y = (
            y - self.camera_top
        ) / (
            self.camera_bottom - self.camera_top
        )

        target_x = (
            self.screen_margin
            + normalized_x
            * (
                self.screen_width
                - 2 * self.screen_margin
            )
        )

        target_y = (
            self.screen_margin
            + normalized_y
            * (
                self.screen_height
                - 2 * self.screen_margin
            )
        )

        self.current_x += (
            target_x - self.current_x
        ) * self.smoothing

        self.current_y += (
            target_y - self.current_y
        ) * self.smoothing

        pyautogui.moveTo(
            int(self.current_x),
            int(self.current_y),
            duration=0
        )

    def click(self):
        pyautogui.click()

    def double_click(self):
        pyautogui.doubleClick()

    def right_click(self):
        pyautogui.rightClick()