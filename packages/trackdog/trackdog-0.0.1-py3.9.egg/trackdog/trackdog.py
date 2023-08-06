import logging
from varname import nameof


class Tracker():
    def __init__(self, store=None, path=None):
        self.store = store
        self.path = path
        self.logger = logging.getLogger(__name__)

    def track(self, val):
        self.logger.debug('tracking %s', nameof(val))
