import logging
import os
from types import TracebackType

from pokete.base.exception_propagation import PropagatingThread
from pokete.base.input.recogniser import recogniser
from pokete.base.single_event import single_event_periodic_event

from .audio import audio


class GameContext:
    def __enter__(self) -> None:
        PropagatingThread(target=recogniser, daemon=True).start()
        single_event_periodic_event.monitor()
        os.system("")
        print("\033[?1049h" + "\033[?25l" + "\033[?1003h\033[?1015h\033[?1006h")

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_tb: TracebackType | None) -> None:
        recogniser.reset()
        print(
            "\033[?1049l\033[1A"
            + "\033[?25h"
            + "\033[?1000l"
            + "\033[?1003l\033[?1015l\033[?1006l"
        )
        logging.info("[General] Exiting...")
        audio.kill()

        if exc_type == KeyboardInterrupt:
            print("\033[?1049l\033[1A\nKeyboardInterrupt")
            return True
        elif exc_type == SystemExit:
            pass
        else:
            logging.error("[General] Error occurend:")
            return False
