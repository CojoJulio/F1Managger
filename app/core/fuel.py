def updateFuel(raceCarState, pilot, deltaTime):
    consumoBase = 0.05
    raceCarState.fuel -= consumoBase * (1 + pilot.agresividad / 100) * deltaTime

    if raceCarState.fuel < 0:
        raceCarState.fuel = 0
