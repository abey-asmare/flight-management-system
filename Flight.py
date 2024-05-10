import random
from randomVariables import Randomly


class Flight(Randomly):
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.priority = self.departure_time.timestamp()

    def __lt__(self, other):
        # Define priority based on departure time; earlier flights have higher priority
        return self.priority < other.priority
    def __gt__(self, other):
        return self.priority > other.priority

