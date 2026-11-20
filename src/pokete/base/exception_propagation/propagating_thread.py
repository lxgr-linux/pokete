from threading import Thread
from typing import override

from .exception_propagating_periodic_event import (
    exception_propagating_periodic_event,
)


class PropagatingThread(Thread):
    @override
    def run(self) -> None:
        try:
            super().run()
        except Exception as e:  # noqa: BLE001
            exception_propagating_periodic_event.enq(e)
