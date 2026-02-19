from core.track import getCurrentSector
from variables.variables import sector_wear_multiplier


def updateTyreWear(tyre, pilot, deltaTime, track, raceCarState):

    sector = getCurrentSector(track, raceCarState)

    desgasteBase = 0.12
    tyre.wear -= desgasteBase * sector_wear_multiplier[sector.type] * (1 + pilot.agresividad / 100) * deltaTime

    if tyre.wear < 0:
        tyre.wear = 0