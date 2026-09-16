import time
import pyautogui


class ScrollController:

    def __init__(self):

        # =====================================================
        # SMOOTHED PALM POSITION
        # =====================================================

        self.smoothed_x = None
        self.smoothed_y = None

        # Previous smoothed position
        self.previous_x = None
        self.previous_y = None

        # Accumulated movement
        self.accumulated_x = 0.0
        self.accumulated_y = 0.0

        # =====================================================
        # TUNING
        # =====================================================

        # Your current vertical tuning
        self.smoothing = 0.95

        # Ignore extremely tiny camera noise
        self.dead_zone = 0.0025

        # Vertical sensitivity
        self.vertical_sensitivity = 3900

        # Horizontal sensitivity
        self.horizontal_sensitivity = 3900

        # Maximum wheel movement
        self.max_scroll = 75

        # Maximum horizontal wheel movement
        self.max_horizontal_scroll = 75

        # Prevent excessive events
        self.cooldown = 0.035

        self.last_scroll_time = 0


    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, x, y):

        # =====================================================
        # FIRST FRAME
        # =====================================================

        if self.smoothed_x is None:

            self.smoothed_x = x
            self.smoothed_y = y

            self.previous_x = x
            self.previous_y = y

            return


        # =====================================================
        # SMOOTH X
        # =====================================================

        self.smoothed_x += (
            x - self.smoothed_x
        ) * self.smoothing


        # =====================================================
        # SMOOTH Y
        # =====================================================

        self.smoothed_y += (
            y - self.smoothed_y
        ) * self.smoothing


        # =====================================================
        # MOVEMENT
        # =====================================================

        movement_x = (
            self.previous_x
            - self.smoothed_x
        )

        movement_y = (
            self.previous_y
            - self.smoothed_y
        )


        # Update previous position
        self.previous_x = self.smoothed_x
        self.previous_y = self.smoothed_y


        # =====================================================
        # DEAD ZONE
        # =====================================================

        if (
            abs(movement_x) < self.dead_zone
            and
            abs(movement_y) < self.dead_zone
        ):
            return


        # =====================================================
        # ACCUMULATE
        # =====================================================

        if abs(movement_x) >= self.dead_zone:

            self.accumulated_x += movement_x


        if abs(movement_y) >= self.dead_zone:

            self.accumulated_y += movement_y


        # =====================================================
        # COOLDOWN
        # =====================================================

        now = time.time()

        if (
            now - self.last_scroll_time
            < self.cooldown
        ):
            return


        # =====================================================
        # CALCULATE VERTICAL SCROLL
        # =====================================================

        vertical_scroll = int(
            self.accumulated_y
            * self.vertical_sensitivity
        )


        # =====================================================
        # CALCULATE HORIZONTAL SCROLL
        # =====================================================

        horizontal_scroll = int(
            self.accumulated_x
            * self.horizontal_sensitivity
        )


        # =====================================================
        # MINIMUM VERTICAL MOVEMENT
        # =====================================================

        if (
            vertical_scroll == 0
            and
            abs(self.accumulated_y)
            >= self.dead_zone
        ):

            vertical_scroll = (
                1
                if self.accumulated_y > 0
                else -1
            )


        # =====================================================
        # MINIMUM HORIZONTAL MOVEMENT
        # =====================================================

        if (
            horizontal_scroll == 0
            and
            abs(self.accumulated_x)
            >= self.dead_zone
        ):

            horizontal_scroll = (
                1
                if self.accumulated_x > 0
                else -1
            )


        # =====================================================
        # LIMIT VERTICAL SPEED
        # =====================================================

        vertical_scroll = max(
            -self.max_scroll,
            min(
                vertical_scroll,
                self.max_scroll
            )
        )


        # =====================================================
        # LIMIT HORIZONTAL SPEED
        # =====================================================

        horizontal_scroll = max(
            -self.max_horizontal_scroll,
            min(
                horizontal_scroll,
                self.max_horizontal_scroll
            )
        )


        # =====================================================
        # SEND VERTICAL SCROLL
        # =====================================================

        if vertical_scroll != 0:

            pyautogui.scroll(
                vertical_scroll
            )


        # =====================================================
        # SEND HORIZONTAL SCROLL
        # =====================================================

        if horizontal_scroll != 0:

            pyautogui.hscroll(
                horizontal_scroll
            )


        # =====================================================
        # UPDATE TIME
        # =====================================================

        if (
            vertical_scroll != 0
            or
            horizontal_scroll != 0
        ):

            self.last_scroll_time = now


        # =====================================================
        # REMOVE USED VERTICAL MOVEMENT
        # =====================================================

        if vertical_scroll != 0:

            self.accumulated_y -= (
                vertical_scroll
                / self.vertical_sensitivity
            )


        # =====================================================
        # REMOVE USED HORIZONTAL MOVEMENT
        # =====================================================

        if horizontal_scroll != 0:

            self.accumulated_x -= (
                horizontal_scroll
                / self.horizontal_sensitivity
            )


    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.smoothed_x = None
        self.smoothed_y = None

        self.previous_x = None
        self.previous_y = None

        self.accumulated_x = 0.0
        self.accumulated_y = 0.0

        self.last_scroll_time = 0