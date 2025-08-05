"""
This module holds the helper functions for the mouse handler.
"""

# 1st party imports
from typing import Tuple
from collections import deque


class Smoother:
    """
    This class is used to smooth the mouse position.
    """

    def __init__(self, max_len: int = 10):
        """
        This method is used to initialize the smoother.
        """
        self.xs = deque(maxlen=max_len)
        self.ys = deque(maxlen=max_len)

    def smooth(self, x: int, y: int) -> Tuple[int, int]:
        """
        This method is used to smooth the mouse position.

        Args:
            x: The x coordinate of the mouse position.
            y: The y coordinate of the mouse position.

        Returns:
            Tuple[int, int]: The smoothed mouse position.
        """

        self.xs.append(x)
        self.ys.append(y)
        avg_x = int(sum(self.xs) / len(self.xs))
        avg_y = int(sum(self.ys) / len(self.ys))
        return avg_x, avg_y
