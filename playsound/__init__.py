import ctypes
import time
import logging


def playsound(file):
    logging.info(file)
    _playsound.playsound(file.encode("utf-8"))
    logging.info("1")


_playsound = ctypes.cdll.LoadLibrary('./playsound/libplaysound.so')
