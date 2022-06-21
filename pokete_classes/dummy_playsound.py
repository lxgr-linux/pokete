"""Dummy fallback sound module"""

import time
from release import SPEED_OF_TIME

def playsound(song):
    """Dummy fallback playsound function"""
    time.sleep(SPEED_OF_TIME * 5)
