from core.track import getCurrentSector
from variables.variables import sector_speed_modifiers, drs_multiplier
import random

def calculateSpeed(track, pilot, car, tyre, raceCarState):

    velocidadBase = track.lapLength / track.baseLapTime

    sector = getCurrentSector(track, raceCarState)

    sectorData = sector_speed_modifiers[sector.type]

    pilotFactor = 1 + (pilot.skill - 50) * 0.002
    carFactor = 1 + (car.performance - 50) * 0.002
    tyreFactor = tyre.grip

    desgasteFactor = 0.7 + (tyre.wear / 100) * 0.3
    fuelFactor = 0.9 + (raceCarState.fuel / 100) * 0.1

    randomFactor = 1 + (random.uniform(-0.02, 0.02))

    speed = velocidadBase * pilotFactor * carFactor * tyreFactor * desgasteFactor * fuelFactor * randomFactor * sectorData["baseMultiplier"]

    if speed > sectorData["maxSpeed"]:
        speed = sectorData["maxSpeed"]

    if raceCarState.drsActive:
        speed *= drs_multiplier
    
    return round(speed * 3.6)