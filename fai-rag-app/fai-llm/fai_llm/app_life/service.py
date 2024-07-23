from typing import Callable


class AppLifeService:
    _shutdown_events: list[Callable]

    def __init__(self):
        self._shutdown_events = []

    def shutdown(self):
        for event in self._shutdown_events:
            event()

    def add_on_shutdown(self, callback: Callable):
        self._shutdown_events.append(callback)
