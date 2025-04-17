from threading import Thread

from .exception_propagating_periodic_event import exception_propagating_periodic_event


class PropagatingThread(Thread):
    def run(self):
        try:
            super().run()
        except Exception as e:
            exception_propagating_periodic_event.enq(e)
