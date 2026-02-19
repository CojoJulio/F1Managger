from core.gap import update_positions_and_gaps
from core.pitstop import pitTick, checkPitEntry
from core.overtake import updateDRS, tryOvertake, executeOvertake
from core.track import getCurrentSector
from core.tyre import updateTyreWear
from core.fuel import updateFuel
from core.speed import calculateSpeed
from state.race_state import race_state

def simulationTick(raceCar, track, deltaTime = 1):

    if raceCar.state.in_pit:
        pitTick(raceCar, deltaTime)
        return
    
    checkPitEntry(raceCar, track)

    sector = getCurrentSector(track, raceCar.state)

    speed = calculateSpeed(track, raceCar.pilot, raceCar.car, raceCar.tyre, raceCar.state)

    raceCar.state.speed = speed

    avance = speed * deltaTime
    raceCar.state.lapProgress += avance / track.lapLength
    raceCar.state.totalTime += deltaTime

    updateTyreWear(raceCar.tyre, raceCar.pilot, deltaTime, track, raceCar.state)
    updateFuel(raceCar.state, raceCar.pilot, deltaTime)


    if  raceCar.state.lapProgress >= 1:

        lap_time = raceCar.state.totalTime - raceCar.state.lap_start_time
        raceCar.lap_history.append(lap_time)
        raceCar.state.last_lap_time = lap_time
        raceCar.state.lap_start_time = raceCar.state.totalTime

        raceCar.state.lap += 1
        raceCar.state.lapProgress -= 1

        if ( race_state.fastest_lap is None or lap_time < race_state.fastest_lap):
            race_state.fastest_lap = lap_time
            race_state.fastest_lap_car = raceCar.pilot.name

        race_state.events.append({
            "type": "lap_complete",
            "payload": {
                "car_id": raceCar.id,
                "lap": raceCar.state.lap,
                "lap_time": lap_time
            }
        })

def raceTick(raceCars, track, deltaTime = 1):
    for raceCar in raceCars:
        simulationTick(raceCar, track, deltaTime)

    raceCars.sort(key=lambda x: x.state.lapProgress, reverse=True)

    update_positions_and_gaps(raceCars, track.lapLength)

    for i, raceCar in enumerate(raceCars):
        if raceCar.state.position != i + 1:
            race_state.events.append({
                "type": "overtake",
                "payload": {
                    "car_id": raceCar.id,
                    "new_position": i + 1
                }
            })
        raceCar.state.position = i + 1

    for i in range(len(raceCars)):
        behind = raceCars[i]
        ahead = raceCars[i - 1]

        sector = getCurrentSector(track, behind.state)

        updateDRS(behind, ahead, sector, track)

        if tryOvertake(behind, ahead, sector, track):
            executeOvertake(behind, ahead)