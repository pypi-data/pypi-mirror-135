import os
from trackdog.store.local import LocalStore
from trackdog.trackdog import Tracker

dog = Tracker()

def init(project=None):
    dog = Tracker(LocalStore(project))

def track(val):
    dog.track(val)
