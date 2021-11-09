import logging

from prometheus_client import make_asgi_app, Counter, Histogram, generate_latest
from quart import Quart


class Prometheus:
    def __init__(self) -> None:
        self.prometheus = None
        self.countdowns = Histogram('countdowns', "Numbers users make bot count to")
        self.commands = Counter('commands_total', "Total number of given commands")
        self.invalid_commands = Counter('invalid_commands', "Total number of given invalid commands")
        self.canceled = Counter('commands_canceld', "Number of canceled countdowns")
        self.error_starts = Counter('error_starts', "Number of times, users tried to strart second countdown")
        self.error_stops = Counter('error_stops', "Number of times users tried to stop countdown, that wasn't there")

    def init(self):
        self.prometheus = make_asgi_app()


prometheus = Prometheus()
quart = Quart(__name__)
logging.getLogger('quart.app').setLevel(logging.ERROR)
logging.getLogger('quart.serving').setLevel(logging.ERROR)


@quart.route('/metrics')
def metrics():
    return generate_latest()
