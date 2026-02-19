import random
from typing import List
from models.race_car import RaceCar
from models.track import Track

class RaceState:

    
    def __init__(self):
        self.track = None
        self.raceCars = []
        self.running = False
        self.time_scale = 1.0
        self.fastest_lap = None
        self.fastest_lap_car = None
        self.events = []

race_state = RaceState()
