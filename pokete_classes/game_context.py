import logging
import threading
from types import TracebackType

from .audio import audio
from .input.recogniser import recogniser


class GameContext:
    def __enter__(self):
        threading.Thread(target=recogniser, daemon=True).start()
        print("\033[?1049h")

    def __exit__(self, exc_type, exc_value, exc_tb:TracebackType):
        recogniser.reset()
        print("\033[?1049l\033[1A")
        logging.info("[General] Exiting...")
        if audio.curr is not None:
            audio.kill()

        if exc_type == KeyboardInterrupt:
            print("\033[?1049l\033[1A\nKeyboardInterrupt")
            return True
        else:
            logging.error("[General] Error occurend:", exc_info=True)
            return False
