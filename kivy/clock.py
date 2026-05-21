# clock.py
import time

class Clock:
    @staticmethod
    def schedule_interval(callback, interval):
        # For testing, call callback a few times then stop (avoid infinite loop)
        for _ in range(3):
            callback(0)
