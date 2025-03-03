import logging
import os

from pokete.base.exception_propagation import PropagatingThread
from pokete.base.input.recogniser import recogniser
from .audio import audio


class GameContext:
    def __enter__(self):
        PropagatingThread(target=recogniser, daemon=True).start()
        os.system("")
        print("\033[?1049h" + "\033[?25l")

    def __exit__(self, exc_type, exc_value, exc_tb):
        recogniser.reset()
        print("\033[?1049l\033[1A" + "\033[?25h")
        logging.info("[General] Exiting...")
        audio.kill()

        if exc_type == KeyboardInterrupt:
            print("\033[?1049l\033[1A\nKeyboardInterrupt")
            return True
        elif exc_type == SystemExit:
            pass
        else:
            logging.error("[General] Error occurend:", exc_info=True)
            return False
