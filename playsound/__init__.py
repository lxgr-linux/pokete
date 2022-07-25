import ctypes
import time
import logging


def playsound(file):
    logging.info("[Playsound] playing %s", file)
    _playsound.playsound(file.encode("utf-8"))


_playsound = ctypes.cdll.LoadLibrary('./playsound/libplaysound.so')
