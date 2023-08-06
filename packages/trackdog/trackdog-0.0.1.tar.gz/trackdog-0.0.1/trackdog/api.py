import logging
import os

from trackdog.store.local import LocalStore
from trackdog.trackdog import Tracker
from varname import argname


def init(project=None, run=None, debug=False):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    global dog
    dog = Tracker(LocalStore(project, run))

def track(val):
    dog.track(val, argname("val"))
