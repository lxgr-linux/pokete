import logging
import os
import threading

from pokete.base.input.recogniser import recogniser
from .audio import audio


class GameContext:
    def __enter__(self):
        threading.Thread(target=recogniser, daemon=True).start()
        print("\033[?1049h")
        os.system("")

    def __exit__(self, exc_type, exc_value, exc_tb):
        recogniser.reset()
        print("\033[?1049l\033[1A")
        logging.info("[General] Exiting...")
        if audio.curr is not None:
            audio.kill()

        if exc_type == KeyboardInterrupt:
            print("\033[?1049l\033[1A\nKeyboardInterrupt")
            return True
        elif exc_type == SystemExit:
            pass
        else:
            logging.error("[General] Error occurend:", exc_info=True)
            return False
